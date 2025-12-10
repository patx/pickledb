[![Logo](https://patx.github.io/pickledb/logo.png)](https://patx.github.io/pickledb)

[pickleDB](https://patx.github.io/pickledb) is a fast, easy to use, in-memory Python 
key-value store with asynchronous support. It is built with the `orjson` module for 
extremely high performance and was originally inspired by Redis. It is licensed under 
the BSD three-clause license.

### pickleDB is easy

```python
>>> from pickledb import PickleDB

>>> db = PickleDB('example.json')

>>> db.set('key', 'value')
True

>>> db.get('key')
'value'
```

### Useful links

- **Homepage**: [patx.github.io/pickledb](https://patx.github.io/pickledb)
- **GitHub**: [github.com/patx/pickledb](https://github.com/patx/pickledb)


