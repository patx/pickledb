"""
pickleDB - https://patx.github.io/pickledb
Harrison Erd - https://harrisonerd.com/
Licensed - BSD 3 Clause (see LICENSE)
"""

import asyncio
import os
from typing import Any
import uuid

import orjson
import aiofiles
try:
    import sqlite3
    import aiosqlite
    sqlite_enable = True
except ImportError:
    sqlite_enable = False


MISSING = object()


def in_async() -> bool:
    """Return True if we're currently running inside an event loop."""
    try:
        asyncio.get_running_loop()
        return True
    except RuntimeError:
        return False


def dualmethod(func):
    """
    Decorator that lets an async method be called in both sync and async code.

    - In async code: returns the coroutine (you must `await` it).
    - In sync code: runs the coroutine with asyncio.run() and returns the result.
    """
    def wrapper(self, *args, **kwargs):
        coro = func(self, *args, **kwargs)
        if in_async():
            return coro
        return asyncio.run(coro)
    return wrapper


class PickleDB:
    """
    A unified async/sync key-value store using orjson + aiofiles.

    All data is kept in-memory in `self.db` and serialized to disk as a single
    orjson-encoded file at `self.location`.
    """

    def __init__(self, location: str):
        self.location = os.path.expanduser(location)
        self.db: dict[str, Any] = {}
        self._lock = asyncio.Lock()

    def __enter__(self):
        self.load()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.save()

    async def __aenter__(self):
        await self.load()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            await self.save()

    @dualmethod
    async def load(self) -> bool:
        """
        Load JSON database from disk into memory.

        Returns True on success (or if the file did not exist / was empty).
        """
        if os.path.exists(self.location) and os.path.getsize(self.location) > 0:
            async with aiofiles.open(self.location, "rb") as f:
                data = await f.read()
            new_db = orjson.loads(data)
        else:
            new_db = {}

        async with self._lock:
            self.db = new_db
        return True

    @dualmethod
    async def save(self) -> bool:
        """
        Atomically save database to disk.

        Writes to `<location>.tmp` and then os.replace() over the original file.
        Returns True on success.
        """
        temp = f"{self.location}.tmp"
        async with self._lock:
            async with aiofiles.open(temp, "wb") as f:
                await f.write(orjson.dumps(self.db))
            await asyncio.to_thread(os.replace, temp, self.location)
        return True

    @dualmethod
    async def set(self, key, value) -> bool:
        """Set a key-value pair. Always returns True."""
        async with self._lock:
            self.db[str(key)] = value
        return True

    @dualmethod
    async def get(self, key, default=None):
        """Get a key's value, or `default` if missing."""
        async with self._lock:
            return self.db.get(str(key), default)

    @dualmethod
    async def remove(self, key) -> bool:
        """Remove a key-value pair. Returns True if it existed, False otherwise."""
        async with self._lock:
            return self.db.pop(str(key), None) is not None

    @dualmethod
    async def all(self):
        """Return a list of all keys."""
        async with self._lock:
            return list(self.db.keys())

    @dualmethod
    async def purge(self) -> bool:
        """Remove all key-value pairs from the database. Always returns True."""
        async with self._lock:
            self.db.clear()
        return True

if sqlite_enable:
    class PickleDBSQLite:
        """
        A unified async/sync key-value store backed by SQLite.

        Each key is stored as a row:

            CREATE TABLE kv (
                key   TEXT PRIMARY KEY,
                value BLOB NOT NULL
            )

        Values are stored as JSON-encoded bytes via orjson.
        """

        def __init__(
            self,
            sqlite_path: str = "pickledb.sqlite3",
            table_name: str = "kv",
        ) -> None:
            self.sqlite_path = sqlite_path
            self.table_name = table_name

            self._conn = sqlite3.connect(self.sqlite_path, check_same_thread=False)
            self._conn.row_factory = sqlite3.Row

            self._conn.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    key   TEXT PRIMARY KEY,
                    value BLOB NOT NULL
                )
                """
            )
            self._conn.commit()

        def _dumps(self, value: Any) -> bytes:
            """Serialize a Python object to orjson-encoded bytes."""
            return orjson.dumps(value)

        def _loads(self, data: bytes) -> Any:
            """Deserialize orjson-encoded bytes back into a Python object."""
            return orjson.loads(data)

        def set(self, key: str | None, value: Any) -> str:
            """
            Set a key-value pair.

            If key is None, generate a new random UUID key and return it.

            In async code, returns a coroutine you must `await`.
            In sync code, returns the key string directly.
            """
            if in_async():
                async def _aset() -> str:
                    async with aiosqlite.connect(self.sqlite_path) as db:
                        db.row_factory = sqlite3.Row
                        payload = self._dumps(value)

                        if key is None:
                            new_key = str(uuid.uuid4())
                            await db.execute(
                                f"INSERT INTO {self.table_name} (key, value) VALUES (?, ?)",
                                (new_key, payload),
                            )
                            await db.commit()
                            return new_key

                        await db.execute(
                            f"""
                            INSERT INTO {self.table_name} (key, value)
                            VALUES (?, ?)
                            ON CONFLICT(key) DO UPDATE SET value=excluded.value
                            """,
                            (str(key), payload),
                        )
                        await db.commit()
                        return str(key)

                return _aset()

            payload = self._dumps(value)
            if key is None:
                new_key = str(uuid.uuid4())
                self._conn.execute(
                    f"INSERT INTO {self.table_name} (key, value) VALUES (?, ?)",
                    (new_key, payload),
                )
                self._conn.commit()
                return new_key

            self._conn.execute(
                f"""
                INSERT INTO {self.table_name} (key, value)
                VALUES (?, ?)
                ON CONFLICT(key) DO UPDATE SET value=excluded.value
                """,
                (str(key), payload),
            )
            self._conn.commit()
            return str(key)

        def get(self, key: str, default: Any = MISSING) -> Any:
            """
            Get the value for a key.

            If the key does not exist:
                - If default is MISSING, raises KeyError.
                - Otherwise returns default.

            In async code, returns a coroutine you must `await`.
            In sync code, returns the value directly.
            """
            if in_async():
                async def _aget() -> Any:
                    async with aiosqlite.connect(self.sqlite_path) as db:
                        db.row_factory = sqlite3.Row
                        cursor = await db.execute(
                            f"SELECT value FROM {self.table_name} WHERE key = ?",
                            (str(key),),
                        )
                        row = await cursor.fetchone()
                        await cursor.close()

                        if row is None:
                            if default is MISSING:
                                raise KeyError(key)
                            return default

                        return self._loads(row["value"])

                return _aget()

            cursor = self._conn.execute(
                f"SELECT value FROM {self.table_name} WHERE key = ?",
                (str(key),),
            )
            row = cursor.fetchone()
            if row is None:
                if default is MISSING:
                    raise KeyError(key)
                return default
            return self._loads(row["value"])

        def remove(self, key: str) -> bool:
            """
            Remove a key-value pair.

            Returns True if a row was deleted, False otherwise.

            In async code, returns a coroutine you must `await`.
            In sync code, returns a bool directly.
            """
            if in_async():
                async def _aremove() -> bool:
                    async with aiosqlite.connect(self.sqlite_path) as db:
                        cursor = await db.execute(
                            f"DELETE FROM {self.table_name} WHERE key = ?",
                            (str(key),),
                        )
                        await db.commit()
                        return cursor.rowcount > 0

                return _aremove()

            cursor = self._conn.execute(
                f"DELETE FROM {self.table_name} WHERE key = ?",
                (str(key),),
            )
            self._conn.commit()
            return cursor.rowcount > 0

        def all(self) -> list[str]:
            """
            Return a list of all keys in the database.

            In async code, returns a coroutine you must `await`.
            In sync code, returns the list directly.
            """
            if in_async():
                async def _aall() -> list[str]:
                    async with aiosqlite.connect(self.sqlite_path) as db:
                        db.row_factory = sqlite3.Row
                        cursor = await db.execute(
                            f"SELECT key FROM {self.table_name} ORDER BY key"
                        )
                        rows = await cursor.fetchall()
                        await cursor.close()
                        return [row["key"] for row in rows]

                return _aall()

            cursor = self._conn.execute(
                f"SELECT key FROM {self.table_name} ORDER BY key"
            )
            return [row["key"] for row in cursor.fetchall()]

        def purge(self) -> bool:
            """
            Remove all key-value pairs from the database.

            Always returns True.

            In async code, returns a coroutine you must `await`.
            In sync code, returns True directly.
            """
            if in_async():
                async def _apurge() -> bool:
                    async with aiosqlite.connect(self.sqlite_path) as db:
                        await db.execute(f"DELETE FROM {self.table_name}")
                        await db.commit()
                        return True

                return _apurge()

            self._conn.execute(f"DELETE FROM {self.table_name}")
            self._conn.commit()
            return True

        def close(self) -> None:
            """
            Close the underlying sync SQLite connection.

            In async code, returns a coroutine you must `await`.
            In sync code, closes immediately.
            """
            if in_async():
                async def _aclose() -> None:
                    self._conn.close()
                return _aclose()

            self._conn.close()


else:
    class PickleDBSQLite:
        """
        This class is only usable if `aiosqlite` is installed, e.g.:
            pip install "pickledb[sqlite]"
        """

        def __init__(self, *args: Any, **kwargs: Any) -> None:
            raise RuntimeError(
                "PickleDBSQLite requires `aiosqlite`. "
                "Install it via `pip install \"pickledb[sqlite]\"`."
            )

