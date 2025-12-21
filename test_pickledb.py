# test_pickledb.py
import os
import json
import asyncio
from pathlib import Path

import pytest

from pickledb import PickleDB, PickleDBSQLite  # adjust this import if your module name is different


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_tmp_path(tmp_path, name="db.json") -> Path:
    """Helper to get a db path inside pytest's tmp_path fixture."""
    return tmp_path / name


# ---------------------------------------------------------------------------
# Basic sync usage (PickleDB)
# ---------------------------------------------------------------------------

def test_sync_set_get_save_and_reload(tmp_path):
    db_path = make_tmp_path(tmp_path)
    db = PickleDB(str(db_path))

    # sync .set() & .save() use dualmethod (internally asyncio.run)
    assert db.set("foo", {"bar": 1}) is True
    assert db.set("num", 123) is True
    assert db.save() is True

    # New instance loads from same file
    db2 = PickleDB(str(db_path))
    db2.load()
    assert db2.get("foo") == {"bar": 1}
    assert db2.get("num") == 123


def test_sync_get_default_and_missing_key(tmp_path):
    db_path = make_tmp_path(tmp_path)
    db = PickleDB(str(db_path))

    db.set("exists", "yep")
    db.save()

    db2 = PickleDB(str(db_path))
    db2.load()

    assert db2.get("exists", default="nope") == "yep"
    assert db2.get("missing", default="nope") == "nope"
    # default=None is implicit
    assert db2.get("also_missing") is None


def test_sync_remove_and_all(tmp_path):
    db_path = make_tmp_path(tmp_path)
    db = PickleDB(str(db_path))

    db.set("a", 1)
    db.set("b", 2)
    db.set("c", 3)

    keys = db.all()
    assert set(keys) == {"a", "b", "c"}

    # remove existing key returns True
    assert db.remove("b") is True
    # removing again returns False
    assert db.remove("b") is False

    keys_after = db.all()
    assert set(keys_after) == {"a", "c"}


def test_sync_purge_clears_database(tmp_path):
    db_path = make_tmp_path(tmp_path)
    db = PickleDB(str(db_path))

    db.set("x", 1)
    db.set("y", 2)
    assert set(db.all()) == {"x", "y"}

    assert db.purge() is True
    assert db.all() == []

    db.save()

    # After reload, still empty
    db2 = PickleDB(str(db_path))
    db2.load()
    assert db2.all() == []


# ---------------------------------------------------------------------------
# Basic async usage (PickleDB)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_async_set_get_save_and_reload(tmp_path):
    db_path = make_tmp_path(tmp_path)
    db = PickleDB(str(db_path))

    await db.set("foo", {"bar": 1})
    await db.set("num", 123)
    await db.save()

    db2 = PickleDB(str(db_path))
    await db2.load()
    assert await db2.get("foo") == {"bar": 1}
    assert await db2.get("num") == 123


@pytest.mark.asyncio
async def test_async_get_default(tmp_path):
    db_path = make_tmp_path(tmp_path)
    db = PickleDB(str(db_path))

    await db.set("exists", "yep")
    await db.save()

    db2 = PickleDB(str(db_path))
    await db2.load()

    assert await db2.get("exists", default="nope") == "yep"
    assert await db2.get("missing", default="nope") == "nope"
    assert await db2.get("also_missing") is None


@pytest.mark.asyncio
async def test_async_remove_all_purge(tmp_path):
    db_path = make_tmp_path(tmp_path)
    db = PickleDB(str(db_path))

    await db.set("a", 1)
    await db.set("b", 2)
    await db.set("c", 3)

    keys = await db.all()
    assert set(keys) == {"a", "b", "c"}

    assert await db.remove("b") is True
    assert await db.remove("b") is False
    keys_after = await db.all()
    assert set(keys_after) == {"a", "c"}

    assert await db.purge() is True
    assert await db.all() == []


# ---------------------------------------------------------------------------
# Context managers (PickleDB)
# ---------------------------------------------------------------------------

def test_sync_context_manager_saves_on_success(tmp_path):
    db_path = make_tmp_path(tmp_path)

    with PickleDB(str(db_path)) as db:
        db.set("inside", "context")
        # __exit__ should call .save() because no exception

    # New instance: must see saved data
    db2 = PickleDB(str(db_path))
    db2.load()
    assert db2.get("inside") == "context"


def test_sync_context_manager_does_not_save_on_exception(tmp_path):
    db_path = make_tmp_path(tmp_path)

    try:
        with PickleDB(str(db_path)) as db:
            db.set("inside", "context")
            raise RuntimeError("boom")
    except RuntimeError:
        pass

    # Because __exit__ sees an exception, it should NOT call .save()
    # Therefore file may not exist, or be empty.
    if db_path.exists():
        content = db_path.read_bytes()
        assert content == b""  # empty file
    else:
        # No file is also acceptable
        assert not db_path.exists()


@pytest.mark.asyncio
async def test_async_context_manager_saves_on_success(tmp_path):
    db_path = make_tmp_path(tmp_path)

    async with PickleDB(str(db_path)) as db:
        await db.set("inside", "async_context")

    db2 = PickleDB(str(db_path))
    await db2.load()
    assert await db2.get("inside") == "async_context"


@pytest.mark.asyncio
async def test_async_context_manager_does_not_save_on_exception(tmp_path):
    db_path = make_tmp_path(tmp_path)

    with pytest.raises(RuntimeError):
        async with PickleDB(str(db_path)) as db:
            await db.set("inside", "async_context")
            raise RuntimeError("boom")

    if db_path.exists():
        content = db_path.read_bytes()
        assert content == b""
    else:
        assert not db_path.exists()


# ---------------------------------------------------------------------------
# Edge cases: missing file, empty file, atomic save (PickleDB)
# ---------------------------------------------------------------------------

def test_load_on_missing_file_returns_empty_db(tmp_path):
    db_path = make_tmp_path(tmp_path)
    assert not db_path.exists()

    db = PickleDB(str(db_path))
    db.load()
    assert db.all() == []
    # After save, file should exist with {} or similar JSON
    db.save()
    assert db_path.exists()

    raw = db_path.read_bytes()
    data = json.loads(raw.decode("utf-8")) if raw else {}
    assert data == {}


def test_load_on_empty_file_returns_empty_db(tmp_path):
    db_path = make_tmp_path(tmp_path)
    db_path.write_text("")  # existing but empty file

    db = PickleDB(str(db_path))
    # load() treats 0-byte file as empty db
    db.load()
    assert db.all() == []


def test_save_uses_temp_file_and_is_atomic(tmp_path):
    db_path = make_tmp_path(tmp_path)
    tmp_name = str(db_path) + ".tmp"

    db = PickleDB(str(db_path))
    db.set("a", 1)
    db.save()

    # temp file should not be left behind
    assert not os.path.exists(tmp_name)

    # file should be valid JSON (orjson output is still standard JSON)
    raw = db_path.read_bytes()
    data = json.loads(raw.decode("utf-8"))
    assert data == {"a": 1}


# ---------------------------------------------------------------------------
# Concurrency tests (PickleDB)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_async_concurrent_sets_are_all_present(tmp_path):
    db_path = make_tmp_path(tmp_path)
    db = PickleDB(str(db_path))

    async def writer(start, end):
        for i in range(start, end):
            await db.set(f"key_{i}", i)

    # Kick off a few concurrent writers
    tasks = [
        asyncio.create_task(writer(0, 300)),
        asyncio.create_task(writer(300, 600)),
        asyncio.create_task(writer(600, 1000)),
    ]
    await asyncio.gather(*tasks)

    keys = await db.all()
    assert len(keys) == 1000
    # spot check
    assert await db.get("key_0") == 0
    assert await db.get("key_999") == 999


@pytest.mark.asyncio
async def test_async_concurrent_gets_and_sets(tmp_path):
    db_path = make_tmp_path(tmp_path)
    db = PickleDB(str(db_path))

    await db.set("counter", 0)

    async def incrementer(n_times):
        for _ in range(n_times):
            # Not atomic on purpose, but we are testing that we don't crash
            current = await db.get("counter", 0)
            await db.set("counter", current + 1)

    tasks = [asyncio.create_task(incrementer(100)) for _ in range(10)]
    await asyncio.gather(*tasks)

    # We *expect* the final value to be <= 1000 because increments are not atomic.
    # The important part is no exceptions and a sensible final value.
    final_value = await db.get("counter")
    assert 0 < final_value <= 1000


# ---------------------------------------------------------------------------
# Stress test: 1,000,000 key-value pairs (PickleDB)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
@pytest.mark.stress
async def test_stress_one_million_entries(tmp_path):
    """
    Stress test inserting and retrieving 1,000,000 key-value pairs.

    NOTE:
    - This test is intentionally heavy and may take a long time.
    - Run it explicitly: `pytest -m stress`.
    """
    N = 1_000_000
    db_path = make_tmp_path(tmp_path, "stress_db.json")
    db = PickleDB(str(db_path))

    # Insert 1M entries
    for i in range(N):
        await db.set(f"key_{i}", i)

    # Retrieve 1M entries
    for i in range(N):
        value = await db.get(f"key_{i}")
        assert value == i

    await db.save()
    assert db_path.exists()


# ---------------------------------------------------------------------------
# Basic tests for PickleDBSQLite
# ---------------------------------------------------------------------------

def test_sqlite_sync_set_get_and_all(tmp_path):
    sqlite_path = tmp_path / "kv.sqlite3"
    kv = PickleDBSQLite(str(sqlite_path))

    key1 = kv.set(None, {"foo": "bar"})
    key2 = kv.set("explicit", [1, 2, 3])

    assert isinstance(key1, str)
    assert key2 == "explicit"

    assert kv.get(key1) == {"foo": "bar"}
    assert kv.get("explicit") == [1, 2, 3]

    keys = set(kv.all())
    assert key1 in keys
    assert "explicit" in keys

    kv.close()


@pytest.mark.asyncio
async def test_sqlite_async_set_get_and_purge(tmp_path):
    sqlite_path = tmp_path / "kv_async.sqlite3"
    kv = PickleDBSQLite(str(sqlite_path))

    key = await kv.set(None, {"async": True})
    assert await kv.get(key) == {"async": True}

    await kv.set("x", 1)
    await kv.set("y", 2)
    keys = set(await kv.all())
    assert key in keys
    assert {"x", "y"} <= keys

    assert await kv.remove("x") is True
    assert await kv.remove("x") is False

    assert await kv.purge() is True
    assert await kv.all() == []

    await kv.close()

