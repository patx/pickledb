pickleDB
--------

pickleDB is lightweight, fast, and simple database based on Python's own 
json module. And it's BSD licensed!


pickleDB is Fun
```````````````

    >>> import pickledb

    >>> db = pickledb.load('test.db', False)

    >>> db.set('key', 'value')

    >>> db.get('key')
    'value'

    >>> db.dump()
    True


And Easy to Install
```````````````````

    $ pip install pickledb


Links
`````

* `website <http://pythonhosted.org/pickleDB/>`_
* `documentation <http://pythonhosted.org/pickleDB/commands.html>`_
* `pypi <http://pypi.python.org/pypi/pickleDB>`_
