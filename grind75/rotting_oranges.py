import collections


NEIGHBORS = [(0, 1), (0, -1), (1, 0), (-1, 0)]


class Solution:
    def orangesRotting(self, grid: list[list[int]]) -> int:
        q = collections.deque()
        ROWS, COLS = len(grid), len(grid[0])

        for r in range(ROWS):
            for c in range(COLS):
                if grid[r][c] == 2:  # rotten
                    q.append([r, c])
        minutes = 0
        while q:
            qlen = len(q)
            rott = False
            for _ in range(qlen):
                [r, c] = q.popleft()
                for dr, dc in NEIGHBORS:
                    nr, nc = dr + r, dc + c
                    if (
                        nr >= 0
                        and nr < ROWS
                        and nc >= 0
                        and nc < COLS
                        and grid[nr][nc] == 1
                    ):
                        rott = True
                        grid[nr][nc] = 2
                        q.append([nr, nc])
            minutes += 1 if rott else 0

        for r in range(ROWS):
            for c in range(COLS):
                if grid[r][c] == 1:  # fresh
                    return -1

        return minutes
