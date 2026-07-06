import collections


NEIGHBORS = [(0, 1), (0, -1), (1, 0), (-1, 0)]


class Solution:
    def floodFill(
        self, image: list[list[int]], sr: int, sc: int, color: int
    ) -> list[list[int]]:
        q = collections.deque([(sr, sc)])
        ROWS, COLS = len(image), len(image[0])
        start_color = image[sr][sc]
        while q:
            r, c = q.pop()
            if image[r][c] == color:
                continue
            image[r][c] = color
            for dr, dc in NEIGHBORS:
                nr, nc = r + dr, c + dc
                if (
                    nr >= 0
                    and nr < ROWS
                    and nc >= 0
                    and nc < COLS
                    and image[nr][nc] != color
                    and image[nr][nc] == start_color
                ):
                    q.appendleft((nr, nc))
        return image
