# pkldb

`pkldb` is a lightweight, high-performance, JSON-based key-value store designed to handle datasets of significant size while maintaining simplicity and speed. Built using the powerful `orjson` library, `pkldb` is perfect for developers who need an efficient, easy-to-use database for Python projects. This is a simplified version of pickleDB focusing on scalability with large datasets.

---

## **Features**

### 1. **High Performance**
- Blazing-fast operations for inserting, retrieving, and dumping data.
- Demonstrated ability to handle datasets up to **50 million key-value pairs** with predictable, linear performance scaling.

### 2. **Ease of Use**
- Simple API with intuitive methods for common database operations:
  - `set(key, value)` - Add or update key-value pairs.
  - `get(key)` - Retrieve the value associated with a key.
  - `remove(key)` - Delete a key-value pair.
  - `purge()` - Clear the database.
  - `all()` - Get a list of all keys.
  - `dump()` - Persist data to disk.

### 3. **Data Integrity**
- Atomic writes ensure the database remains consistent, even in the event of an error during disk operations.

### 4. **Scalable Design**
- Efficient memory and disk utilization enable handling of massive datasets on modern hardware.

### 5. **Configurable Auto Dumping**
- Enable or disable automatic saving of changes with the `auto_dump` parameter.

### 6. **Lightweight and Portable**
- Stores data in a simple JSON file, making it easy to move and manage.

---

## **Performance Highlights**

The `pkldb` has been rigorously tested for datasets of various sizes, showcasing its impressive performance:

### **Test Results**
| Entries      | Memory Load Time | Retrieval Time | Dump Time |
|--------------|------------------|----------------|-----------|
| **1M**       | 1.21s            | 0.90s          | 0.17s     |
| **10M**      | 14.11s           | 10.30s         | 1.67s     |
| **20M**      | 29.95s           | 21.86s         | 3.25s     |
| **50M**      | 93.79s           | 136.42s        | 61.08s    |

These results demonstrate `pkldb`'s capability to scale efficiently while maintaining excellent performance.

---

## **Installation**

```bash
pip install orjson
```

### Why `orjson`?
`orjson` is a fast and efficient JSON parser and serializer for Python. It is significantly faster than the built-in `json` module, enabling `pkldb` to achieve its high performance, especially when handling large datasets.

Download or clone this repository and include `pkldb.py` in your project.

---

## **Usage**

```python
from pkldb import pkldb

# Initialize the database
mydb = pkldb("my_database.db", auto_dump=False)

# Add key-value pairs
mydb.set("key1", "value1")
mydb.set("key2", 42)
mydb.set("key3", [1, 2, 3])  # Using a list as a value
mydb.set("key4", {"nested": "value"})  # Using a dictionary as a value

# Retrieve a value
print(mydb.get("key1"))  # Output: value1
print(mydb.get("key4"))  # Output: {'nested': 'value'}

# List all keys
print(mydb.all())  # Output: ["key1", "key2", "key3", "key4"]

# Remove a key
mydb.remove("key1")
print(mydb.all())  # Output: ["key2", "key3", "key4"]

# Save the database to disk
mydb.dump()
print("Database saved to disk.")

# Clear the database
mydb.purge()
print(mydb.all())  # Output: []
```

---

## **Comparison with Other Databases**

| Feature              | pkldb       | Redis        | SQLite       | TinyDB      | MongoDB     | KenobiDB    |
|----------------------|-------------|--------------|--------------|-------------|-------------|-------------|
| **Storage Type**     | JSON File   | In-Memory    | File-Based   | JSON File   | Document DB | SQLite      |
| **Data Model**       | Key-Value   | Key-Value    | Relational   | Key-Value   | Document    | Document    |
| **Persistence**      | Yes         | Optional     | Yes          | Yes         | Yes         | Yes         |
| **Scalability**      | Medium      | High         | Medium       | Low         | High        | Medium      |
| **Setup**            | None        | Server-Based | None         | None        | Server-Based| None        |
| **Performance**      | High        | Very High    | Medium       | Low         | High        | Medium      |
| **Dependencies**     | Minimal     | Moderate     | Minimal      | Minimal     | High        | Minimal     |
| **Concurrency**      | Single-Threaded | Multi-Threaded | Single-Threaded | Single-Threaded | Multi-Threaded | Multi-Threaded |
| **Use Case**         | Lightweight and portable key-value store | High-performance caching | Local relational database | Lightweight JSON-based store | Scalable NoSQL solutions | Lightweight document database |

### **Strengths**

- **Speed**: Handles massive datasets with ease, outperforming many similar solutions.
- **Data Integrity**: Atomic dumps ensure your data is always safe.
- **Simplicity**: Minimal dependencies and an intuitive API make it beginner-friendly.
- **Portability**: JSON-based storage simplifies data sharing and management.

### **Limitations**

- **Memory Usage**: The entire dataset is loaded into memory, which might be a constraint on systems with limited RAM for extremely large datasets.
- **Single-Threaded**: The program is not thread-safe. For concurrent access, use external synchronization like:
  ```python
  import threading

  lock = threading.Lock()

  # Thread-safe operations
  with lock:
      mydb.set("thread-safe-key", "value")
  ```

---

## **Contributing**

Contributions are welcome! Feel free to open an issue or submit a pull request on GitHub.

---

## **License**

This project is licensed under the BSD License. See the `LICENSE` file for details.

---

`pkldb` is your go-to choice for a simple, reliable, and fast key-value store. With proven performance at scale, it's the perfect tool for your next Python project. 🚀

