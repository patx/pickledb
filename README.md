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

## Installation
- Just add the `pickledb.py` file to your working directory or use `pip install pickledb`.
- pickleDB also includes a simplified and faster version using orjson called `pkldb.py`, to use this add it to your working directory and note the slight difference in setup `from pkldb.py import pkldb` then `db = pkldb('example.json')`

# PickleDB Documentation

## Introduction
PickleDB is a lightweight, file-based key-value store with optional support for time-to-live (TTL). It provides a simple and intuitive API for storing and managing data persistently.

---

## Table of Contents
1. **Basic Usage**
2. **Key-Value Methods**
3. **List Methods**
4. **Dictionary Methods**
5. **Enhanced Features**

---

## 1. Basic Usage
```python
from pickledb_enhanced import load

db = load('mydb.json', auto_dump=True, enable_ttl=True)
```
- `auto_dump`: Automatically save changes to the file.
- `enable_ttl`: Enable TTL support for expiring keys.

---

## 2. Key-Value Methods

### `set(key, value, ttl=None)`
Set a key-value pair in the database.

### `get(key)`
Retrieve the value associated with a key.

### `exists(key)`
Check if a key exists.

### `rem(key)`
Remove a key from the database.

### `getall()`
Get all keys in the database.

### `clear()`
Clear all keys.

### `deldb()`
Delete the database file.

---

## 3. List Methods

### `lcreate(name)`
Create a new list in the database.

### `ladd(name, value)`
Add a value to an existing list.

### `lgetall(name)`
Retrieve all values from a list.

### `lsort(name, reverse=False)`
Sort a list in ascending or descending order.
- `reverse`: Sort in descending order if `True`.

### `lremove(name, value)`
Remove a value from a list.

### `lgetrange(name, start, end)`
Retrieve a range of values from a list.
- `start`: Start index.
- `end`: End index.

### `llen(name)`
Get the length of a list.

---

## 4. Dictionary Methods

### `dcreate(name)`
Create a new dictionary in the database.

### `dadd(name, key, value)`
Add a key-value pair to a dictionary.

### `dget(name, key)`
Retrieve a value from a dictionary.

### `dgetall(name)`
Retrieve all key-value pairs from a dictionary.

### `dremove(name, key)`
Remove a key from a dictionary.

### `dmerge(name, other_dict)`
Merge another dictionary into an existing dictionary.

### `dkeys(name)`
Get all keys from a dictionary.

### `dvalues(name)`
Get all values from a dictionary.

---

## 5. Enhanced Features

### **TTL Support**
- Expire keys automatically after a given time.

### **File Compression**
- Compress the database file to save space.

### **Automatic Persistence**
- Save changes automatically using `auto_dump`.

---

## Example Usage

### **Working with Lists**
```python
# Create a list and add values
db.lcreate('mylist')
db.ladd('mylist', 'item1')
db.ladd('mylist', 'item2')

# Sort the list
db.lsort('mylist')  # ['item1', 'item2']

# Get a range of values
db.lgetrange('mylist', 0, 1)  # ['item1']

# Remove an item
db.lremove('mylist', 'item1')
```

### **Working with Dictionaries**
```python
# Create a dictionary and add values
db.dcreate('mydict')
db.dadd('mydict', 'key1', 'value1')
db.dadd('mydict', 'key2', 'value2')

# Merge another dictionary
db.dmerge('mydict', {'key3': 'value3'})

# Get all keys and values
db.dkeys('mydict')  # ['key1', 'key2', 'key3']
db.dvalues('mydict')  # ['value1', 'value2', 'value3']

# Remove a key
db.dremove('mydict', 'key1')
```

---

## Notes
- Always ensure proper file permissions for the database file.
- Use thread-safe practices when accessing the database concurrently.

---

## Changelog
- **Enhanced Features**: Added methods for list sorting, removal, range fetching, and dictionary merging.

