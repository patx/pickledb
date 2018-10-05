import pickledb

# a work in progress

class TestClass(object):

    db = pickledb.load('tests.db', False)

    def test_load(self):
        x = pickledb.load('x.db', False)
        assert x is not None

    def test_set(self):
        self.db.set('key', 'value')
        x = self.db.get('key')
        assert x == 'value'

    def test_getall(self):
        self.db.deldb()
        self.db.set('key1', 'value1')
        self.db.set('key2', 'value2')
        self.db.dcreate('dict1')
        self.db.lcreate('list1')
        x = self.db.getall()
        z = list(x)
        y = ['key2', 'key1', 'dict1', 'list1']
        assert x == y

    def test_get(self):
        self.db.set('key', 'value')
        x = self.db.get('key')
        assert x == 'value'

    def test_rem(self):
        self.db.set('key', 'value')
        self.db.rem('key')
        x = self.db.get('key')
        assert x is False

    def test_append(self):
        self.db.set('key', 'value')
        self.db.append('key', 'value')
        x = self.db.get('key')
        assert x == 'valuevalue'

    def test_exists(self):
        self.db.set('key', 'value')
        x = self.db.exists('key')
        assert x is True
