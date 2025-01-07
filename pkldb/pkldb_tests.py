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

    def test_retrieve_before_dump(self):
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
            print(f"{num_docs} stored in memory in {mem_duration:.2f} seconds")

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

if __name__ == "__main__":
    unittest.main()

