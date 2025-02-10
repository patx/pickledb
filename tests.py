import unittest
import os
import time
import signal
import asyncio
import aiofiles
import orjson

# Adjust the import path if needed. For example, if 'pickledb' is your own module,
# ensure the relative or absolute path matches your project structure.
from pickledb import PickleDB, AsyncPickleDB


class TestPickleDB(unittest.TestCase):
    def setUp(self):
        """Set up a PickleDB instance with a real file."""
        self.test_file = "test_pickledb.json"
        self.db = PickleDB(self.test_file)

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
            num_docs = 1_000_000

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
            self.db.save()
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
        self.db.save()
        reloaded_db = PickleDB(self.test_file)
        self.assertEqual(reloaded_db.get("key1"), "value1")

    def test_invalid_file_loading(self):
        """Test initializing a database with a corrupt file."""
        with open(self.test_file, 'w') as f:
            f.write("corrupt data")
        with self.assertRaises(RuntimeError):
            PickleDB(self.test_file)

    def test_set_non_string_key(self):
        """Test setting a non-string key."""
        self.db.set(123, "value123")
        self.assertEqual(self.db.get("123"), "value123")

    def test_remove_non_string_key(self):
        """Test removing a key that was stored as a non-string key."""
        self.db.set(123, "value123")
        self.assertTrue(self.db.remove(123))
        self.assertIsNone(self.db.get("123"))


class TestAsyncPickleDB(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        """Set up an AsyncPickleDB instance with a real file."""
        self.test_file = "test_async_pickledb.json"
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        self.db = AsyncPickleDB(self.test_file)

    async def asyncTearDown(self):
        """Clean up after async tests by removing the test file."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    async def test_aset_and_aget(self):
        """Test setting and retrieving a key-value pair asynchronously."""
        await self.db.aset("key1", "async_value1")
        value = await self.db.aget("key1")
        self.assertEqual(value, "async_value1")

    async def test_aget_nonexistent_key(self):
        """Test retrieving a key that does not exist asynchronously."""
        value = await self.db.aget("nonexistent")
        self.assertIsNone(value)

    async def test_aremove_key(self):
        """Test removing a key-value pair asynchronously."""
        await self.db.aset("key1", "to_remove")
        removed = await self.db.aremove("key1")
        self.assertTrue(removed)
        value = await self.db.aget("key1")
        self.assertIsNone(value)

    async def test_aremove_nonexistent_key(self):
        """Test removing a key that does not exist asynchronously."""
        removed = await self.db.aremove("nonexistent")
        self.assertFalse(removed)

    async def test_apurge(self):
        """Test purging all keys asynchronously."""
        await self.db.aset("key1", "val1")
        await self.db.aset("key2", "val2")
        await self.db.apurge()
        keys = await self.db.aall()
        self.assertEqual(keys, [])

    async def test_aall_keys(self):
        """Test retrieving all keys asynchronously."""
        await self.db.aset("keyA", "valA")
        await self.db.aset("keyB", "valB")
        keys = await self.db.aall()
        self.assertListEqual(sorted(keys), ["keyA", "keyB"])

    async def test_asave_and_reload(self):
        """
        Test dumping (asave) the async database to disk and reloading it
        by creating a new AsyncPickleDB instance.
        """
        await self.db.aset("async_key", "async_val")
        await self.db.asave()

        # Create a new AsyncPickleDB instance to verify persistence,
        # then use its inherited synchronous `get` method.
        new_db = AsyncPickleDB(self.test_file)
        self.assertEqual(new_db.get("async_key"), "async_val")

    async def test_aset_non_string_key(self):
        """Test setting a non-string key asynchronously."""
        await self.db.aset(123, "val123")
        value = await self.db.aget("123")
        self.assertEqual(value, "val123")

    async def test_concurrent_access(self):
        """Test concurrent async set operations under the lock."""
        async def set_values(db, start, end):
            for i in range(start, end):
                await db.aset(f"key{i}", f"value{i}")

        # Run two coroutines concurrently
        await asyncio.gather(
            set_values(self.db, 0, 50),
            set_values(self.db, 50, 100)
        )

        # Verify data integrity
        for i in range(100):
            val = await self.db.aget(f"key{i}")
            self.assertEqual(val, f"value{i}")


if __name__ == "__main__":
    unittest.main()
