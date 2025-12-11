[![Logo](https://patx.github.io/pickledb/logo.png)](https://patx.github.io/pickledb)

[pickleDB](https://patx.github.io/pickledb) is a fast, easy to use, in-memory Python 
key-value store with first class asynchronous support. It is built with the `orjson` 
module for extremely high performance. It is licensed under the BSD three-clause 
license. [Check out the website](https://patx.github.io/pickledb) for installation 
instructions, API docs, advanced examples, benchmarks, and more.

```python
from pickledb import PickleDB

db = PickleDB("example.json").load()
db.set("key", "value")

db.get("key")  # return "value"
```

