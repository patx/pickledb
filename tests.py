import pickledb

# a work in progress


class TestClass(object):

    db = pickledb.load('tests.db', False)

    def test_load(self):
        x = pickledb.load('x.db', False)
        assert x is not None

    def test_sugar_get(self):
        self.db.db["foo"] = "bar"
        x = self.db["foo"]
        assert x == "bar"

    def test_sugar_set(self):
        self.db["foo"] = "bar"
        assert "bar" == self.db.db["foo"]

    def test_sugar_rem(self):
        self.db.db["foo"] = "bar"
        del self.db["foo"]
        assert "foo" not in self.db.db

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
        y = dict.fromkeys(['key2', 'key1', 'dict1', 'list1']).keys()
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
        self.db.rem('key')

    def test_not_exists(self):
        self.db.set('key', 'value')
        x = self.db.exists('not_key')
        assert x is False
        self.db.rem('key')

    def test_lexists(self):
        self.db.lcreate('list')
        self.db.ladd('list', 'value')
        x = self.db.lexists('list', 'value')
        assert x is True
        self.db.lrem('list')

    def test_not_lexists(self):
        self.db.lcreate('list')
        self.db.ladd('list', 'value')
        x = self.db.lexists('list', 'not_value')
        assert x is False
        self.db.lrem('list')

    def test_dexists(self):
        self.db.dcreate('dict')
        self.db.dadd('dict', ('key', 'value'))
        x = self.db.dexists('dict', 'key')
        assert x is True
        self.db.drem('dict')

    def test_not_dexists(self):
        self.db.dcreate('dict')
        self.db.dadd('dict', ('key', 'value'))
        x = self.db.dexists('dict', 'not_key')
        assert x is False
        self.db.drem('dict')
