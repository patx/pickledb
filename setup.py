"""
pickleDB
--------

pickleDB is lightweight, fast, and simple database based on Python's own 
json module. And it's BSD licensed!

pickleDB is Fun
```````````````

::

    >>> import pickledb as db

    >>> db.load('test.db')

    >>> db.set('key', 'value')

    >>> db.get('key')
    'value'


And Easy to Install
```````````````````

::

    $ pip install pickledb

Links
`````

* `website <http://packages.python.org/pickleDB/>`_
* `documentation <http://packages.python.org/pickleDB/commands.html>`_
* `github repo
  <https://github.com/patx/pickledb>`_

"""

from distutils.core import setup

setup(name = "pickleDB",
    version="0.2.1",
    description="A lightweight, fast, and simple database using json.",
    author="Harrison Erd",
    author_email="patx44@gmail.com",
    license="three-clause BSD",
    url="http://github.com/patx/pickledb",
    long_description=__doc__,
    classifiers = [
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Intended Audience :: Developers",
        "Topic :: Database" ],
    py_modules=['pickledb'])
