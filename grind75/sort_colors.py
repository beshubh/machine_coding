class Solution:
    def sortColors(self, nums: list[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        counts = [0] * 3
        for n in nums:
            counts[n] += 1
        i = 0
        for c in counts:
            while n := c and n > 0:
                nums[i] = c
                n -= 1
                i += 1
