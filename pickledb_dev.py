"""
Copyright Harrison Erd

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

1. Redistributions of source code must retain the above copyright
notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright
notice, this list of conditions and the following disclaimer in the
documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
contributors may be used to endorse or promote products derived from
this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
from __future__ import annotations

import asyncio
import math
import os
import threading
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

import aiofiles
import orjson


_VEC_KEY = "__pvindex__"  # { key: [floats...] }


def _cosine(a: Sequence[float], b: Sequence[float]) -> float:
    # Safe cosine similarity without numpy
    if not a or not b:
        return 0.0
    la = math.sqrt(sum(x * x for x in a))
    lb = math.sqrt(sum(x * x for x in b))
    if la == 0.0 or lb == 0.0:
        return 0.0
    # Use shortest length if vectors differ (graceful handling)
    n = min(len(a), len(b))
    dot = sum(a[i] * b[i] for i in range(n))
    return dot / (la * lb)


def _normalize_key(key: Any) -> str:
    return str(key)


class PickleDB:
    """
    A minimal orjson-based K/V store with optional autosave and a simple built-in vector index.

    Features
    - Thread-safe (RLock) for free-threaded Python (no GIL).
    - Atomic, durable save (temp file + fsync + replace).
    - Optional autosave on set/remove/purge/vector changes.
    - Lightweight vector index for approximate "semantic" lookups via cosine similarity.
      (You provide embeddings; we store and search them.)

    Notes
    - Vectors are persisted under the reserved key `_VEC_KEY`.
    - You can ignore vector APIs if you don't need them.
    """

    def __init__(self, location: str, *, autosave: bool = False):
        self.location = os.path.expanduser(location)
        self._lock = threading.RLock()
        self._autosave = autosave
        self.db: Dict[str, Any] = {}
        self._vecs: Dict[str, List[float]] = {}
        self._load()

    # Syntax sugar
    def __setitem__(self, key: Any, value: Any):
        self.set(key, value)

    def __getitem__(self, key: Any):
        return self.get(key)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.save()
        return False

    # IO
    def _load(self):
        with self._lock:
            if os.path.exists(self.location) and os.path.getsize(self.location) > 0:
                try:
                    with open(self.location, "rb") as f:
                        data = orjson.loads(f.read())
                except Exception as e:
                    raise RuntimeError(f"{e}\nFailed to load database.")
            else:
                data = {}

            # Extract vectors & user data
            vecs = data.pop(_VEC_KEY, {})
            if not isinstance(vecs, dict):
                vecs = {}
            self.db = data
            # Ensure vectors are lists of floats
            cleaned: Dict[str, List[float]] = {}
            for k, v in vecs.items():
                if isinstance(v, (list, tuple)) and all(isinstance(x, (int, float)) for x in v):
                    cleaned[k] = [float(x) for x in v]
            self._vecs = cleaned

    def save(self, option: int = 0) -> bool:
        """
        Persist atomically with fsync durability.
        """
        temp_location = f"{self.location}.tmp"
        with self._lock:
            try:
                # Compose payload including vectors
                payload = dict(self.db)
                if self._vecs:
                    payload[_VEC_KEY] = self._vecs

                with open(temp_location, "wb") as tf:
                    tf.write(orjson.dumps(payload, option=option))
                    tf.flush()
                    os.fsync(tf.fileno())

                os.replace(temp_location, self.location)
                dir_fd = os.open(os.path.dirname(self.location) or ".", os.O_DIRECTORY)
                try:
                    os.fsync(dir_fd)
                finally:
                    os.close(dir_fd)
                return True
            except Exception as e:
                print(f"Failed to save database: {e}")
                return False

    # Key/Value
    def set(self, key: Any, value: Any, *, autosave: Optional[bool] = None) -> bool:
        with self._lock:
            self.db[_normalize_key(key)] = value
            if (self._autosave if autosave is None else autosave):
                self.save()
            return True

    def get(self, key: Any) -> Any:
        with self._lock:
            return self.db.get(_normalize_key(key))

    def remove(self, key: Any, *, autosave: Optional[bool] = None) -> bool:
        k = _normalize_key(key)
        with self._lock:
            ok = False
            if k in self.db:
                del self.db[k]
                ok = True
            if k in self._vecs:  # also remove vector, if any
                del self._vecs[k]
                ok = True
            if ok and (self._autosave if autosave is None else autosave):
                self.save()
            return ok

    def purge(self, *, autosave: Optional[bool] = None) -> bool:
        with self._lock:
            self.db.clear()
            self._vecs.clear()
            if (self._autosave if autosave is None else autosave):
                self.save()
            return True

    def all(self) -> List[str]:
        with self._lock:
            return list(self.db.keys())

    # Vectors
    def set_vector(self, key: Any, vector: Iterable[float], *, autosave: Optional[bool] = None) -> None:
        """
        Attach/update an embedding vector for `key`.
        """
        k = _normalize_key(key)
        vec = [float(x) for x in vector]
        with self._lock:
            self._vecs[k] = vec
            if (self._autosave if autosave is None else autosave):
                self.save()

    def get_vector(self, key: Any) -> Optional[List[float]]:
        with self._lock:
            return list(self._vecs.get(_normalize_key(key), [])) or None

    def remove_vector(self, key: Any, *, autosave: Optional[bool] = None) -> bool:
        k = _normalize_key(key)
        with self._lock:
            existed = self._vecs.pop(k, None) is not None
            if existed and (self._autosave if autosave is None else autosave):
                self.save()
            return existed

    def set_with_vector(
        self, key: Any, value: Any, vector: Iterable[float], *, autosave: Optional[bool] = None
    ) -> None:
        """
        Convenience: set value and vector for the same key in one shot.
        """
        k = _normalize_key(key)
        vec = [float(x) for x in vector]
        with self._lock:
            self.db[k] = value
            self._vecs[k] = vec
            if (self._autosave if autosave is None else autosave):
                self.save()

    def search_vector(
        self,
        query_vector: Sequence[float],
        *,
        top_k: int = 5,
        min_score: Optional[float] = None,
        filter_keys: Optional[Iterable[str]] = None,
    ) -> List[Tuple[str, float]]:
        """
        Return top_k (key, score) by cosine similarity.
        """
        q = [float(x) for x in query_vector]
        with self._lock:
            keys = set(filter_keys) if filter_keys else None
            scores: List[Tuple[str, float]] = []
            for k, v in self._vecs.items():
                if keys and k not in keys:
                    continue
                s = _cosine(q, v)
                if min_score is None or s >= min_score:
                    scores.append((k, s))
            scores.sort(key=lambda kv: kv[1], reverse=True)
            return scores[: max(0, top_k)]


class AsyncPickleDB:
    """
    Fully-async variant with the same API shape.
    Safe for no-GIL as long as you confine an instance to a single event loop/thread.

    If you need cross-thread access to the SAME instance, add a separate `threading.RLock`
    around all public methods (or keep one instance per loop/thread).
    """

    def __init__(self, location: str, *, autosave: bool = False):
        self.location = os.path.expanduser(location)
        self._lock = asyncio.Lock()
        self._autosave = autosave
        self.db: Dict[str, Any] = {}
        self._vecs: Dict[str, List[float]] = {}

    async def __aenter__(self):
        await self.aload()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            await self.asave()
        return False

    # I/O
    async def aload(self):
        async with self._lock:
            if os.path.exists(self.location) and os.path.getsize(self.location) > 0:
                try:
                    async with aiofiles.open(self.location, "rb") as f:
                        content = await f.read()
                    data = orjson.loads(content)
                except Exception as e:
                    raise RuntimeError(f"{e}\nFailed to load database.")
            else:
                data = {}

            vecs = data.pop(_VEC_KEY, {})
            if not isinstance(vecs, dict):
                vecs = {}
            self.db = data

            cleaned: Dict[str, List[float]] = {}
            for k, v in vecs.items():
                if isinstance(v, (list, tuple)) and all(isinstance(x, (int, float)) for x in v):
                    cleaned[k] = [float(x) for x in v]
            self._vecs = cleaned

    async def asave(self, option: int = 0) -> bool:
        temp_location = f"{self.location}.tmp"
        async with self._lock:
            try:
                payload = dict(self.db)
                if self._vecs:
                    payload[_VEC_KEY] = self._vecs

                # Write temp file
                async with aiofiles.open(temp_location, "wb") as temp_file:
                    await temp_file.write(orjson.dumps(payload, option=option))
                    await temp_file.flush()

                # Replace & fsync directory on a thread to avoid blocking the event loop
                def _replace_and_sync():
                    os.replace(temp_location, self.location)
                    dir_fd = os.open(os.path.dirname(self.location) or ".", os.O_DIRECTORY)
                    try:
                        os.fsync(dir_fd)
                    finally:
                        os.close(dir_fd)

                await asyncio.to_thread(_replace_and_sync)
                return True
            except Exception as e:
                print(f"Failed to save database: {e}")
                return False

    # Key/Value
    async def aset(self, key: Any, value: Any, *, autosave: Optional[bool] = None) -> bool:
        async with self._lock:
            self.db[_normalize_key(key)] = value
            do_save = self._autosave if autosave is None else autosave
        if do_save:
            await self.asave()
        return True

    async def aget(self, key: Any) -> Any:
        async with self._lock:
            return self.db.get(_normalize_key(key))

    async def aremove(self, key: Any, *, autosave: Optional[bool] = None) -> bool:
        k = _normalize_key(key)
        ok = False
        async with self._lock:
            if k in self.db:
                del self.db[k]
                ok = True
            if k in self._vecs:
                del self._vecs[k]
                ok = True
            do_save = ok and (self._autosave if autosave is None else autosave)
        if do_save:
            await self.asave()
        return ok

    async def apurge(self, *, autosave: Optional[bool] = None) -> bool:
        async with self._lock:
            self.db.clear()
            self._vecs.clear()
            do_save = self._autosave if autosave is None else autosave
        if do_save:
            await self.asave()
        return True

    async def aall(self) -> List[str]:
        async with self._lock:
            return list(self.db.keys())

    # Vectors
    async def aset_vector(self, key: Any, vector: Iterable[float], *, autosave: Optional[bool] = None) -> None:
        k = _normalize_key(key)
        vec = [float(x) for x in vector]
        async with self._lock:
            self._vecs[k] = vec
            do_save = self._autosave if autosave is None else autosave
        if do_save:
            await self.asave()

    async def aget_vector(self, key: Any) -> Optional[List[float]]:
        async with self._lock:
            return list(self._vecs.get(_normalize_key(key), [])) or None

    async def aremove_vector(self, key: Any, *, autosave: Optional[bool] = None) -> bool:
        k = _normalize_key(key)
        async with self._lock:
            existed = self._vecs.pop(k, None) is not None
            do_save = existed and (self._autosave if autosave is None else autosave)
        if do_save:
            await self.asave()
        return existed

    async def aset_with_vector(
        self, key: Any, value: Any, vector: Iterable[float], *, autosave: Optional[bool] = None
    ) -> None:
        k = _normalize_key(key)
        vec = [float(x) for x in vector]
        async with self._lock:
            self.db[k] = value
            self._vecs[k] = vec
            do_save = self._autosave if autosave is None else autosave
        if do_save:
            await self.asave()

    async def asearch_vector(
        self,
        query_vector: Sequence[float],
        *,
        top_k: int = 5,
        min_score: Optional[float] = None,
        filter_keys: Optional[Iterable[str]] = None,
    ) -> List[Tuple[str, float]]:
        q = [float(x) for x in query_vector]
        async with self._lock:
            keys = set(filter_keys) if filter_keys else None
            scores: List[Tuple[str, float]] = []
            for k, v in self._vecs.items():
                if keys and k not in keys:
                    continue
                s = _cosine(q, v)
                if min_score is None or s >= min_score:
                    scores.append((k, s))
        scores.sort(key=lambda kv: kv[1], reverse=True)
        return scores[: max(0, top_k)]

