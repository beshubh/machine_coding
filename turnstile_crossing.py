from collections import deque


class Turnstile:
    ENTER = 0
    EXIT = 1

    def __init__(self, time: list[int], direction: list[int]):
        self._time = time
        self._direction = direction
        self._answer = [-1] * len(time)

        self._clock = 0
        self._cur = 0
        self._enterq = deque()
        self._exitq = deque()

        self._prev_direction = self.EXIT
        self._used_prev_second = False

    def _add_arrivals(self):
        while self._cur < len(self._time) and self._time[self._cur] <= self._clock:
            if self._direction[self._cur] == self.EXIT:
                self._exitq.append(self._cur)
            else:
                self._enterq.append(self._cur)
            self._cur += 1


    def _choose_direction(self):
        # if the turnstile was not used, then we prefer the previous direction
        # if the turnstiel was not sued, prefer exit
        pref = self._prev_direction if self._used_prev_second else self.EXIT
        if pref == self.EXIT and self._exitq:
            return self.EXIT
        if pref == self.ENTER and self._enterq:
            return self.ENTER

        # covering the edge case
        return self.EXIT if pref == self.ENTER else self.ENTER


    def step(self):
        # on each step add all the arrivals with time <= current clocks
        self._add_arrivals()
        if not self._enterq and not self._exitq:
            if self._cur == len(self._time):
                return False
            self._clock += 1
            self._used_prev_second = False
            return True
        dir = self._choose_direction()
        if dir == self.ENTER:
            person = self._enterq.popleft()
        else:
            person = self._exitq.popleft()

        self._answer[person] = self._clock
        self._used_prev_second = True
        self._prev_direction = dir
        self._clock += 1
        return True

    def run(self):
        while self.step():
            pass
        return self._answer


def solution(time: list[int], direction: list[int]):
    return Turnstile(time, direction).run()


if __name__ == "__main__":
    assert solution([0, 0, 1, 5], [0, 1, 1, 0]) == [2, 0, 1, 5]
    assert solution([0, 1, 1, 3, 3], [0, 1, 0, 0, 1]) == [0, 2, 1, 4, 3]
