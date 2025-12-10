import asyncio
import os
import aiofiles
import orjson
from typing import Any


def in_async():
    """Check if running in an event loop."""
    try:
        asyncio.get_running_loop()
        return True
    except RuntimeError:
        return False


def dualmethod(func):
    """Allows async methods to also be called synchronously."""
    def wrapper(self, *args, **kwargs):
        coro = func(self, *args, **kwargs)
        if in_async():
            # In an async context: return coroutine for 'await'
            return coro
        # In sync context: run it to completion and return result
        return asyncio.run(coro)
    return wrapper


class PickleDB:
    """
    A unified async/sync key-value store using orjson + aiofiles.
    """

    def __init__(self, location: str):
        self.location = os.path.expanduser(location)
        self.db: dict[str, Any] = {}
        self._lock = asyncio.Lock()

    async def _load(self):
        """Pure async loader used by both sync and async entrypoints."""
        if os.path.exists(self.location) and os.path.getsize(self.location) > 0:
            async with aiofiles.open(self.location, "rb") as f:
                data = await f.read()
            self.db = orjson.loads(data)
        else:
            self.db = {}

    async def _save(self):
        """Pure async saver used by both sync and async entrypoints."""
        temp = f"{self.location}.tmp"
        async with self._lock:
            async with aiofiles.open(temp, "wb") as f:
                await f.write(orjson.dumps(self.db))
            await asyncio.to_thread(os.replace, temp, self.location)
        return True

    def __enter__(self):
        # Call the *internal* async method, not the dualmethod wrapper
        asyncio.run(self._load())
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            asyncio.run(self._save())

    async def __aenter__(self):
        await self._load()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            await self._save()

    @dualmethod
    async def load(self):
        """Load JSON database from disk."""
        await self._load()

    @dualmethod
    async def save(self):
        """Atomically save database to disk."""
        return await self._save()

    @dualmethod
    async def set(self, key, value):
        """Set a key-value pair."""
        async with self._lock:
            self.db[str(key)] = value
        return True

    @dualmethod
    async def get(self, key, default=None):
        """Get a key's value."""
        async with self._lock:
            return self.db.get(str(key), default)

    @dualmethod
    async def remove(self, key):
        """Remove a key-value pair."""
        async with self._lock:
            return self.db.pop(str(key), None) is not None

    @dualmethod
    async def all(self):
        """Return a list of all keys."""
        async with self._lock:
            return list(self.db.keys())

    @dualmethod
    async def purge(self):
        """Remove all key-value pairs from database."""
        async with self._lock:
            self.db.clear()
        return True

