from unittest import TestCase, main
import pickledb

class TestKeyMethods(TestCase):
    def setUp(self):
        self.db = pickledb.load("test.db", False)

    def test_set_string(self):
        self.db.set("key", "string")
        value = self.db.get("key")
        self.assertEqual(value, "string")

    def test_set_int(self):
        self.db.set("key", 1)
        value = self.db.get("key")
        self.assertEqual(value, 1)

    def test_set_double(self):
        self.db.set("key", 1.0)
        value = self.db.get("key")
        self.assertEqual(value, 1.0)

    def test_set_bool(self):
        self.db.set("key", True)
        value = self.db.get("key")
        self.assertEqual(value, True)

    def test_getall(self):
        self.db.set("key1", "value1")
        self.db.set("key2", "value2")
        self.db.set("key3", "value3")
        for k in ["key1", "key2", "key3"]:
            self.assertTrue(k in self.db.getall())

    def test_rem(self):
        self.db.set("key", "value")
        self.db.rem("key")
        self.assertTrue("key" not in self.db.getall())

if __name__ == "__main__":
    main()
