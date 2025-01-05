
import time
import unittest
import signal
from pkldb import pkldb  # Adjust the import path if needed
import tempfile
import os

class TestPkldbLargeDataset(unittest.TestCase):
    def setUp(self):
        """Set up a temporary pkldb instance for testing."""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.db = pkldb(self.temp_file.name, auto_dump=False)

    def tearDown(self):
        """Clean up after tests."""
        if hasattr(self.db, "close"):
            self.db.close()
        if os.path.exists(self.temp_file.name):
            os.remove(self.temp_file.name)

    def _timeout_handler(self, signum, frame):
        raise TimeoutError("Test exceeded the timeout duration")

    def test_large_dataset_with_timeout(self):
        """Stress test: Insert and retrieve a large number of key-value pairs with a timeout."""
        timeout_duration = 250  # Timeout in seconds (4 minutes)

        # Set a signal-based timeout
        signal.signal(signal.SIGALRM, self._timeout_handler)
        signal.alarm(timeout_duration)

        try:
            num_docs = 10_000_000

            # Measure insertion performance
            start_time = time.time()
            for i in range(num_docs):
                self.db.set(f"key{i}", {"key": f"value{i}"})
            self.db.dump()  # Final dump
            end_time = time.time()
            insertion_duration = end_time - start_time

            self.assertLess(insertion_duration, 250, "Inserting a bunch of key-value pairs took too long")
            print(f"Inserted {num_docs} key-value pairs in {insertion_duration:.2f} seconds")

            # Measure retrieval performance
            start_time = time.time()
            retrieved_docs = [self.db.get(f"key{i}") for i in range(num_docs)]
            end_time = time.time()
            retrieval_duration = end_time - start_time

            self.assertEqual(len(retrieved_docs), num_docs, "Not all key-value pairs were retrieved")
            for i in range(num_docs):
                self.assertEqual(retrieved_docs[i], {"key": f"value{i}"}, f"Mismatch at key{i}")
            print(f"Retrieved {num_docs} key-value pairs in {retrieval_duration:.2f} seconds")
        finally:
            signal.alarm(0)  # Cancel the alarm after the test

if __name__ == "__main__":
    unittest.main()
