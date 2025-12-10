[![Logo](https://patx.github.io/pickledb/logo.png)](https://patx.github.io/pickledb)

[![PyPI Downloads](https://static.pepy.tech/badge/pickledb)](https://pepy.tech/projects/pickledb)

## **pickleDB: Your Lightweight, High-Speed Key-Value Store**

`pickleDB` is a lightweight, in-memory key-value store designed for developers who want **simplicity, speed, and reliability** — without sacrificing modern capabilities. BSD 3-Clause License © Harrison Erd.

- 💫 **Blazing Speed**: Backed by the high-performance [orjson](https://pypi.org/project/orjson/) library, pickleDB handles millions of records with ease. Perfect for applications where every millisecond counts
- 😋 **Ridiculously Easy to Use**: With its minimalist API, pickleDB makes adding, retrieving, and managing your data as simple as writing a Python list. No steep learning curves. No unnecessary complexity.
- 🔒 **Rock-Solid Reliability**: Your data deserves to be safe. Atomic saves ensure your database remains consistent—even if something goes wrong.
- 🐍 **Simple Pythonic Flexibility**: Store strings, lists, dictionaries, and more—all with native Python operations. No need to learn special commands. If you know Python, you already know pickleDB.
- 🙋 **Community & Contributions**: We’re passionate about making pickleDB better every day. Got ideas, feedback, or an issue to report? Let’s connect on [GitHub Issues](https://github.com/patx/pickledb/issues)
- 💾 **Portable**: Data is stored as standard JSON, human-readable and cross-language friendly.
- 🕸️ **Async-Ready**: Non-blocking I/O with [aiofiles](https://pypi.org/project/aiofiles/). Works with web frameworks like Starlette, FastAPI, or [MicroPie](https://patx.github.io/micropie).
- ⚡ **Unified API**: One class, one set of methods - works seamlessly in **both sync and async** environments.
- 💢 **Limitations**: The entire dataset resides **in memory** while loaded which might be a constraint on systems with limited RAM for extremely large datasets. pickleDB is designed for simplicity, so it may not meet the needs of applications requiring advanced database features. For larger-scale or concurrent applications requiring a more robust, consider [DataSet](https://dataset.readthedocs.io/en/latest/), [Redis](https://redis.io/), [SQLite](https://www.sqlite.org/), or [MongoDB](https://www.mongodb.com/).
- 📎 **Useful Links**: [GitHub](https://github.com/patx/pickledb) - [PyPI](https://pypi.org/project/pickleDB/) - [Report an Issue/Ask for Help](https://github.com/patx/pickledb/issues) - [Documentation](https://harrisonerd.com/pickledb)

## Getting Started

### Installation
Install via pip:

```bash
pip install pickledb
```

### Synchronous Example

```python
from pickledb import PickleDB

db = PickleDB("data.json")
db.load()

db.set("username", "alice")
db.set("theme", {"color": "blue", "font": "sans-serif"})

print(db.get("username"))  # → "alice"

db.save()
```

### Asynchronous Example

```python
import asyncio
from pickledb import PickleDB

async def main():
    async with PickleDB("data.json") as db:
        await db.set("score", 42)
        value = await db.get("score")
        print(value)  # → 42

asyncio.run(main())
```


## Core Methods

| Method | Description |
|--------|--------------|
| `load()` | Loads the database from disk (async-aware). |
| `save()` | Atomically saves the database to disk. |
| `set(key, value)` | Sets or updates a key. |
| `get(key, default=None)` | Returns the value for a key. |
| `remove(key)` | Deletes a key if it exists. |
| `all()` | Returns a list of all keys. |
| `purge()` | Clears the entire database. |

All of these methods can be used **synchronously or asynchronously** — just `await` them if inside an event loop.


## Performance Highlights

pickleDB demonstrates strong performance for handling large-sized datasets:

| Entries      | Memory Load Time | Retrieval Time | Save Time |
|--------------|------------------|----------------|-----------|
| **1M**       | 0.68 sec         | 0.64 sec       | 0.03 sec  |
| **10M**      | 7.48 sec         | 7.27 sec       | 0.22 sec  |
| **50M**      | 43.36 sec        | 36.53 sec      | 1.09 sec  |

Tests were performed on a Dell XPS 9350 running Ubuntu 24.04 using pickleDB's async mode.


## User Guide and Examples

### Add or Update Data

You can add or update key-value pairs using the `set()` method:

```python
# Add a new key-value pair
db.set('username', 'admin')

# Or shorthand
db['username'] = 'admin'

# Update an existing key-value pair
db.set('username', 'superadmin')
print(db.get('username'))  # Output: 'superadmin'
```

Keys are automatically converted to strings, and values can be any **JSON-serializable** object.

### Retrieve Values

You can retrieve a keys value using the `get()` method:

```python
# Get the value for a key
print(db.get('username'))  # Output: 'superadmin'

# Using Python syntax sugar
db['username']  # Output: 'superadmin'

# Attempt to retrieve a non-existent key
print(db.get('nonexistent'))  # Output: None
```

### List All Keys

You can get a list of all the keys currently in the database using the `all()` method:

```python
db.set('item1', 'value1')
db.set('item2', 'value2')

print(db.all())  # Output: ['username', 'item1', 'item2']
```

*Note:* This method shows all keys currently loaded, it does **not** guarantee they are persisted to the disk (yet).

### Remove Keys

To remove a key from the database use the `remove()` method:

```python
db.remove('item1')
print(db.all())  # Output: ['username', 'item2']
```

### Purge the Database

To remove all keys and their values from the database use the `purge()` method:
 
```python
db.purge()
print(db.all())  # Output: []
```

### Saving Data

**pickleDB does not auto-save by default** for performance reasons. To persist data, call `save()` manually or use a context manager:

```python
db.save()  # Output: True

# Context manager example
with db:
    db.set('foo', 'bar')
    db.set('hello', 'world')
# Automatically saves when exiting the context
```

*Note:* All the above methods work/display on the in-memory database. To persist any of the above methods actions use must call the `save()` method or use a context manager, as stated above.

### Asynchronous Usage

pickleDB 1.4 uses a **single unified class** for both synchronous and asynchronous contexts.

```python
import asyncio
from pickledb import PickleDB

async def main():
    async with PickleDB('data.json') as db:
        await db.set('score', 42)
        print(await db.get('score'))  # Output: 42

asyncio.run(main())
```

Just `await` any method when inside an async function/event-loop.

### Store and Retrieve Complex Data

```python
# Store a dictionary
db.set('user', {'name': 'Alice', 'age': 30, 'city': 'Wonderland'})

# Retrieve and modify
user = db.get('user')
user['age'] += 1
db.set('user', user)

print(db.get('user'))
# Output: {'name': 'Alice', 'age': 31, 'city': 'Wonderland'}
```

### Use Lists for Dynamic Data

```python
db.set('tasks', ['Write code', 'Test app', 'Deploy'])

tasks = db.get('tasks')
tasks.append('Celebrate')
db.set('tasks', tasks)

print(db.get('tasks'))
# Output: ['Write code', 'Test app', 'Deploy', 'Celebrate']
```

### Advanced Key Search

You can filter keys dynamically using Python list comprehensions:

```python
def get_keys_with_match(db_instance, match):
    return [key for key in db_instance.all() if match in key]

db.set('apple', 1)
db.set('apricot', 2)
db.set('banana', 3)

print(get_keys_with_match(db, 'ap'))
# Output: ['apple', 'apricot']
```

### Namespaces

Simulate namespaces using prefixes:

```python
db.set('user:1', {'name': 'Alice'})
db.set('user:2', {'name': 'Bob'})

def get_namespace_keys(db_instance, namespace):
    return [key for key in db_instance.all() if key.startswith(f"{namespace}:")]

print(get_namespace_keys(db, 'user'))
# Output: ['user:1', 'user:2']
```

### Key Expiration (TTL)

pickleDB doesn’t include TTL natively, but you can simulate it:

```python
import time

def set_with_expiry(db, key, value, ttl):
    db.set(key, {'value': value, 'expires_at': time.time() + ttl})

def get_if_not_expired(db, key):
    data = db.get(key)
    if data and time.time() < data['expires_at']:
        return data['value']
    db.remove(key)
    return None

set_with_expiry(db, 'session', 'active', ttl=5)
time.sleep(3)
print(get_if_not_expired(db, 'session'))  # 'active'
time.sleep(3)
print(get_if_not_expired(db, 'session'))  # None
```

### Encrypted Storage

```python
from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher = Fernet(key)

encrypted = cipher.encrypt(b"My secret data")
db.set('secure', encrypted)

decrypted = cipher.decrypt(db.get('secure'))
print(decrypted.decode())  # Output: My secret data
```

### Batch Operations

```python
def batch_set(db, items):
    for key, value in items.items():
        db.set(key, value)

batch_set(db, {'k1': 'v1', 'k2': 'v2', 'k3': 'v3'})
print(db.all())

def batch_delete(db, keys):
    for key in keys:
        db.remove(key)

batch_delete(db, ['k1', 'k2'])
print(db.all())
```

### Key Pattern Matching

```python
import re

def get_keys_by_pattern(db, pattern):
    regex = re.compile(pattern)
    return [key for key in db.all() if regex.search(key)]

db.set('user:1', {'name': 'Alice'})
db.set('user:2', {'name': 'Bob'})
db.set('admin:1', {'name': 'Charlie'})

print(get_keys_by_pattern(db, r'user:\d'))
# Output: ['user:1', 'user:2']
```

### Signal Handling for Graceful Shutdowns

```python
import signal, sys
from pickledb import PickleDB

db = PickleDB('data.json')

signal.signal(signal.SIGINT, lambda s, f: (db.save(), sys.exit(0)))
signal.signal(signal.SIGTERM, lambda s, f: (db.save(), sys.exit(0)))

db.set('key1', 'value1')
print("Running... Press Ctrl+C to save and exit.")
while True:
    pass
```

### Using pickleDB with Web Frameworks

Example using [MicroPie](https://patx.github.io/micropie):

```python
from uuid import uuid4
from micropie import App
from pickledb import PickleDB

db = PickleDB('pastes.json')

class Root(App):
    async def index(self, paste_content=None):
        if self.request.method == "POST":
            pid = str(uuid4())
            await db.set(pid, paste)
            await db.save()
            return self._redirect(f'/paste/{pid}')
        return await self._render_template('index.html')

    async def paste(self, paste_id):
        paste = await db.get(paste_id)
        return await self._render_template('paste.html', paste_id=paste_id, paste_content=paste)

app = Root()
```

## Core API Reference

### Class: `PickleDB`

```python
class PickleDB(location: str)
```

A lightweight, JSON-backed key-value database. All data is kept in memory while loaded and written atomically to disk on `save()`.

#### Parameters
| Name | Type | Description |
|------|-------|-------------|
| `location` | `str` | Path to the JSON file backing the database. Tilde (`~`) is expanded. |


### Context Manager Support

#### Synchronous
```python
with PickleDB("data.json") as db:
    db.set("foo", "bar")
```

#### Asynchronous
```python
async with PickleDB("data.json") as db:
    await db.set("foo", "bar")
```

On successful exit, the DB is automatically saved.


### Method Reference

#### `load()`

```python
load() -> None
await load() -> None
```

Loads the database into memory from disk if the file exists and contains valid JSON. Creates an empty database otherwise.


#### `save()`

```python
save() -> bool
await save() -> bool
```

Writes the in-memory database to disk.

Returns `True` on success.

Notes:
- Uses a temporary file + `os.replace` for durability.
- Automatically called on successful context-manager exit.

#### `set()`

```python
set(key: str, value: Any) -> bool
await set(key: str, value: Any) -> bool
```

Sets or updates a value for a key.
`key` is coerced to `str`, and `value` must be JSON-serializable.

Returns `True`.

##### Syntax Sugar
```python
db["username"] = "alice"
```

#### `get()`

```python
get(key: str, default: Any = None) -> Any
await get(key: str, default: Any = None) -> Any
```

Retrieves a value by key.

Returns:
- stored value
- `default` if key does not exist

##### Syntax Sugar
```python
value = db["username"]
```


#### `remove()`

```python
remove(key: str) -> bool
await remove(key: str) -> bool
```

Removes a key.

Returns:
- `True` if removed
- `False` if not found

#### `all()`

```python
all() -> list[str]
await all() -> list[str]
```

Returns a list of all keys currently in memory.

#### `purge()`

```python
purge() -> bool
await purge() -> bool
```

Clears the entire in-memory database.

Returns:
- `True`

### Synchronous vs Asynchronous Behavior

All public methods of `PickleDB` work in both runtimes:

| Environment | Usage |
|-------------|--------|
| Synchronous | `db.load()` |
| Asynchronous | `await db.load()` |

Internally, the library detects whether it is inside an async event loop.
