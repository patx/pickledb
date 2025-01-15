[![PyPI Downloads](https://static.pepy.tech/badge/pickledb)](https://pepy.tech/projects/pickledb)

# **pickleDB: Your Lightweight, High-Speed Key-Value Store**

## **Fast. Simple. Reliable.**
Unlock the power of effortless data storage with **pickleDB**—the no-fuss, blazing-fast key-value store designed for Python developers. Whether you're building a small script or a performant microservice, pickleDB delivers simplicity and speed with the reliability you can count on.

## **Why Choose pickleDB?**

### ✅ **Blazing Speed**
Backed by the high-performance [orjson](https://pypi.org/project/orjson/) library, pickleDB handles millions of records with ease. Perfect for applications where every millisecond counts.

### ✅ **Ridiculously Easy to Use**
With its minimalist API, pickleDB makes adding, retrieving, and managing your data as simple as writing a Python list. No steep learning curves. No unnecessary complexity.

### ✅ **Rock-Solid Reliability**
Your data deserves to be safe. Atomic saves ensure your database remains consistent—even if something goes wrong.

### ✅ **Pythonic Flexibility**
Store strings, lists, dictionaries, and more—all with native Python operations. No need to learn special commands. If you know Python, you already know pickleDB.


## **Getting Started**

### **Install in Seconds**
pickleDB is available on PyPI. Get started with just one command:
```bash
pip install pickledb
```

### **Your First pickleDB**
```python
from pickledb import PickleDB

# Initialize the database
db = PickleDB('my_database.db')

# Add a key-value pair
db.set('greeting', 'Hello, world!')

# Retrieve the value
print(db.get('greeting'))  # Output: Hello, world!

# Save the data to disk
db.save()
```
It’s that simple! In just a few lines, you have a fully functioning key-value store.

## **Performance Highlights**

pickleDB demonstrates strong performance for handling large-sized datasets:

| Entries      | Memory Load Time | Retrieval Time | Save Time |
|--------------|------------------|----------------|-----------|
| **1M**       | 1.21 sec         | 0.90 sec       | 0.17 sec  |
| **10M**      | 14.11 sec        | 10.30 sec      | 1.67 sec  |
| **50M**      | 93.79 sec        | 136.42 sec     | 61.08 sec |

Tests were performed on a StarLabs StarLite Mk IV (Quad-Core Intel® Pentium® Silver N5030 CPU @ 1.10GHz w/ 8GB memory) running elementary OS 7.1 Horus.

## **Minimal, Powerful API**

pickleDB offers a clean and Pythonic API for managing data efficiently:

### **`set(key, value)`**
Add or update a key-value pair:
```python
# Add a new key-value pair
db.set('username', 'admin')

# Or shorthand
db['username'] = 'admin'

# Update an existing key-value pair
db.set('username', 'superadmin')
print(db.get('username'))  # Output: 'superadmin'
```

### **`get(key)`**
Retrieve the value associated with a key:
```python
# Get the value for a key
print(db.get('username'))  # Output: 'superadmin'

# Like the set() method, you can use Python syntax sugar here as well
print(db['username']) # Output: 'superadmin'

# Attempt to retrieve a non-existent key
print(db.get('nonexistent_key'))  # Output: None
```

### **`all()`**
Get a list of all keys:
```python
# Add multiple keys
db.set('item1', 'value1')
db.set('item2', 'value2')

# Retrieve all keys
print(db.all())  # Output: ['username', 'item1', 'item2']
```

### **`remove(key)`**
Delete a key and its value:
```python
# Remove a key-value pair
db.remove('item1')
print(db.all())  # Output: ['username', 'item2']
```

### **`purge()`**
Clear all data in the database:
```python
# Clear the database
db.purge()
print(db.all())  # Output: []
```

### **`save()`**
Persist the database to disk:
```python
# Save the current state of the database
db.save()
print("Database saved successfully!")
```


## **Key Improvements in Version 1.0**

pickleDB 1.0 is a reimagined version designed for speed, simplicity, and reliability. Key changes include:

- **Atomic Saves**: Ensures data integrity during writes, eliminating potential corruption issues.
- **Faster Serialization**: Switched to `orjson` for significantly improved speed.
- **Streamlined API**: Removed legacy methods (e.g., `ladd`, `dmerge`) in favor of native Python operations.
- **Unified Handling of Data Types**: Treats all Python-native types (lists, dicts, etc.) as first-class citizens.
- **Explicit Saves**: The `auto_save` feature was removed to provide users greater control and optimize performance.

If backward compatibility is essential, version 0.9 is still available:
- View the legacy code [here](https://gist.github.com/patx/3ad47fc3814d7293feb902f6ab49c48f).
- Install it by:
  ```bash
  pip uninstall pickledb
  ```
  Then download the legacy file and include it in your project.


## **With pickleDB you have the full power of Python behind you! Check out some examples of advanced use cases**

### **Store and Retrieve Complex Data**
PickleDB works seamlessly with Python data structures. Example:
```python
# Store a dictionary
db.set('user', {'name': 'Alice', 'age': 30, 'city': 'Wonderland'})

# Retrieve and update it
user = db.get('user')
user['age'] += 1

# Save the updated data
db.set('user', user)
print(db.get('user'))  # Output: {'name': 'Alice', 'age': 31, 'city': 'Wonderland'}
```

### **Use Lists for Dynamic Data**
Handle lists with ease:
```python
# Add a list of items
db.set('tasks', ['Write code', 'Test app', 'Deploy'])

# Retrieve and modify
tasks = db.get('tasks')
tasks.append('Celebrate')
db.set('tasks', tasks)

print(db.get('tasks'))  # Output: ['Write code', 'Test app', 'Deploy', 'Celebrate']
```

### **Store Configurations**
Create a simple, persistent configuration store:
```python
# Set configuration options
db.set('config', {'theme': 'dark', 'notifications': True})

# Access and update settings
config = db.get('config')
config['notifications'] = False
db.set('config', config)
print(db.get('config'))  # Output: {'theme': 'dark', 'notifications': False}
```

### **Session Management**
Track user sessions effortlessly:
```python
# Add session data
db.set('session_12345', {'user_id': 1, 'status': 'active'})

# End a session
session = db.get('session_12345')
session['status'] = 'inactive'
db.set('session_12345', session)

print(db.get('session_12345'))  # Output: {'user_id': 1, 'status': 'inactive'}
```

### **Advanced Key Search**
Search the database with the full power of Python:
```python
# Create simple helper methods based on what YOU need
def get_keys_with_match_list(db_instance, match):
    return [key for key in db_instance.all() if match in key]

def get_keys_with_match_dict(db_instance, match):
    return dict(filter(lambda item: match in item[0], db_instance.db.items()))

# Create an instance of PickleDB
db = PickleDB("example.json")

# Add key-value pairs
db.set('apple', 1)
db.set('apricot', 2)
db.set('banana', 3)

# Use glob search to return a list
matching_keys = get_keys_with_match_list(db, 'ap')
print(matching_keys)  # Output: ['apple', 'apricot']

# Use glob search to return a dict
matching_dict = get_keys_with_match_dict(db, 'ap')
print(matching_dict)  # Output: {"apple": 1, "apricot": 3}
```

### Namespace Support
If you use prefixes to simulate namespaces, you can manage groups of keys more efficiently:
```python
# Set multiple keys with a namespace
db.set('user:1', {'name': 'Alice', 'age': 30})
db.set('user:2', {'name': 'Bob', 'age': 25})

# Get all keys in a namespace
def get_namespace_keys(db_instance, namespace):
    return [key for key in db_instance.all() if key.startswith(f"{namespace}:")]

user_keys = get_namespace_keys(db, 'user')
print(user_keys)  # Output: ['user:1', 'user:2']
```

### Expire Keys
Manually simulate a basic TTL (time-to-live) mechanism for expiring keys:
```python
import time

# Set a key with an expiration time
def set_with_expiry(db_instance, key, value, ttl):
    db_instance.set(key, {'value': value, 'expires_at': time.time() + ttl})

# Get a key only if it hasn't expired
def get_if_not_expired(db_instance, key):
    data = db_instance.get(key)
    if data and time.time() < data['expires_at']:
        return data['value']
    db_instance.remove(key)  # Remove expired key
    return None

# Example usage
set_with_expiry(db, 'session_123', 'active', ttl=10)
time.sleep(5)
print(get_if_not_expired(db, 'session_123'))  # Output: 'active'
time.sleep(6)
print(get_if_not_expired(db, 'session_123'))  # Output: None
```

### Encrypted Storage
Use encryption for secure storage of sensitive data:
```python
from cryptography.fernet import Fernet

# Initialize encryption
key = Fernet.generate_key()
cipher = Fernet(key)

# Encrypt and save data
encrypted_value = cipher.encrypt(b"My secret data")
db.set('secure_key', encrypted_value)

# Retrieve and decrypt data
encrypted_value = db.get('secure_key')
decrypted_value = cipher.decrypt(encrypted_value)
print(decrypted_value.decode())  # Output: My secret data

```

### Batch Operations
Add multiple key-value pairs in a single operation:
```python
def batch_set(db_instance, items):
    for key, value in items.items():
        db_instance.set(key, value)

# Add multiple keys
batch_set(db, {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'})
print(db.all())  # Output: ['key1', 'key2', 'key3']
```

Delete multiple key-value pairs in a single operation:
```python
def batch_delete(db_instance, keys):
    for key in keys:
        db_instance.remove(key)

# Example usage
db.set('temp1', 'value1')
db.set('temp2', 'value2')
batch_delete(db, ['temp1', 'temp2'])
print(db.all())  # Output: []
```

### Manipulate Database Stats
Display database statistics, such as the total number of keys, data size, or memory usage:
```python
def db_stats(db_instance):
    total_keys = len(db_instance.all())
    data_size = sum(len(str(value)) for value in db_instance.db.values())
    return {"total_keys": total_keys, "data_size": data_size}

# Example usage
stats = db_stats(db)
print(stats)  # Output: {'total_keys': 10, 'data_size': 12345}
```

### Data Migration
Export and import database content between files:
```python
# Export database content
def export_db(db_instance, export_path):
    with open(export_path, 'w') as f:
        f.write(orjson.dumps(db_instance.db).decode())

# Import database content
def import_db(db_instance, import_path):
    with open(import_path, 'r') as f:
        db_instance.db = orjson.loads(f.read())
    db_instance.save()

# Example usage
export_db(db, 'exported_data.json')
db.purge()
import_db(db, 'exported_data.json')
print(db.all())  # Restores all keys
```

### Backup to AWS
Demonstrate a method for backing up the database to a remote location, such as an AWS S3 bucket:
```python
import boto3

def backup_to_s3(db_instance, bucket_name, s3_key):
    s3 = boto3.client('s3')
    with open(db_instance.location, 'rb') as f:
        s3.upload_fileobj(f, bucket_name, s3_key)

# Example usage
backup_to_s3(db, 'my-s3-bucket', 'backup/my_database.db')
```

### Use pickleDB over HTTP (REST)
Access pickleDB database with any language that can handle REST requests:
```python
from flask import Flask, request, jsonify
from pickledb import PickleDB

app = Flask(__name__)
db = PickleDB('api.db')

@app.route('/set', methods=['POST'])
def set_value():
    data = request.json
    db.set(data['key'], data['value'])
    db.save()
    return jsonify({"message": "Value saved!"})

@app.route('/get/<key>', methods=['GET'])
def get_value(key):
    value = db.get(key)
    return jsonify({"value": value})

if __name__ == '__main__':
    app.run(debug=True)
```

### Key Pattern Matching
Support complex matching patterns using regular expressions:
```python
import re

# Get keys that match a regex pattern
def get_keys_by_pattern(db_instance, pattern):
    regex = re.compile(pattern)
    return [key for key in db_instance.all() if regex.search(key)]

# Example usage
db.set('user:1', {'name': 'Alice'})
db.set('user:2', {'name': 'Bob'})
db.set('admin:1', {'name': 'Charlie'})
matching_keys = get_keys_by_pattern(db, r'user:\d')
print(matching_keys)  # Output: ['user:1', 'user:2']
```

### Adding Custom Signal Handling
You can easily implement custom signal handling in your application to ensure graceful shutdowns and data persistence during unexpected terminations. Below is an example of how to integrate custom signal handling with pickleDB:

```python
import signal
import sys
from pickledb import PickleDB  # Import the PickleDB class

# Initialize the PickleDB instance
db = PickleDB('my_database.db')

# Register signal handlers for SIGINT (Ctrl+C) and SIGTERM (system termination)
signal.signal(signal.SIGINT, lambda signum, frame: (db.save(), sys.exit(0)))
signal.signal(signal.SIGTERM, lambda signum, frame: (db.save(), sys.exit(0)))

# Example usage
db.set('key1', 'value1')
db.set('key2', 'value2')

print("Database is running. Press Ctrl+C to save and exit.")

# Keep the program running to allow signal handling
try:
    while True:
        pass
except KeyboardInterrupt:
    pass
```

### **Asynchronous Saves**
Want non-blocking saves? You can implement an async wrapper to handle saves in the background. This is particularly useful for applications that need high responsiveness without delaying due to disk operations, like small web applications. Check out examples [here](https://gist.github.com/patx/5c12d495ff142f3262325eeae81eb000).

## **Limitations**

While pickleDB is powerful, it’s important to understand its limitations:

- **Memory Usage**: The entire dataset is loaded into memory, which might be a constraint on systems with limited RAM for extremely large datasets.
- **Single-Threaded**: The program is not thread-safe. For concurrent access, use external synchronization like Python's `RLock()`.
- **Blocking Saves**: Saves are blocking by default. To achieve non-blocking saves, use [asynchronous wrappers](https://gist.github.com/patx/5c12d495ff142f3262325eeae81eb000).
- **Lack of Advanced Features**: pickleDB is designed for simplicity, so it may not meet the needs of applications requiring advanced database features.

For projects requiring more robust solutions, consider alternatives like **[kenobiDB](Https://github.com/patx/kenobi)**, [Redis](http://redis.io/), [SQLite](https://www.sqlite.org/), or [MongoDB](https://www.mongodb.com/).

## **Community & Contributions**

### **Join the Community**
We’re passionate about making pickleDB better every day. Got ideas, feedback, or an issue to report? Let’s connect:
- **File an Issue**: [GitHub Issues](https://github.com/patx/pickledb/issues)
- **Ask Questions**: Reach out to our growing community of users and developers.

### **Contribute to pickleDB**
Want to leave your mark? Help us make pickleDB even better:
- **Submit a Pull Request**: Whether it's fixing a bug, improving the documentation, or adding a feature, we’d love your contributions.
- **Suggest New Features**: Share your ideas to make pickleDB more powerful.

Together, we can build a better tool for everyone.
