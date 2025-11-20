"""
Copyright Harrison Erd

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

1. Redistributions of source code must retain the above copyright
notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright
notice, this list of conditions and the following disclaimer in the
documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
contributors may be used to endorse or promote products derived from
this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
import asyncio
import os
import aiofiles
import orjson

class ModifiedFlagImpl:
    __slots__ = ('_dirty',)
    def __init__(self):
        self._dirty = False

    def get_modified(self):
        return self._dirty

    def set_modified(self):
        self._dirty = True
        return self._dirty

    def clear_modified(self):
        self._dirty = False
        return self._dirty

class PickleDB(ModifiedFlagImpl):
    """
    A barebones orjson-based key-value store with essential methods:
    set, get, save, remove, purge, and all.
    """
    __slots__ = ('location','db')
    def __init__(self, location):
        """
        Initialize the PickleDB object.

        Args:
            location (str): Path to the JSON file.
        """
        super(PickleDB,self).__init__()
        self.location = os.path.expanduser(location)
        self._load() #defines .db


    def __setitem__(self, key, value):
        """
        Wraps the `set` method to allow `db[key] = value`. See `set`
        method for details.
        """
        self.set_modified()
        return self.set(key, value)

    def __getitem__(self, key):
        """
        Wraps the `get` method to allow `value = db[key]`. See `get`
        method for details.
        """
        return self.get(key)

    def __enter__(self):
        """
        Enter the context manager.
        Does nothing but return `self` for modifications.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the context manager.
        Automatically saves changes if no exception occurred.
        """
        if exc_type is None:
            self.save()
        return False

    def _load(self):
        """
        Load data from the JSON file if it exists, or initialize an empty
        database.
        """
        if (os.path.exists(self.location) and
                os.path.getsize(self.location) > 0):
            try:
                with open(self.location, "rb") as f:
                    self.db = orjson.loads(f.read())
            except Exception as e:
                raise RuntimeError(f"{e}\nFailed to load database.")
        else:
            self.db = {}
        self.clear_modified()
        return

    def save(self, option=0):
        """
        Save the database to the file using an atomic save.

        Args:
            options (int): `orjson.OPT_*` flags to configure
                           serialization behavior.

        Behavior:
            - Writes to a temporary file and replaces the
              original file only after the write is successful,
              ensuring data integrity.

        Returns:
            bool: True if save was successful, False if not.
        """
        temp_location = f"{self.location}.tmp"
        try:
            with open(temp_location, "wb") as temp_file:
                temp_file.write(orjson.dumps(self.db, option=option))
            os.replace(temp_location, self.location)
            self.clear_modified()
            return True
        except Exception as e:
            print(f"Failed to save database: {e}")
            return False

    def set(self, key, value):
        """
        Add or update a key-value pair in the database.

        Args:
            key (any): The key to set. If the key is not a string, it
                       will be converted to a string.
            value (any): The value to associate with the key.

        Behavior:
            - If the key already exists, its value will be updated.
            - If the key does not exist, it will be added to the
              database.

        Returns:
            bool: True if the operation succeeds.
        """
        key = str(key) if not isinstance(key, str) else key
        self.db[key] = value
        self.set_modified()
        return True

    def remove(self, key):
        """
        Remove a key and its value from the database.

        Args:
            key (any): The key to delete. If the key is not a string,
                       it will be converted to a string.

        Returns:
            bool: True if the key was deleted, False if the key does
                  not exist.
        """
        key = str(key) if not isinstance(key, str) else key
        if key in self.db:
            del self.db[key]
            self.set_modified()
            return True
        return False

    def purge(self):
        """
        Clear all keys from the database.

        Returns:
            bool: True if the operation succeeds.
        """
        self.db.clear()
        self.set_modified()
        return True

    def get(self, key):
        """
        Get the value associated with a key.

        Args:
            key (any): The key to retrieve. If the key is not a
                       string, it will be converted to a string.

        Returns:
            any: The value associated with the key, or None if the
            key does not exist.
        """
        key = str(key) if not isinstance(key, str) else key
        return self.db.get(key)

    def all(self):
        """
        Get a list of all keys in the database.

        Returns:
            list: A list of all keys.
        """
        return list(self.db.keys())


class AsyncPickleDB(ModifiedFlagImpl):
    """
    A fully asynchronous orjson-based key-value store.
    Provides async load, save, and CRUD operations with file locking.
    """
    __slots__ = ('_lock','location', 'db')
    def __init__(self, location):
        super(AsyncPickleDB,self).__init__()
        self.location = os.path.expanduser(location)
        self._lock = asyncio.Lock()
        self.db = {}

    async def __aenter__(self):
        await self.aload()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            await self.asave()
        return False  # Do not suppress exceptions

    async def aload(self):
        """
        Load data from the JSON file if it exists.
        """
        if os.path.exists(self.location) and os.path.getsize(self.location) > 0:
            try:
                async with aiofiles.open(self.location, "rb") as f:
                    content = await f.read()
                self.db = orjson.loads(content)
                self.clear_modified()
            except Exception as e:
                raise RuntimeError(f"{e}\nFailed to load database.")
        else:
            self.db = {}

    async def asave(self, option=0):
        """
        Save the database to file atomically.
        """
        temp_location = f"{self.location}.tmp"
        async with self._lock:
            try:
                async with aiofiles.open(temp_location, "wb") as temp_file:
                    await temp_file.write(orjson.dumps(self.db, option=option))
                await asyncio.to_thread(os.replace, temp_location, self.location)
                self.clear_modified()
                return True
            except Exception as e:
                print(f"Failed to save database: {e}")
                return False

    async def aset(self, key, value):
        async with self._lock:
            self.db[str(key)] = value
            self.set_modified()
            return True

    async def aget(self, key):
        async with self._lock:
            return self.db.get(str(key))

    async def aremove(self, key):
        async with self._lock:
            self.set_modified()
            return self.db.pop(str(key), None) is not None

    async def aall(self):
        async with self._lock:
            return list(self.db.keys())

    async def apurge(self):
        async with self._lock:
            self.set_modified()
            self.db.clear()
            return True
