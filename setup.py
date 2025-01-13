"""
pickleDB
--------

pickleDB is lightweight, fast, and simple database based on the orjson module. And it's BSD licensed!


pickleDB is Fun
```````````````

::

    >>> import pickledb

    >>> db = pickledb.load('test.db')

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

* `Website <https://patx.github.io/pickledb>`_
* `Documentation <http://patx.github.io/pickledb/commands.html>`_
* `PyPI <http://pypi.python.org/pypi/pickleDB>`_
* `Github Repo <https://github.com/patx/pickledb>`_


Key Improvements in Version 1.0
```````````````````````````````

* pickleDB 1.0 is a reimagined version designed for speed, simplicity, and reliability. This version is NOT backwards compatible. Key changes include:
* Atomic Saves: Ensures data integrity during writes, eliminating potential corruption issues.
* Faster Serialization: Switched to `orjson` for significantly improved speed.
* Streamlined API: Removed legacy methods (e.g., `ladd`, `dmerge`) in favor of native Python operations.
* Unified Handling of Data Types: Treats all Python-native types (lists, dicts, etc.) as first-class citizens.
* Explicit Saves: The `auto_save` feature was removed to provide users greater control and optimize performance.


"""

from distutils.core import setup

setup(name="pickleDB",
    version="1.0",
    description="A lightweight and simple database using json.",
    long_description=__doc__,
    author="Harrison Erd",
    author_email="erdh@mail.broward.edu",
    license="three-clause BSD",
    url="http://github.com/patx/pickledb",
    classifiers = [
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Intended Audience :: Developers",
        "Topic :: Database" ],
    py_modules=['pickledb'],
    install_requires=['orjson'],
)

