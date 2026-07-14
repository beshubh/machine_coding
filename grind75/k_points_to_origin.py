import math
from heapq import heappop, heappush


class Solution:
    def kClosest(self, points: list[list[int]], k: int) -> list[list[int]]:

        def cmp(p):
            return math.sqrt(p[0] ** 2 + p[1] ** 2)

        pq = []
        for p in points:
            heappush(pq, (-cmp(p), p))
            if len(pq) > k:
                heappop(pq)
        return [p[1] for p in pq]
