import unittest
import os
import time
import signal
from pickledb import PickleDB  # Adjust the import path if needed


class TestPickleDB(unittest.TestCase):
    def setUp(self):
        """Set up a PickleDB instance with a real file."""
        self.test_file = "test_pickledb.json"
        self.db = PickleDB(self.test_file, auto_dump=False)

    def tearDown(self):
        """Clean up after tests."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def _timeout_handler(self, signum, frame):
        """Handle timeouts for stress tests."""
        raise TimeoutError("Test exceeded the timeout duration")

    # Original Stress Test
    def test_stress_operation(self):
        """Stress test: Insert and retrieve a large number of key-value pairs, then dump."""
        timeout_duration = 600  # Timeout in seconds (10 minutes)

        # Set a signal-based timeout
        signal.signal(signal.SIGALRM, self._timeout_handler)
        signal.alarm(timeout_duration)

        try:
            num_docs = 20_000_000

            # Measure memory loading time
            start_time = time.time()
            for i in range(num_docs):
                self.db.set(f"key{i}", f"value{i}")
            mem_time = time.time()
            mem_duration = mem_time - start_time
            print(f"\n{num_docs} stored in memory in {mem_duration:.2f} seconds")

            # Measure retrieval performance before dumping
            start_time = time.time()
            retrieved_docs = [self.db.get(f"key{i}") for i in range(num_docs)]
            retrieval_time = time.time() - start_time
            print(f"Retrieved {num_docs} key-value pairs in {retrieval_time:.2f} seconds")

            # Measure dump performance
            start_time = time.time()
            self.db.dump()
            dump_time = time.time() - start_time
            print(f"Dumped {num_docs} key-value pairs to disk in {dump_time:.2f} seconds")

        finally:
            signal.alarm(0)  # Cancel the alarm after the test

    # Functional Tests
    def test_set_and_get(self):
        """Test setting and retrieving a key-value pair."""
        self.db.set("key1", "value1")
        self.assertEqual(self.db.get("key1"), "value1")

    def test_get_nonexistent_key(self):
        """Test retrieving a key that does not exist."""
        self.assertIsNone(self.db.get("nonexistent"))

    def test_remove_key(self):
        """Test removing a key-value pair."""
        self.db.set("key1", "value1")
        self.assertTrue(self.db.remove("key1"))
        self.assertIsNone(self.db.get("key1"))

    def test_remove_nonexistent_key(self):
        """Test removing a key that does not exist."""
        self.assertFalse(self.db.remove("nonexistent"))

    def test_purge(self):
        """Test purging all keys and values."""
        self.db.set("key1", "value1")
        self.db.set("key2", "value2")
        self.db.purge()
        self.assertEqual(self.db.all(), [])

    def test_all_keys(self):
        """Test retrieving all keys."""
        self.db.set("key1", "value1")
        self.db.set("key2", "value2")
        self.assertListEqual(sorted(self.db.all()), ["key1", "key2"])

    def test_dump_and_reload(self):
        """Test dumping the database to disk and reloading it."""
        self.db.set("key1", "value1")
        self.db.dump()
        reloaded_db = PickleDB(self.test_file, auto_dump=False)
        self.assertEqual(reloaded_db.get("key1"), "value1")

    def test_invalid_file_loading(self):
        """Test initializing a database with a corrupt file."""
        with open(self.test_file, 'w') as f:
            f.write("corrupt data")
        db = PickleDB(self.test_file, auto_dump=False)
        self.assertEqual(db.all(), [])

    def test_auto_dump(self):
        """Test the auto-dump functionality."""
        db = PickleDB(self.test_file, auto_dump=True)
        db.set("key1", "value1")
        reloaded_db = PickleDB(self.test_file, auto_dump=False)
        self.assertEqual(reloaded_db.get("key1"), "value1")

    def test_set_non_string_key(self):
        """Test setting a non-string key."""
        self.db.set(123, "value123")
        self.assertEqual(self.db.get("123"), "value123")

    def test_remove_non_string_key(self):
        """Test removing a key that was stored as a non-string key."""
        self.db.set(123, "value123")
        self.assertTrue(self.db.remove(123))
        self.assertIsNone(self.db.get("123"))


if __name__ == "__main__":
    unittest.main()

