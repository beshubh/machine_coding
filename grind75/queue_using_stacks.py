class MyQueue:
    def __init__(self):
        self._stack_push = []
        self._stack_pop = []

    def push(self, x: int) -> None:
        self._stack_push.append(x)

    def _populate_pop_stack(self):
        if not self._stack_pop:
            while self._stack_push:
                self._stack_pop.append(self._stack_push.pop())

    def pop(self) -> int:
        self._populate_pop_stack()
        if not self._stack_pop:
            raise ValueError("Queue is empty")
        return self._stack_pop.pop()

    def peek(self) -> int:
        self._populate_pop_stack()
        if not self._stack_pop:
            raise ValueError("Queue is empty")
        return self._stack_pop[-1]

    def empty(self) -> bool:
        return len(self._stack_pop) + len(self._stack_push) == 0


# Your MyQueue object will be instantiated and called as such:
# obj = MyQueue()
# obj.push(x)
# param_2 = obj.pop()
# param_3 = obj.peek()
# param_4 = obj.empty()
