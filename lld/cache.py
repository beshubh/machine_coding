import threading
from abc import ABC, abstractmethod
from collections import defaultdict
from collections.abc import Hashable
from typing import Any


class EvictionPolicy[K: Hashable](ABC):
    @abstractmethod
    def on_insert(self, key: K) -> None: ...

    @abstractmethod
    def on_access(self, key: K) -> None: ...

    @abstractmethod
    def on_remove(self, key: K) -> None: ...

    @abstractmethod
    def evict(self) -> K | None:
        """Remove and return the key to evict or null if empty"""


class Node[K: Hashable]:
    def __init__(self, key: K | None = None) -> None:
        self.key = key
        self.freq = 0
        self.prev: Node[K] | None = None
        self.next: Node[K] | None = None


class DoublyLinkedList[K: Hashable]:
    def __init__(self) -> None:
        self.head: Node[K] = Node()
        self.tail: Node[K] = Node()

        self.head.next, self.tail.prev = self.tail, self.head
        self.size = 0

    def append(self, node: Node[K]) -> None:
        last = self.tail.prev
        node.next, node.prev = self.tail, last
        last.next = self.tail.prev = node
        self.size += 1

    def remove(self, node: Node[K]) -> None:
        node.prev.next, node.next.prev = node.next, node.prev
        node.next = node.prev = None
        self.size -= 1

    def pop_front(self) -> Node[K] | None:
        if self.size == 0:
            return Node
        node = self.head.next
        if node is self.tail:
            return None
        self.remove(node)
        return node

    def __len__(self):
        return self.size


class LRUPolicy[K: Hashable](EvictionPolicy[K]):
    def __init__(self) -> None:
        self._nodes: dict[K, Node[K]] = {}
        self._list: DoublyLinkedList[K] = DoublyLinkedList()

    def on_insert(self, key: K) -> None:
        node = Node(key)
        self._nodes[key] = node
        self._list.append(node)

    def on_access(self, key: K) -> None:
        node = self._nodes[key]
        self._list.remove(node)
        self._list.append(node)

    def on_remove(self, key: K) -> None:
        node = self._nodes.pop(key, None)
        if node:
            self._list.remove(node)

    def evict(self) -> K | None:
        node = self._list.pop_front()
        if node is None:
            return None
        del self._nodes[node.key]
        return node.key


class LFUPolicy[K: Hashable](EvictionPolicy[K]):
    def __init__(self) -> None:
        self._nodes: dict[K, Node[K]] = {}
        self._buckets: dict[int, DoublyLinkedList[K]] = defaultdict(DoublyLinkedList)
        self._min_freq = 0

    def on_insert(self, key: K) -> None:
        node = Node(key)
        self._nodes[key] = node
        self._buckets[1].append(node)
        self._min_freq = 1

    def _unlink(self, node: Node[K]):
        bucket = self._buckets[node.freq]
        bucket.remove(node)
        if not bucket:
            del self._buckets[node.freq]

    def on_access(self, key: K) -> None:
        node = self._nodes[key]
        old = node.freq
        self._unlink(node)
        if self._min_freq == old and old not in self._buckets:
            self._min_freq += 1
        node.freq += 1
        self._buckets[node.freq].append(node)

    def on_remove(self, key: K) -> None:
        node = self._nodes.pop(key, None)
        if node is None:
            return
        self._unlink(node)
        if self._min_freq == node.freq and node.freq not in self._buckets:
            self._min_freq = min(self._buckets, default=0)

    def evict(self) -> K | None:
        if not self._nodes:
            return None
        bucket = self._buckets[self._min_freq]
        node = bucket.pop_front()
        if not bucket:
            del self._buckets[self._min_freq]
        del self._nodes[node.key]
        return node.key


class Cache[K: Hashable, V: Any]:
    def __init__(self, capacity: int, eviction_policy: EvictionPolicy[K]) -> None:
        self._capacity = capacity
        self._policy = eviction_policy

        self._store: dict[K, V] = {}
        self._lock = threading.Lock()

    def get(self, key: K) -> V | None:
        with self._lock:
            if key not in self._store:
                return None
            self._policy.on_access(key)
            return self._store[key]

    def put(self, key: K, value: V) -> None:
        with self._lock:
            if key in self._store:
                self._store[key] = value
                self._policy.on_access(key)
                return

            if len(self._store) >= self._capacity:
                victim = self._policy.evict()
                if victim is not None:
                    del self._store[victim]

            self._store[key] = value
            self._policy.on_insert(key)

    def delete(self, key: K) -> bool:
        with self._lock:
            if key not in self._store:
                return False
            del self._store[key]
            self._policy.on_remove(key)
            return True

    def __len__(self):
        return len(self._store)
