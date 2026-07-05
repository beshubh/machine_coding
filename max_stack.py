from sortedcontainers import SortedList


class MaxStack:
    def __init__(self):
        self._stack = []
        self._sl = SortedList()

    def push(self, x: int) -> None:
        self._stack.append(x)
        self._sl.add((x, len(self._stack) - 1))

    def pop(self) -> int:
        while self._stack and self._stack[-1] is None:
            self._stack.pop()
        top = self._stack[-1]
        self._sl.remove((top, len(self._stack) - 1))
        return self._stack.pop()

    def top(self) -> int:
        while self._stack and self._stack[-1] is None:
            self._stack.pop()
        return self._stack[-1]

    def peekMax(self) -> int:
        return self._sl[-1][0]

    def popMax(self) -> int:
        mx = self._sl.pop(-1)
        self._stack[mx[1]] = None
        return mx[0]


# Your MaxStack object will be instantiated and called as such:
# obj = MaxStack()
# obj.push(x)
# param_2 = obj.pop()
# param_3 = obj.top()
# param_4 = obj.peekMax()
# param_5 = obj.popMax()
