import unittest
import os
import time
from pickledb import load

class TestPickleDB(unittest.TestCase):

    def setUp(self):
        self.db_file = "test_db.json"
        self.db = load(self.db_file, auto_dump=True, enable_ttl=True)

    def tearDown(self):
        if os.path.exists(self.db_file):
            os.remove(self.db_file)
        if os.path.exists(f"{self.db_file}.gz"):
            os.remove(f"{self.db_file}.gz")

    # Basic Key-Value Operations
    def test_set_and_get(self):
        self.db.set("key1", "value1")
        self.assertEqual(self.db.get("key1"), "value1")

    def test_exists(self):
        self.db.set("key2", "value2")
        self.assertTrue(self.db.exists("key2"))
        self.assertFalse(self.db.exists("key3"))

    def test_rem(self):
        self.db.set("key3", "value3")
        self.assertTrue(self.db.rem("key3"))
        self.assertFalse(self.db.exists("key3"))

    def test_getall(self):
        self.db.set("key1", "value1")
        self.db.set("key2", "value2")
        self.assertCountEqual(self.db.getall(), ["key1", "key2"])

    def test_clear(self):
        self.db.set("key1", "value1")
        self.db.set("key2", "value2")
        self.db.clear()
        self.assertEqual(len(self.db.getall()), 0)

    def test_deldb(self):
        self.db.set("key1", "value1")
        self.db.deldb()
        self.assertFalse(os.path.exists(self.db_file))

    # TTL Functionality
    def test_ttl_expiry(self):
        self.db.set("key1", "value1", ttl=1)
        time.sleep(2)
        self.assertIsNone(self.db.get("key1"))

    # List Operations
    def test_lcreate_and_ladd(self):
        self.db.lcreate("mylist")
        self.db.ladd("mylist", "item1")
        self.db.ladd("mylist", "item2")
        self.assertEqual(self.db.lgetall("mylist"), ["item1", "item2"])

    def test_ladd_to_non_list(self):
        self.db.set("key1", "value1")
        with self.assertRaises(TypeError):
            self.db.ladd("key1", "item1")

    # Dictionary Operations
    def test_dcreate_and_dadd(self):
        self.db.dcreate("mydict")
        self.db.dadd("mydict", "key1", "value1")
        self.db.dadd("mydict", "key2", "value2")
        self.assertEqual(self.db.dget("mydict", "key1"), "value1")

    def test_dadd_to_non_dict(self):
        self.db.set("key1", "value1")
        with self.assertRaises(TypeError):
            self.db.dadd("key1", "key2", "value2")

    def test_dgetall(self):
        self.db.dcreate("mydict")
        self.db.dadd("mydict", "key1", "value1")
        self.db.dadd("mydict", "key2", "value2")
        self.assertEqual(self.db.dgetall("mydict"), {"key1": "value1", "key2": "value2"})

    # File Compression
    def test_compress(self):
        self.db.set("key1", "value1")
        self.assertTrue(self.db.compress())
        self.assertTrue(os.path.exists(f"{self.db_file}.gz"))

    # Error Handling
    def test_set_invalid_key(self):
        with self.assertRaises(TypeError):
            self.db.set(123, "value1")

    def test_get_nonexistent_key(self):
        self.assertIsNone(self.db.get("nonexistent"))

    def test_rem_nonexistent_key(self):
        self.assertFalse(self.db.rem("nonexistent"))

    def test_ladd_to_nonexistent_list(self):
        with self.assertRaises(TypeError):
            self.db.ladd("nonexistent_list", "value")

    def test_dadd_to_nonexistent_dict(self):
        with self.assertRaises(TypeError):
            self.db.dadd("nonexistent_dict", "key", "value")

if __name__ == "__main__":
    unittest.main()

