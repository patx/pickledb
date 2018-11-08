![Download badge](http://pepy.tech/badge/pickledb)

# pickleDB
pickleDB is lightweight, fast, and simple database based on the
[simplejson](https://pypi.python.org/pypi/simplejson/) module.
And it's BSD licensed!


## pickleDB is Fun
```python
>>> import pickledb

>>> db = pickledb.load('test.db', False)

>>> db.set('key', 'value')

>>> db.get('key')
'value'

>>> db.dump()
True
```

## Easy to Install
```python
$ pip install pickledb
```

## Links
* [website](https://patx.github.io/pickledb)
* [documentation](https://patx.github.io/pickledb/commands.html)
* [pypi](http://pypi.python.org/pypi/pickleDB)
* [github repo](https://github.com/patx/pickledb)


## Latest Release Notes (version: 0.8.0)
* All *keys* must now be strings
* All *names* for lists must now be strings
* All *names* for dicts must now be strings
* The get(key) function now returns *False* instead of None if there is no key

