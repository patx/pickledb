
import os
import sys
import signal
import shutil
import json
import gzip
from tempfile import NamedTemporaryFile
from threading import RLock
from time import time

def load(location, auto_dump=True, enable_ttl=False):
    """
    Create and return a PickleDB object.

    Args:
        location (str): Path to the JSON file.
        auto_dump (bool): If True, automatically save changes to the file.
        enable_ttl (bool): If True, enable time-to-live (TTL) support for keys.

    Returns:
        PickleDB: The initialized PickleDB object.
    """
    return PickleDB(location, auto_dump, enable_ttl)


class PickleDB:
    """
    A lightweight, file-based key-value store with optional TTL support.
    """

    def __init__(self, location, auto_dump=True, enable_ttl=False):
        """
        Initialize the PickleDB object.

        Args:
            location (str): Path to the JSON file.
            auto_dump (bool): Automatically save changes to the file.
            enable_ttl (bool): Enable TTL support for keys.
        """
        self.location = os.path.expanduser(location)
        self.auto_dump = auto_dump
        self.enable_ttl = enable_ttl
        self._lock = RLock()
        self.db = {}
        self.ttl = {}
        self._load()
        self._set_signal_handler()

    def __getitem__(self, item):
        '''Syntax sugar for get()'''
        return self.get(item)

    def __setitem__(self, key, value):
        '''Sytax sugar for set()'''
        return self.set(key, value)

    def __delitem__(self, key):
        '''Sytax sugar for rem()'''
        return self.rem(key)

    def _set_signal_handler(self):
        """Set up signal handler for graceful shutdown."""
        signal.signal(signal.SIGTERM, self._graceful_exit)

    def _graceful_exit(self, *args):
        """Ensure any ongoing dump completes before exiting."""
        self.dump()
        sys.exit(0)

    def _load(self):
        """Load data from the JSON file."""
        if os.path.exists(self.location):
            try:
                with open(self.location, 'rt') as f:
                    self.db = json.load(f)
            except (ValueError, json.JSONDecodeError):
                self.db = {}
        else:
            self.db = {}

    def _dump(self):
        """Dump the database to a temporary file and replace the original."""
        with NamedTemporaryFile(mode='wt', delete=False) as temp_file:
            json.dump(self.db, temp_file)
        shutil.move(temp_file.name, self.location)

    def dump(self):
        """Force save the database to the file."""
        with self._lock:
            self._dump()

    def _autodump(self):
        """Automatically dump the database if auto_dump is enabled."""
        if self.auto_dump:
            self.dump()

    def set(self, key, value, ttl=None):
        """
        Set a key-value pair in the database.

        Args:
            key (str): The key to set.
            value (any): The value to associate with the key.
            ttl (int, optional): Time-to-live in seconds. Defaults to None.

        Returns:
            bool: True if the operation succeeds.
        """
        if not isinstance(key, str):
            raise TypeError("Key must be a string.")
        with self._lock:
            self.db[key] = value
            if ttl and self.enable_ttl:
                self.ttl[key] = time() + ttl
            self._autodump()
        return True

    def get(self, key):
        """
        Get the value associated with a key.

        Args:
            key (str): The key to retrieve.

        Returns:
            any: The value associated with the key, or None if the key does not exist or has expired.
        """
        with self._lock:
            if self.enable_ttl and key in self.ttl:
                if time() > self.ttl[key]:
                    self.rem(key)
                    return None
            return self.db.get(key)

    def exists(self, key):
        """
        Check if a key exists in the database.

        Args:
            key (str): The key to check.

        Returns:
            bool: True if the key exists, False otherwise.
        """
        return key in self.db

    def rem(self, key):
        """
        Remove a key from the database.

        Args:
            key (str): The key to remove.

        Returns:
            bool: True if the key was removed, False if it did not exist.
        """
        with self._lock:
            if key in self.db:
                del self.db[key]
                if key in self.ttl:
                    del self.ttl[key]
                self._autodump()
                return True
        return False

    def getall(self):
        """
        Retrieve all keys in the database.

        Returns:
            list: A list of all keys in the database.
        """
        return list(self.db.keys())

    def clear(self):
        """
        Remove all keys from the database.

        Returns:
            bool: True if the operation succeeds.
        """
        with self._lock:
            self.db.clear()
            self.ttl.clear()
            self._autodump()
        return True

    def deldb(self):
        """
        Delete the entire database.

        Returns:
            bool: True if the operation succeeds.
        """
        with self._lock:
            self.db = {}
            self.ttl = {}
            if os.path.exists(self.location):
                os.remove(self.location)
        return True

    def compress(self):
        """
        Compress the database file using gzip.

        Returns:
            bool: True if the operation succeeds.
        """
        with self._lock:
            compressed_file = f"{self.location}.gz"
            with open(self.location, 'rb') as f_in:
                with gzip.open(compressed_file, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
        return True

    def append(self, key, value):
        """
        Append a value to an existing list.

        Args:
            key (str): The key of the list.
            value (any): The value to append.

        Returns:
            bool: True if the operation succeeds.
        """
        with self._lock:
            if key not in self.db or not isinstance(self.db[key], list):
                raise TypeError("Key must reference a list.")
            self.db[key].append(value)
            self._autodump()
        return True

    def lcreate(self, name):
        """
        Create a new list in the database.

        Args:
            name (str): The name of the list.

        Returns:
            bool: True if the operation succeeds.
        """
        if not isinstance(name, str):
            raise TypeError("List name must be a string.")
        with self._lock:
            if name in self.db:
                raise ValueError("List already exists.")
            self.db[name] = []
            self._autodump()
        return True

    def ladd(self, name, value):
        """
        Add a value to an existing list.

        Args:
            name (str): The name of the list.
            value (any): The value to add.

        Returns:
            bool: True if the operation succeeds.
        """
        with self._lock:
            if name not in self.db or not isinstance(self.db[name], list):
                raise TypeError("List does not exist or is not a valid list.")
            self.db[name].append(value)
            self._autodump()
        return True

    def lgetall(self, name):
        """
        Retrieve all values from a list.

        Args:
            name (str): The name of the list.

        Returns:
            list: All values in the list.
        """
        with self._lock:
            if name not in self.db or not isinstance(self.db[name], list):
                raise TypeError("List does not exist or is not a valid list.")
            return self.db[name]

    def lsort(self, name, reverse=False):
        """
        Sort a list in the database.

        Args:
            name (str): The name of the list.
            reverse (bool): Sort in descending order if True.

        Returns:
            list: The sorted list.
        """
        with self._lock:
            if name not in self.db or not isinstance(self.db[name], list):
                raise TypeError("List does not exist or is not a valid list.")
            self.db[name].sort(reverse=reverse)
            self._autodump()
            return self.db[name]

    def lremove(self, name, value):
        """
        Remove a value from a list.

        Args:
            name (str): The name of the list.
            value (any): The value to remove.

        Returns:
            bool: True if the value was removed, False otherwise.
        """
        with self._lock:
            if name not in self.db or not isinstance(self.db[name], list):
                raise TypeError("List does not exist or is not a valid list.")
            try:
                self.db[name].remove(value)
                self._autodump()
                return True
            except ValueError:
                return False

    def lgetrange(self, name, start, end):
        """
        Get a range of values from a list.

        Args:
            name (str): The name of the list.
            start (int): The starting index.
            end (int): The ending index.

        Returns:
            list: The sublist from start to end.
        """
        with self._lock:
            if name not in self.db or not isinstance(self.db[name], list):
                raise TypeError("List does not exist or is not a valid list.")
            return self.db[name][start:end]

    def llen(self, name):
        """
        Get the length of a list.

        Args:
            name (str): The name of the list.

        Returns:
            int: The length of the list.
        """
        with self._lock:
            if name not in self.db or not isinstance(self.db[name], list):
                raise TypeError("List does not exist or is not a valid list.")
            return len(self.db[name])

    def dcreate(self, name):
        """
        Create a new dictionary in the database.

        Args:
            name (str): The name of the dictionary.

        Returns:
            bool: True if the operation succeeds.
        """
        if not isinstance(name, str):
            raise TypeError("Dictionary name must be a string.")
        with self._lock:
            if name in self.db:
                raise ValueError("Dictionary already exists.")
            self.db[name] = {}
            self._autodump()
        return True

    def dadd(self, name, key, value):
        """
        Add a key-value pair to a dictionary.

        Args:
            name (str): The name of the dictionary.
            key (str): The key to add.
            value (any): The value to associate with the key.

        Returns:
            bool: True if the operation succeeds.
        """
        if not isinstance(key, str):
            raise TypeError("Key must be a string.")
        with self._lock:
            if name not in self.db or not isinstance(self.db[name], dict):
                raise TypeError("Dictionary does not exist or is not a valid dictionary.")
            self.db[name][key] = value
            self._autodump()
        return True

    def dget(self, name, key):
        """
        Retrieve a value from a dictionary.

        Args:
            name (str): The name of the dictionary.
            key (str): The key to retrieve.

        Returns:
            any: The value associated with the key.
        """
        with self._lock:
            if name not in self.db or not isinstance(self.db[name], dict):
                raise TypeError("Dictionary does not exist or is not a valid dictionary.")
            return self.db[name].get(key)

    def dgetall(self, name):
        """
        Retrieve all key-value pairs from a dictionary.

        Args:
            name (str): The name of the dictionary.

        Returns:
            dict: All key-value pairs in the dictionary.
        """
        with self._lock:
            if name not in self.db or not isinstance(self.db[name], dict):
                raise TypeError("Dictionary does not exist or is not a valid dictionary.")
            return self.db[name]

    def dremove(self, name, key):
        """
        Remove a key from a dictionary.

        Args:
            name (str): The name of the dictionary.
            key (str): The key to remove.

        Returns:
            bool: True if the key was removed, False otherwise.
        """
        with self._lock:
            if name not in self.db or not isinstance(self.db[name], dict):
                raise TypeError("Dictionary does not exist or is not a valid dictionary.")
            if key in self.db[name]:
                del self.db[name][key]
                self._autodump()
                return True
            return False

    def dmerge(self, name, other_dict):
        """
        Merge another dictionary into an existing dictionary.

        Args:
            name (str): The name of the dictionary.
            other_dict (dict): The dictionary to merge.

        Returns:
            dict: The updated dictionary.
        """
        with self._lock:
            if name not in self.db or not isinstance(self.db[name], dict):
                raise TypeError("Dictionary does not exist or is not a valid dictionary.")
            if not isinstance(other_dict, dict):
                raise TypeError("Argument must be a dictionary.")
            self.db[name].update(other_dict)
            self._autodump()
            return self.db[name]

    def dkeys(self, name):
        """
        Get all keys from a dictionary.

        Args:
            name (str): The name of the dictionary.

        Returns:
            list: A list of keys in the dictionary.
        """
        with self._lock:
            if name not in self.db or not isinstance(self.db[name], dict):
                raise TypeError("Dictionary does not exist or is not a valid dictionary.")
            return list(self.db[name].keys())

    def dvalues(self, name):
        """
        Get all values from a dictionary.

        Args:
            name (str): The name of the dictionary.

        Returns:
            list: A list of values in the dictionary.
        """
        with self._lock:
            if name not in self.db or not isinstance(self.db[name], dict):
                raise TypeError("Dictionary does not exist or is not a valid dictionary.")
            return list(self.db[name].values())
