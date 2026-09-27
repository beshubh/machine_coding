from heapq import heappush, heappop


def dijkstra(graph: dict[int, list[tuple[int, int]]], src: int):

    dist = {src: 0}
    pq = [(0, src)]
    parent = {}
    while pq:
        d, u = heappop(pq)
        if d > dist[u]:
            continue

        for v, w in graph[u]:
            nd = d + w
            if nd < dist.get(v, float("inf")):
                dist[v] = nd
                parent[v] = u
                heappush(pq, (nd, v))
    return dist


def grid_dijkstra(grid: list[list[int]]):
    DIRECTIONS = ((0, 1), (0, -1), (1, 0), (-1, 0))

    R, C = len(grid), len(grid[0])

    dist = [[float("inf")] * C for _ in range(R)]
    dist[0][0] = grid[0][0]
    pq = [(grid[0][0], 0, 0)]
    while pq:
        d, r, c = heappop(pq)
        if d > dist[r][c]:
            continue
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and d + grid[nr][nc] < dist[nr][nc]:
                dist[nr][nc] = d + grid[nr][nc]
                heappush(pq, (dist[nr][nc], nr, nc))
    return dist[R - 1][C - 1]

