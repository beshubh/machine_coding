import collections

NEIGHBORS = [(1, 0), (0, 1), (-1, 0), (0, -1)]


class Solution:
    def updateMatrix(self, mat: list[list[int]]) -> list[list[int]]:
        ROWS, COLS = len(mat), len(mat[0])
        result = [[-1] * COLS for _ in range(ROWS)]
        q = collections.deque()
        for r in range(ROWS):
            for c in range(COLS):
                if mat[r][c] == 0:
                    result[r][c] = 0
                    q.appendleft((r, c))
        while q:
            r, c = q.pop()
            for dr, dc in NEIGHBORS:
                nr, nc = r + dr, c + dc
                if (
                    nr >= 0
                    and nr < ROWS
                    and nc >= 0
                    and nc < COLS
                    and result[nr][nc] == -1  # not seen
                ):
                    result[nr][nc] = result[r][c] + 1
                    q.appendleft((nr, nc))
        return result
