# **pickleDB: Your Lightweight, High-Speed Key-Value Store**

## **Fast. Simple. Reliable.**
Unlock the power of effortless data storage with **pickleDB**—the no-fuss, blazing-fast key-value store designed for Python developers. Whether you're building a small script or a performant microservice, pickleDB delivers simplicity and speed with the reliability you can count on.

---

## **Why Choose pickleDB?**

### ✅ **Blazing Speed**
Backed by the high-performance [orjson](https://pypi.org/project/orjson/) library, pickleDB handles millions of records with ease. Perfect for applications where every millisecond counts.

### ✅ **Ridiculously Easy to Use**
With its minimalist API, pickleDB makes adding, retrieving, and managing your data as simple as writing a Python list. No steep learning curves. No unnecessary complexity.

### ✅ **Rock-Solid Reliability**
Your data deserves to be safe. Atomic saves ensure your database remains consistent—even if something goes wrong.

### ✅ **Pythonic Flexibility**
Store strings, lists, dictionaries, and more—all with native Python operations. No need to learn special commands. If you know Python, you already know pickleDB.

---

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

---

## **More Examples to Get You Inspired**

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

---

## **Performance Highlights**

pickleDB demonstrates strong performance for handling large-sized datasets:

| Entries      | Memory Load Time | Retrieval Time | Save Time |
|--------------|------------------|----------------|-----------|
| **1M**       | 1.21 sec         | 0.90 sec       | 0.17 sec  |
| **10M**      | 14.11 sec        | 10.30 sec      | 1.67 sec  |
| **50M**      | 93.79 sec        | 136.42 sec     | 61.08 sec |

Tests were performed on a StarLabs StarLite Mk IV (Quad-Core Intel® Pentium® Silver N5030 CPU @ 1.10GHz w/ 8GB memory) running elementary OS 7.1 Horus.

---

## **Minimal, Powerful API**

pickleDB offers a clean and Pythonic API for managing data efficiently:

### **`set(key, value)`**
Add or update a key-value pair:
```python
# Add a new key-value pair
db.set('username', 'admin')

# Update an existing key-value pair
db.set('username', 'superadmin')
print(db.get('username'))  # Output: 'superadmin'
```

### **`get(key)`**
Retrieve the value associated with a key:
```python
# Get the value for a key
print(db.get('username'))  # Output: 'superadmin'

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

---

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

---

## **Limitations**

While pickleDB is powerful, it’s important to understand its limitations:

- **Memory Usage**: The entire dataset is loaded into memory, which might be a constraint on systems with limited RAM for extremely large datasets.
- **Single-Threaded**: The program is not thread-safe. For concurrent access, use external synchronization like Python's `RLock()`.
- **Blocking Saves**: Saves are blocking by default. To achieve non-blocking saves, use asynchronous wrappers.
- **Lack of Advanced Features**: pickleDB is designed for simplicity, so it may not meet the needs of applications requiring advanced database features.

For projects requiring more robust solutions, consider alternatives like **[kenobiDB](Https://github.com/patx/kenobi)**, [Redis](http://redis.io/), [SQLite](https://www.sqlite.org/), or [MongoDB](https://www.mongodb.com/).

---

## **Asynchronous Saves**
Want non-blocking saves? You can implement an async wrapper to handle saves in the background. This is particularly useful for applications that need high responsiveness without delaying due to disk operations, like small web applications. Check out examples [here](https://gist.github.com/patx/5c12d495ff142f3262325eeae81eb000).

---

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

---

## **Documentation**

Explore the full capabilities of pickleDB with our detailed documentation:
- **API Reference**: [Commands and Examples](https://patx.github.io/pickledb/commands.html)
- [GitHub Repository](https://github.com/patx/pickledb)
- [Installation Details (PyPI)](http://pypi.python.org/pypi/pickleDB)

Whether you're a beginner or an experienced developer, these resources will guide you through everything pickleDB has to offer.
