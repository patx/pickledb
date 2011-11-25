from pickledb import pickledb
import unittest
import os
import time
from datetime import datetime

class TestBasicFunctionality(unittest.TestCase):
    def setUp(self):
        while True:
            self.dbf='testdb_%d.json' % int(round(time.time()))
            if not os.path.exists(self.dbf):
                break
            else:
                continue
        self.db = pickledb(self.dbf, False)
        self.teststring = datetime.utcnow()
        self.testinteger = int(round(time.time()))
    
    def tearDown(self):
        if os.path.exists(self.dbf):
            os.remove(self.dbf)
    
    def testSet(self):
        self.assertTrue(self.db.set('var', self.teststring))
    
    def testGet1(self):
        a = self.teststring
        self.db.set('var', a)
        b = self.db.get('var')
        self.assertTrue(a==b)
    
    def testGet2(self):
        self.db.set('var', self.testinteger)
        a = self.db.get('var')
        self.assertTrue(type(a)==type(str()) and a==str(self.testinteger))
    
    def testRemoveString(self):
        a = self.teststring
        self.db.set('var', a)
        b = self.db.get('var')
        self.db.rem('var')
        c = self.db.get('var')
        self.assertTrue(a == b and b != c and c == None)


if __name__ == '__main__':
    unittest.main()