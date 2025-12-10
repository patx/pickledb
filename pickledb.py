"""
pickleDB - https://patx.github.io/pickledb
Harrison Erd - https://harrisonerd.com/
Licensed - BSD 3 Clause (see LICENSE)
"""

import asyncio
import os
import aiofiles
import orjson


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
            return coro
        return asyncio.run(coro)
    return wrapper


class PickleDB:
    """
    A unified async/sync key-value store using orjson + aiofiles.
    """

    def __init__(self, location: str):
        self.location = os.path.expanduser(location)
        self.db = {}
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
        """Load JSON database from disk into memory."""
        if os.path.exists(self.location) and os.path.getsize(self.location) > 0:
            async with aiofiles.open(self.location, "rb") as f:
                data = await f.read()
            new_db = orjson.loads(data)
        else:
            new_db = {}

        async with self._lock:
            self.db = new_db
        return self

    @dualmethod
    async def save(self) -> bool:
        """Atomically save database to disk."""
        temp = f"{self.location}.tmp"
        async with self._lock:
            async with aiofiles.open(temp, "wb") as f:
                await f.write(orjson.dumps(self.db))
            await asyncio.to_thread(os.replace, temp, self.location)
        return True

    @dualmethod
    async def set(self, key, value) -> bool:
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
    async def remove(self, key) -> bool:
        """Remove a key-value pair."""
        async with self._lock:
            return self.db.pop(str(key), None) is not None

    @dualmethod
    async def all(self):
        """Return a list of all keys."""
        async with self._lock:
            return list(self.db.keys())

    @dualmethod
    async def purge(self) -> bool:
        """Remove all key-value pairs from database."""
        async with self._lock:
            self.db.clear()
        return True

