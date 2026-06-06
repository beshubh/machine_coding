import threading
import collections

class Trigger:
    def __init__(self):
        self._fired = False
        self._condition = threading.Condition()

    def wait(self):
        with self._condition:
            while not self._fired:
                self._condition.wait()

    def fire(self):
        with self._condition:
            self._fired = True
            self._condition.notify_all()




class BlockingBox:
    def __init__(self):
        self._cond = threading.Condition()
        self._has_value = False
        self._value = None

    def put(self, x):
        with self._cond:
            while self._has_value:
                self._cond.wait()

            self._value = x
            self._has_value = True
            self._cond.notify_all()

    def get(self):
        with self._cond:
            while not self._has_value:
                self._cond.wait()

            value = self._value
            self._has_value = False
            self._value = None
            self._cond.notify_all()
            return value



class BoundedQueue[T]:

    def __init__(self, capacity: int):
        self._q = collections.deque()
        self._capacity = capacity

        self._cond = threading.Condition()

    def put(self, x):
        with self._cond:
            while len(self._q) >= self._capacity:
                self._cond.wait()
            self._q.appendleft(x)
            self._cond.notify_all()

    def get(self):
        with self._cond:
            while len(self._q) == 0:
                self._cond.wait()
            item = self._q.pop()
            self._cond.notify_all()
            return item


def wait_until(cond, predicate, timeout=None):
    with cond:
        while not predicate:
            if not cond.wait(timeout=timeout):
                return predicate()
        return True
