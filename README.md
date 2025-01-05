![Download badge](http://pepy.tech/badge/pickledb)

# pickleDB
pickleDB is lightweight, fast, and simple database based on the
[json](https://docs.python.org/3/library/json.html) module.
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


# PickleDB Documentation

PickleDB is a lightweight, file-based key-value store written in Python. It offers support for basic operations, lists, dictionaries, and optional TTL (time-to-live) functionality, with built-in thread safety.

---

## Features

- **Key-Value Store**: Simple `set` and `get` operations.
- **Lists and Dictionaries**: Native support for list and dictionary data types.
- **Thread Safety**: Uses `RLock` to ensure safe multi-threaded operations.
- **TTL Support**: Optional time-to-live functionality for expiring keys.
- **Auto Dump**: Automatically saves changes to the database file.
- **File Compression**: Compresses the database file using gzip.
- **Human-Readable Storage**: Stores data in a JSON file for easy inspection and modification.

---

## Installation

PickleDB is a Python script. To use it, clone the repository and import the `PickleDB` class or use the `load` function in your project.

```bash
# Clone the repository
git clone https://github.com/your-repo/pickledb.git

# Use in your Python code
from pickledb import load
```

---

## Initialization

To create or load a database:

```python
from pickledb import load

db = load("example.db", auto_dump=True, enable_ttl=True)
```

- `location`: Path to the JSON file where the database will be stored.
- `auto_dump`: If `True`, changes to the database are automatically saved.
- `enable_ttl`: If `True`, keys can be assigned a time-to-live.

---

## API Reference

### Key-Value Operations

#### `set(key, value, ttl=None)`
Set a key-value pair in the database.

- **key** (str): The key.
- **value**: The value to associate with the key.
- **ttl** (int, optional): Time-to-live in seconds. Defaults to `None`.

#### `get(key)`
Get the value associated with a key.

- **Returns**: The value, or `None` if the key does not exist or has expired.

#### `exists(key)`
Check if a key exists in the database.

- **Returns**: `True` if the key exists, `False` otherwise.

#### `rem(key)`
Remove a key from the database.

- **Returns**: `True` if the key was removed, `False` otherwise.

#### `getall()`
Retrieve all keys in the database.

- **Returns**: A list of all keys.

#### `clear()`
Remove all keys from the database.

#### `deldb()`
Delete the entire database file.

---

### TTL Support

Keys can have an optional TTL (time-to-live), causing them to expire after a set duration.

#### Example:

```python
# Set a key with a 10-second TTL
db.set("temp_key", "temp_value", ttl=10)

# Wait for expiration
time.sleep(11)
print(db.get("temp_key"))  # Output: None
```

---

### List Operations

#### `lcreate(name)`
Create a new list in the database.

#### `ladd(name, value)`
Add a value to an existing list.

#### `lgetall(name)`
Retrieve all values from a list.

---

### Dictionary Operations

#### `dcreate(name)`
Create a new dictionary in the database.

#### `dadd(name, key, value)`
Add a key-value pair to a dictionary.

#### `dget(name, key)`
Retrieve a value from a dictionary.

#### `dgetall(name)`
Retrieve all key-value pairs from a dictionary.

---

### File Compression

#### `compress()`
Compress the database file using gzip.

#### Example:

```python
# Compress the database file
db.compress()
```

---

## Thread Safety

PickleDB uses `RLock` to ensure safe multi-threaded operations. This allows recursive locking within the same thread, ensuring consistent access to the database.

---

## Example Usage

```python
from pickledb import load
import time

# Initialize database
db = load("mydb.json", auto_dump=True, enable_ttl=True)

# Key-Value Operations
db.set("key1", "value1")
print(db.get("key1"))

# List Operations
db.lcreate("mylist")
db.ladd("mylist", "item1")
print(db.lgetall("mylist"))

# Dictionary Operations
db.dcreate("mydict")
db.dadd("mydict", "key1", "value1")
print(db.dgetall("mydict"))

# TTL Example
db.set("temp_key", "temp_value", ttl=5)
time.sleep(6)
print(db.get("temp_key"))  # Output: None

# Compress the database file
db.compress()
```

---

## Testing

Unit tests for PickleDB are included in `test_pickledb.py`. Run the tests using:

```bash
python -m unittest test_pickledb.py
```

---

## License

PickleDB is licensed under the BSD License. See the `LICENSE` file for more details.


