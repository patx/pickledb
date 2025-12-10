#!/usr/bin/env python3
import argparse
import asyncio
import os
import time
from pathlib import Path

from pickledb import PickleDB


def human_bytes(n):
    """Return human-readable file size."""
    for unit in ["B", "KB", "MB", "GB"]:
        if n < 1024:
            return f"{n:.2f} {unit}"
        n /= 1024
    return f"{n:.2f} TB"


# ------------------------------------------------------------------------------
# SYNC BENCHMARKS
# ------------------------------------------------------------------------------

def bench_sync(db_path: Path, count: int):
    print(f"\n=== Sync Benchmark ({count:,} keys) ===")
    db = PickleDB(str(db_path))

    # SET
    t0 = time.perf_counter()
    for i in range(count):
        db.set(f"key_{i}", i)
    t1 = time.perf_counter()

    # GET
    for i in range(count):
        db.get(f"key_{i}")
    t2 = time.perf_counter()

    # SAVE
    db.save()
    t3 = time.perf_counter()

    set_rate = count / (t1 - t0)
    get_rate = count / (t2 - t1)
    save_time = t3 - t2
    file_size = human_bytes(os.path.getsize(db_path))

    print(f"SET:   {set_rate:,.0f} ops/sec  ({t1 - t0:.2f}s)")
    print(f"GET:   {get_rate:,.0f} ops/sec  ({t2 - t1:.2f}s)")
    print(f"SAVE:                ({save_time:.2f}s)")
    print(f"File size: {file_size}")


# ------------------------------------------------------------------------------
# ASYNC BENCHMARKS
# ------------------------------------------------------------------------------

async def bench_async(db_path: Path, count: int):
    print(f"\n=== Async Benchmark ({count:,} keys) ===")
    db = PickleDB(str(db_path))

    # SET
    t0 = time.perf_counter()
    for i in range(count):
        await db.set(f"key_{i}", i)
    t1 = time.perf_counter()

    # GET
    for i in range(count):
        await db.get(f"key_{i}")
    t2 = time.perf_counter()

    # SAVE
    await db.save()
    t3 = time.perf_counter()

    set_rate = count / (t1 - t0)
    get_rate = count / (t2 - t1)
    save_time = t3 - t2
    file_size = human_bytes(os.path.getsize(db_path))

    print(f"SET:   {set_rate:,.0f} ops/sec  ({t1 - t0:.2f}s)")
    print(f"GET:   {get_rate:,.0f} ops/sec  ({t2 - t1:.2f}s)")
    print(f"SAVE:                ({save_time:.2f}s)")
    print(f"File size: {file_size}")


# ------------------------------------------------------------------------------
# CLI ENTRY
# ------------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="PickleDB performance benchmark.")
    parser.add_argument(
        "-n", "--count",
        type=int,
        default=100_000,
        help="Number of key-value pairs (default: 100k)"
    )
    parser.add_argument(
        "--async",
        action="store_true",
        dest="async_mode",
        help="Run async version instead of sync"
    )
    parser.add_argument(
        "--db",
        type=str,
        default="benchmark_db.json",
        help="Database filename (default: benchmark_db.json)"
    )

    args = parser.parse_args()
    db_path = Path(args.db)

    # Remove file if exists
    if db_path.exists():
        db_path.unlink()

    if args.async_mode:
        asyncio.run(bench_async(db_path, args.count))
    else:
        bench_sync(db_path, args.count)


if __name__ == "__main__":
    main()

