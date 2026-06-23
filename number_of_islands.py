

class DSU:

    def __init__(self):
        self.rank = {}
        self.root = {}
        self.components = 0

    def add(self, node):
        self.root[node] = node
        self.rank[node] = 0
        self.components += 1

    def find(self, a):
        if self.root[a] != a:
            self.root[a] = self.find(self.root[a])
        return self.root[a]

    def union(self, a, b) -> bool:
        ra, rb = self.find(a), self.find(b) # O(1), amortized
        if ra == rb:
            # already connected
            return False
        if self.rank[rb] > self.rank[ra]:
            ra, rb = rb, ra
        self.root[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        self.components -= 1
        return True


NEIGHBORS = [
    (0, 1),
    (0, -1),
    (1, 0),
    (-1, 0)
]

def num_islands(m: int, n: int, positions: list[tuple[int, int]]) -> list[int]:
    output= []

    dsu = DSU() # Space: O(k)
    islands = set() # Space: O (k)
    for (r, c) in positions:  # Time O(K)
        if (r, c) in islands:
           output.append(dsu.components)
           continue
        dsu.add((r, c))
        islands.add((r, c))
        for (dr, dc) in NEIGHBORS: # constant
            nr, nc = dr + r, dc + c
            if nr < 0 or nr >= m or nc < 0 or nc >= n:
                continue
            if (nr, nc) in islands:
                dsu.union((r, c), (nr, nc)) # log(mn)
        output.append(dsu.components)

    # time: O(k.log(mn)), space: O(k)
    return output
