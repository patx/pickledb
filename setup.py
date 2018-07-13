"""
pickleDB
--------

pickleDB is lightweight, fast, and simple database based on Python's own
json module. And it's BSD licensed!

pickleDB is Fun
```````````````

::

    >>> import pickledb

    >>> db = pickledb.load('test.db', False)

    >>> db.set('key', 'value')

    >>> db.get('key')
    'value'

    >>> db.dump()
    True


And Easy to Install
```````````````````

::

    $ pip install pickledb

Links
`````

* `website <http://packages.python.org/pickleDB/>`_
* `documentation <http://packages.python.org/pickleDB/commands.html>`_
* `bitbucket repo <https://bitbucket.org/patx/pickledb>`_

"""

from distutils.core import setup

setup(name = "pickleDB",
    version="0.6.2",
    description="A lightweight and simple database with pickle or simplejson backend.",
    author="Harrison Erd",
    author_email="patx44@gmail.com",
    license="three-clause BSD",
    url="http://bitbucket.org/patx/pickledb",
    long_description=__doc__,
    classifiers = [
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Intended Audience :: Developers",
        "Topic :: Database" ],
    py_modules=['pickledb'],
    install_requires=['simplejson', 'pickle'])
