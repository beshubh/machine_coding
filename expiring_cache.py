import heapq
import time
from dataclasses import dataclass
from typing import Any


@dataclass
class CacheEntry:
    data: Any
    exp: float


class ExpiringCache:
    def __init__(self):
        self._store: dict[str, CacheEntry] = {}
        self._expire_pq = []

    def put(self, key: str, value: str, ttl: float) -> None:
        exp = time.monotonic() + ttl
        self._store[key] = CacheEntry(data=value, exp=exp)
        heapq.heappush(self._expire_pq, (exp, key))

    def get(self, key: str) -> str | None:
        if key not in self._store:
            return None
        entry = self._store[key]
        if entry.exp <= time.monotonic():
            del self._store[key]
            return None
        return entry.data

    def cleanup(self) -> None:
        now = time.monotonic()
        while self._expire_pq and self._expire_pq[0][0] <= now:
            (exp, key) = heapq.heappop(self._expire_pq)

            entry = self._store.get(key)
            if entry is None:
                continue

            if entry.exp != exp:
                # stale heap entry
                continue
            del self._store[key]


def run_tests():
    cache = ExpiringCache()

    cache.put("a", "hello", 10)
    assert cache.get("a") == "hello"

    assert cache.get("missing") is None

    cache.put("b", "world", 0)
    assert cache.get("b") is None

    cache.put("x", "old", 10)
    cache.put("x", "new", 20)
    assert cache.get("x") == "new"

    cache.put("short", "value", 0.05)
    time.sleep(0.1)
    assert cache.get("short") is None

    cache.put("c", "foo", 0.05)
    cache.put("d", "bar", 10)

    time.sleep(0.1)
    cache.cleanup()

    assert cache.get("c") is None
    assert cache.get("d") == "bar"

    print("All tests passed!")


if __name__ == "__main__":
    run_tests()
