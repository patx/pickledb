import pickledb


class TestClass(object):

    db = pickledb.load('tests.db', False)

    def test_get(self):
        self.db.set('key', 'value')
        x = self.db.get('key')
        assert x == 'value'

    def test_rem(self):
        self.db.set('key', 'value')
        self.db.rem('key')
        x = self.db.get('key')
        assert x is None

    def test_append(self):
        self.db.set('key', 'value')
        self.db.append('key', 'value')
        x = self.db.get('key')
        assert x == 'valuevalue'

    def test_exists(self):
        self.db.set('key', 'value')
        x = self.db.exists('key')
        assert x is True
