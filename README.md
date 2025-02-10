[![PyPI Downloads](https://static.pepy.tech/badge/pickledb)](https://pepy.tech/projects/pickledb)

[![Logo](https://patx.github.io/pickledb/logo.png)](https://patx.github.io/pickledb)

# **pickleDB: Your Lightweight, High-Speed Key-Value Store**

**Fast. Simple. Reliable.** Unlock the power of effortless data storage with **pickleDB**—the no-fuss, blazing-fast key-value store designed for Python developers. Whether you're building a small script or a performant microservice, pickleDB delivers simplicity and speed with the reliability you can count on.

## **Why Choose pickleDB?**

### ✅ **Blazing Speed**
Backed by the high-performance [orjson](https://pypi.org/project/orjson/) library, pickleDB handles millions of records with ease. Perfect for applications where every millisecond counts.

### ✅ **Ridiculously Easy to Use**
With its minimalist API, pickleDB makes adding, retrieving, and managing your data as simple as writing a Python list. No steep learning curves. No unnecessary complexity.

### ✅ **Rock-Solid Reliability**
Your data deserves to be safe. Atomic saves ensure your database remains consistent—even if something goes wrong.

### ✅ **Pythonic Flexibility**
Store strings, lists, dictionaries, and more—all with native Python operations. No need to learn special commands. If you know Python, you already know pickleDB.

### ✅ **Async Support**
Use pickleDB's `AsyncPickleDB` class for async operations and saves made possible with aiofiles. Ready to go for use with web frameworks like Starlette, FastAPI, and [MicroPie](https://patx.github.io/micropie).

## **Getting Started**
### Check out pickleDB's [website](https://patx.github.io/pickledb) for a [user guide](https://patx.github.io/pickledb/guide) complete with advanced examples and the complete [API documentation](https://patx.github.io/pickledb/commands).


## **Performance Highlights**

pickleDB demonstrates strong performance for handling large-sized datasets:

| Entries      | Memory Load Time | Retrieval Time | Save Time |
|--------------|------------------|----------------|-----------|
| **1M**       | 1.21 sec         | 0.90 sec       | 0.17 sec  |
| **10M**      | 14.11 sec        | 10.30 sec      | 1.67 sec  |
| **50M**      | 93.79 sec        | 136.42 sec     | 61.08 sec |

Tests were performed on a StarLabs StarLite Mk IV (Quad-Core Intel® Pentium® Silver N5030 CPU @ 1.10GHz w/ 8GB memory) running elementary OS 7.1 Horus.

## **Limitations**

While pickleDB is powerful, it’s important to understand its limitations:

- **Memory Usage**: The entire dataset is loaded into memory, which might be a constraint on systems with limited RAM for extremely large datasets.
- **Single-Threaded**: The program is not thread-safe by default. For concurrent access, use the async class `AsyncPickleDB`.
- **Blocking Saves**: Saves are blocking by default. To achieve non-blocking saves, use the `AsyncPickleDB` class.
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
