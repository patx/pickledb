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

* `website <https://patx.github.io/pickledb>`_
* `documentation <http://patx.github.io/pickledb/commands.html>`_
* `pypi <http://pypi.python.org/pypi/pickleDB>`_
* `github repo <https://github.com/patx/pickledb>`_

"""

from distutils.core import setup

setup(name = "pickleDB",
    version="0.8.0",
    description="A lightweight and simple database using simplejson.",
    author="Harrison Erd",
    author_email="erdh@mail.broward.edu",
    license="three-clause BSD",
    url="http://github.com/patx/pickledb",
    long_description=__doc__,
    classifiers = [
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Intended Audience :: Developers",
        "Topic :: Database" ],
    py_modules=['pickledb'],
    install_requires=['simplejson'])
