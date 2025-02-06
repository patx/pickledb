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

import os
import aiofiles
import orjson


class AsyncPickleDB:
    """
    A barebones orjson-based key-value store with essential methods:
    set, get, save, remove, purge, and all.
    """

    def __init__(self, location):
        """
        Initialize the PickleDB object.

        Args:
            location (str): Path to the JSON file.
        """
        self.location = os.path.expanduser(location)

    async def __setitem__(self, key, value):
        """
        Wraps the `set` method to allow `db[key] = value`. See `set`
        method for details.
        """
        return await self.set(key, value)

    async def __getitem__(self, key):
        """
        Wraps the `get` method to allow `value = db[key]`. See `get`
        method for details.
        """
        return await self.get(key)

    async def save(self, entry, option=0):
        """
        Save an entry to the file using JSON Lines format.

        Args:
            entry (dict): The entry to save.
            options (int): `orjson.OPT_*` flags to configure
                           serialization behavior.

        Returns:
            bool: True if save was successful, False if not.
        """
        try:
            async with aiofiles.open(self.location, "ab") as f:
                await f.write(orjson.dumps(entry, option=option) + b'\n')
            return True
        except Exception as e:
            print(f"Failed to save entry: {e}")
            return False

    async def set(self, key, value):
        """
        Add or update a key-value pair in the database.

        Args:
            key (any): The key to set. If the key is not a string, it
                       will be converted to a string.
            value (any): The value to associate with the key.

        Returns:
            bool: True if the operation succeeds.
        """
        key = str(key) if not isinstance(key, str) else key
        await self.save({key: value})
        return True

    async def remove(self, key):
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
        await self.save({"__remove__": key})
        return True

    async def purge(self):
        """
        Clear all keys from the database.

        Returns:
            bool: True if the operation succeeds.
        """
        try:
            async with aiofiles.open(self.location, "w") as f:
                await f.write("")
            return True
        except Exception as e:
            print(f"Failed to purge database: {e}")
            return False

    async def get(self, key):
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
        if os.path.exists(self.location) and os.path.getsize(self.location) > 0:
            try:
                async with aiofiles.open(self.location, "rb") as f:
                    async for line in f:
                        entry = orjson.loads(line)
                        if key in entry:
                            return entry[key]
                        elif "__remove__" in entry and entry["__remove__"] == key:
                            return None
            except Exception as e:
                print(f"Failed to get key: {e}")
        return None

    async def all(self):
        """
        Get a list of all keys in the database.

        Returns:
            list: A list of all keys.
        """
        keys = []
        if os.path.exists(self.location) and os.path.getsize(self.location) > 0:
            try:
                async with aiofiles.open(self.location, "rb") as f:
                    async for line in f:
                        entry = orjson.loads(line)
                        if "__remove__" in entry:
                            keys.remove(entry["__remove__"])
                        else:
                            keys.extend(entry.keys())
            except Exception as e:
                print(f"Failed to get all keys: {e}")
        return keys
