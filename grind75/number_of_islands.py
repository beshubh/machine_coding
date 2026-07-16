import collections

NEIGHBORS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


class Solution:
    def numIslands(self, grid: list[list[str]]) -> int:
        seen = set()
        ROWS = len(grid)
        COLS = len(grid[0])

        def bfs(r, c):
            q = collections.deque([(r, c)])
            seen.add((r, c))
            while q:
                row, col = q.popleft()
                for dr, dc in NEIGHBORS:
                    nr, nc = dr + row, dc + col
                    if (
                        nr >= 0
                        and nr < ROWS
                        and nc >= 0
                        and nc < COLS
                        and (nr, nc) not in seen
                        and grid[nr][nc] == "1"
                    ):
                        seen.add((nr, nc))
                        q.append((nr, nc))

        islands = 0
        for r in range(ROWS):
            for c in range(COLS):
                if grid[r][c] == "1" and (r, c) not in seen:
                    bfs(r, c)
                    islands += 1
        return islands
