.. Image:: http://pepy.tech/badge/pickledb

pickleDB
--------

pickleDB is lightweight, fast, and simple database based on the `simplejson <https://pypi.python.org/pypi/simplejson/>`_ module. And it's BSD licensed!


pickleDB is Fun
```````````````

    >>> import pickledb

    >>> db = pickledb.load('test.db', False)

    >>> db.set('key', 'value')

    >>> db.get('key')
    'value'

    >>> db.dump()
    True


Easy to Install
```````````````

    $ pip install pickledb


Links
`````

* `website <https://patx.github.io/pickledb>`_
* `documentation <http://patx.github.io/pickledb/commands.html>`_
* `pypi <http://pypi.python.org/pypi/pickleDB>`_
* `github repo <https://github.com/patx/pickledb>`_
