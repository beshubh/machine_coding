class Solution:
    def climbStairs(self, n: int) -> int:
        cache = {}

        def inner(s):
            if s in cache:
                return cache[s]
            if s >= n:
                return 1
            cache[s] = inner(s + 1) + inner(s + 2)
            return cache[s]

        return inner(1)
