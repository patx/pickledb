pickleDB
========

pickleDB is a small, lightweight, and fast key-value store. It was inspired by 
[redis][1] and [MongoDB][2]. pickleDB is built upon Python's [json][3] module (
however, originally it was based on pickle, hence the name). BSD three-caluse licensed. 



Commands
--------

* `SET key value` Set the string value of a key

* `GET key` Get the value of a key

* `REM key` Delete a key

* `LCREATE name` Create a list

* `LADD name value` Add a value to a list

* `LGETALL name` Return all values in a list

* `LGET name pos` Return one value in a list

* `LREM name` Remove a list and all of its values

* `LPOP name pos` Remove one value in a list

* `APPEND key more` Add more to a key's value

* `LAPPEND name pos more` Add more to a value in a list


Example
-------

This is a quick example running through of the most basic commands.

    >>> import pickledb as db
    >>> db.load('test.db')
    True
    >>> db.set('key', 'value')
    True
    >>> db.get('key')
    'value'
    >>> db.rem('key')
    True
    >>> db.get('key')
    KeyError: 'key' # because its been deleted
    >>> db.lcreate('a list')
    True
    >>> db.ladd('a list', 'something')
    True
    >>> db.ladd('a list', 'now something else')
    True
    >>> db.getall('a list')
    ['something', 'now something else']
    >>> db.lget('a list', 0)
    'something'
    >>> db.lget('a list', 1)
    'now something else'
    >>> db.lpop('a list', 0)
    True
    >>> db.lgetall('a list')
    ['now something else']
    >>> db.lrem('a list')
    True
    >>> db.lgetall('a list')
    KeyError: 'a list' # because its been deleted


Installation
------------

    $ pip install pickledb


Contributing
------------

Once you've made your great commits:

1. [Fork][4] pickleDB
2. Create a topic branch - `git checkout -b my_branch`
3. Push to your branch - `git push origin my_branch`
4. Create an [Issue][5] with a link to your branch
5. That's it!


You can also send [me (patx)][6] and email with any suggestions and/or questions.


Meta
----

* Code: `git clone git://github.com/patx/pickledb.git`
* Home: <http://packages.python.org/pickleDB>
* Bugs: <http://github.com/patx/pickledb/issues>
* PyPi: <http://pypi.python.org/pypi/pickleDB>

[1]: http://redis.io/
[2]: http://www.mongodb.org/
[3]: http://docs.python.org/library/json.html
[4]: http://help.github.com/forking/
[5]: http://github.com/patx/pickledb/issues
[6]: mailto:patx44@gmail.com
