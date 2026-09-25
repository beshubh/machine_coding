import heapq


DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]


def minimum_monster_cost(grid: list[list[str]]) -> int:
    rows = len(grid)
    cols = len(grid[0])
    pq = []
    start = None
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "S":
                start = (r, c)

    if start is None:
        return -1
    pq = [(0, start)]
    dist = [[1e9] * cols for _ in range(rows)]
    dist[start[0]][start[1]] = 0

    while pq:
        cost, (r, c) = heapq.heappop(pq)
        if grid[r][c] == "E":
            return cost
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if nr < 0 or nr >= rows or nc < 0 or nc >= cols:
                continue
            if grid[nr][nc] == "#":
                continue

            new_cost = cost + (1 if grid[nr][nc] == "M" else 0)
            if new_cost < dist[nr][nc]:
                dist[nr][nc] = new_cost
                heapq.heappush(pq, (new_cost, (nr, nc)))
    return -1


def minimum_monster_cost_path(grid: list[list[str]]) -> list[list[int]]:
    rows = len(grid)
    cols = len(grid[0])
    pq = []
    start = None
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "S":
                start = (r, c)

    if start is None:
        return []
    pq = [(0, start)]
    dist = [[1e9] * cols for _ in range(rows)]
    dist[start[0]][start[1]] = 0
    path = []
    parent = {}
    while pq:
        cost, (r, c) = heapq.heappop(pq)
        if grid[r][c] == "E":
            path = []
            cell = (r, c)
            while cell != start:
                path.append(list(cell))
                cell = parent[cell]
            path.append(list(start))
            return path[::-1]
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if nr < 0 or nr >= rows or nc < 0 or nc >= cols:
                continue
            if grid[nr][nc] == "#":
                continue

            new_cost = cost + (1 if grid[nr][nc] == "M" else 0)
            if new_cost < dist[nr][nc]:
                parent[(nr, nc)] = (r, c)
                dist[nr][nc] = new_cost
                heapq.heappush(pq, (new_cost, (nr, nc)))
    return []


def minimum_monster_cost_with_arbitrary_weights(grid: list[list[str]], costs) -> int:
    rows = len(grid)
    cols = len(grid[0])
    pq = []
    start = None
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "S":
                start = (r, c)

    if start is None:
        return -1
    pq = [(0, start)]
    dist = [[1e9] * cols for _ in range(rows)]
    dist[start[0]][start[1]] = 0

    while pq:
        cost, (r, c) = heapq.heappop(pq)
        if grid[r][c] == "E":
            return cost
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if nr < 0 or nr >= rows or nc < 0 or nc >= cols:
                continue
            if grid[nr][nc] == "#":
                continue

            new_cost = cost + costs[nr][nc]
            if new_cost < dist[nr][nc]:
                dist[nr][nc] = new_cost
                heapq.heappush(pq, (new_cost, (nr, nc)))
    return -1


def solve(grid):
    return minimum_monster_cost_path(grid)
