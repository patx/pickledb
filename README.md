[![PyPI Downloads](https://static.pepy.tech/badge/pickledb)](https://pepy.tech/projects/pickledb)

[![Logo](https://patx.github.io/pickledb/logo.png)](https://patx.github.io/pickledb)

# **pickleDB: Your Lightweight, High-Speed Key-Value Store**

### 💡 **Getting Started**
Check out pickleDB's [website](https://patx.github.io/pickledb) for installation instructions, a [user guide](https://patx.github.io/pickledb/guide) complete with advanced examples and the complete [API documentation](https://patx.github.io/pickledb/commands).

### 💫 **Blazing Speed**
Backed by the high-performance [orjson](https://pypi.org/project/orjson/) library, pickleDB handles millions of records with ease. Perfect for applications where every millisecond counts.

### 😋 **Ridiculously Easy to Use**
With its minimalist API, pickleDB makes adding, retrieving, and managing your data as simple as writing a Python list. No steep learning curves. No unnecessary complexity.

### 🔒 **Rock-Solid Reliability**
Your data deserves to be safe. Atomic saves ensure your database remains consistent—even if something goes wrong.

### 🐍 **Pythonic Flexibility**
Store strings, lists, dictionaries, and more—all with native Python operations. No need to learn special commands. If you know Python, you already know pickleDB.

### ⚡ **Async Support**
Use pickleDB's `AsyncPickleDB` class for async operations and saves made possible with aiofiles. Ready to go for use with web frameworks like Starlette, FastAPI, and [MicroPie](https://patx.github.io/micropie).

### 💢 **Limitations**
The entire dataset is loaded into memory, which might be a constraint on systems with limited RAM for extremely large datasets. pickleDB is designed for simplicity, so it may not 
meet the needs of applications requiring advanced database features. For projects requiring more robust solutions, consider alternatives like [kenobiDB](Https://github.com/patx/kenobi), 
[Redis](http://redis.io/), [SQLite](https://www.sqlite.org/), or [MongoDB](https://www.mongodb.com/).

### 🙋 **Community & Contributions**
We’re passionate about making pickleDB better every day. Got ideas, feedback, or an issue to report? Let’s connect on [GitHub Issues](https://github.com/patx/pickledb/issues)


## **Performance Highlights**
pickleDB demonstrates strong performance for handling large-sized datasets:

| Entries      | Memory Load Time | Retrieval Time | Save Time |
|--------------|------------------|----------------|-----------|
| **1M**       | 1.21 sec         | 0.90 sec       | 0.17 sec  |
| **10M**      | 14.11 sec        | 10.30 sec      | 1.67 sec  |
| **50M**      | 93.79 sec        | 136.42 sec     | 61.08 sec |

Tests were performed on a StarLabs StarLite Mk IV (Quad-Core Intel® Pentium® Silver N5030 CPU @ 1.10GHz w/ 8GB memory) running elementary OS 7.1 Horus.
