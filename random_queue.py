import random
import collections


class RandomQueue:
    def __init__(self):
        self._items: list[int] = []
        self._head = 0

    def enqueue(self, value: int) -> None:
        self._items.append(value)

    def dequeue(self) -> int:
        if self._head == len(self._items):
            raise IndexError("Queue is emtpy")

        if self._head > 1000 and self._head * 2 >= len(self._items):
            self._items = self._items[self._head :]
            self._head = 0
        v = self._items[self._head]
        self._head += 1
        return v

    def get_random(self) -> int:
        if self._head == len(self._items):
            raise IndexError("Queue is emtpy")
        idx = random.randrange(self._head, len(self._items))
        return self._items[idx]


def run_tests():
    q = RandomQueue()

    q.enqueue(10)
    q.enqueue(20)
    q.enqueue(30)

    assert q.dequeue() == 10

    q.enqueue(40)

    # Queue is now logically: [20, 30, 40]

    for _ in range(100):
        value = q.get_random()
        assert value in {20, 30, 40}

    assert q.dequeue() == 20
    assert q.dequeue() == 30
    assert q.dequeue() == 40

    try:
        q.dequeue()
        assert False, "Expected dequeue() on empty queue to fail"
    except IndexError:
        pass

    try:
        q.get_random()
        assert False, "Expected get_random() on empty queue to fail"
    except IndexError:
        pass

    # duplicates
    q.enqueue(5)
    q.enqueue(5)
    q.enqueue(10)

    for _ in range(100):
        assert q.get_random() in {5, 10}

    print("All tests passed!")


if __name__ == "__main__":
    run_tests()
