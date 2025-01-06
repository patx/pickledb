import os
import orjson
import multiprocessing

class pkldb:
    """
    A orjson-based key-value store with essential methods: set, get, dump, delete, purge, and all.
    """
    def __init__(self, location, auto_dump=False):
        """
        Initialize the pkldb object.

        Args:
            location (str): Path to the JSON file.
            auto_dump (bool): Automatically save changes to the file.
        """
        self.location = os.path.expanduser(location)
        self.auto_dump = auto_dump
        self._load()

    def _load(self):
        """
        Load data from the JSON file if it exists, or initialize an empty database.
        """
        if os.path.exists(self.location) and os.path.getsize(self.location) > 0:
            try:
                with open(self.location, 'rb') as f:
                    self.db = orjson.loads(f.read())
            except (ValueError, IOError):
                self.db = {}
        else:
            self.db = {}

    def _dump_process(self, data, location):
        """
        Helper method to perform the dump operation in a separate process.
        """
        temp_location = f"{location}.tmp"
        try:
            with open(temp_location, 'wb') as temp_file:
                temp_file.write(orjson.dumps(data))
            os.replace(temp_location, location)  # Atomic replacement
        except IOError as e:
            print(f"Failed to dump database: {e}")

    def dump(self):
        """
        Save the database to the file atomically in a separate process.
        """
        process = multiprocessing.Process(target=self._dump_process, args=(self.db, self.location))
        process.start()
        process.join()

    def set(self, key, value):
        """
        Set a key-value pair in the database.

        Args:
            key (any): The key to set (converted to a string).
            value (any): The value to associate with the key.

        Returns:
            bool: True if the operation succeeds.
        """
        self.db[str(key)] = value
        if self.auto_dump:
            self.dump()
        return True

    def get(self, key):
        """
        Get the value associated with a key.

        Args:
            key (any): The key to retrieve.

        Returns:
            any: The value associated with the key, or None if the key does not exist.
        """
        return self.db.get(str(key))

    def remove(self, key):
        """
        Remove a key and its value from the database.

        Args:
            key (any): The key to delete.

        Returns:
            bool: True if the key was deleted, False if the key does not exist.
        """
        if str(key) in self.db:
            del self.db[str(key)]
            if self.auto_dump:
                self.dump()
            return True
        return False

    def purge(self):
        """
        Clear all keys from the database.

        Returns:
            bool: True if the operation succeeds.
        """
        self.db.clear()
        if self.auto_dump:
            self.dump()
        return True

    def all(self):
        """
        Get a list of all keys in the database.

        Returns:
            list: A list of all keys.
        """
        return list(self.db.keys())

