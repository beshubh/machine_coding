class MinStack:
    def __init__(self):
        self._stack = []
        self._min_stack = []

    def push(self, value: int) -> None:
        self._stack.append(value)
        if not self._min_stack or self._min_stack[-1][0] > value:
            self._min_stack.append((value, len(self._stack) - 1))

    def pop(self) -> None:
        idx = len(self._stack) - 1
        t = self.top()
        if self._min_stack[-1] == (t, idx):
            self._min_stack.pop()
        self._stack.pop()

    def top(self) -> int:
        return self._stack[-1]

    def getMin(self) -> int:
        return self._min_stack[-1][0]


# Your MinStack object will be instantiated and called as such:
# obj = MinStack()
# obj.push(value)
# obj.pop()
# param_3 = obj.top()
# param_4 = obj.getMin()
