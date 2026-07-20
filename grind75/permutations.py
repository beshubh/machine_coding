class Solution:
    def permute(self, nums: list[int]) -> list[list[int]]:
        output = []
        current = []
        used = set()
        n = len(nums)

        def go():
            if len(current) == n:
                output.append(current.copy())
                return
            for j in range(n):
                if j not in used:
                    used.add(j)
                    current.append(nums[j])
                    go()
                    used.remove(j)
                    current.pop()

        go()
        return output
