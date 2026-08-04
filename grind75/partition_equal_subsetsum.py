class Solution:
    def canPartition(self, nums: list[int]) -> bool:
        cache = {}
        total_sum = sum(nums)
        # two partitions subset means
        # let two subsets sums be a and b
        # return true on a == b
        # for two sums to be equal: a and b have to include all the elements of the nums
        # a + b = total_sum
        # a = total_sum - a
        # to prove a = b
        # a = total_sum - a
        # 2a = total_sum
        # a = total_sum / 2
        # if we can prove a == total_sum / 2 we can prove that there are two subsets with equal sum
        if total_sum % 2 != 0:
            return False

        # recursion
        def go(i: int, current_sum: int):
            key = (i, current_sum)
            if i >= len(nums):
                return current_sum == (total_sum + 1) // 2
            if key in cache:
                return cache[key]
            c1 = go(i + 1, current_sum + nums[i])
            c2 = go(i + 1, current_sum)
            cache[key] = c1 or c2
            return c1 or c2

        # iterative
        half = total_sum // 2
        dp = [[False for _ in range(half + 1)] for _ in range(len(nums) + 1)]
        for i in range(len(nums) + 1):
            dp[i][half] = True

        for i in range(len(nums) - 1, -1, -1):
            for j in range(half - 1, -1, -1):
                if j + nums[i] <= half:
                    dp[i][j] = dp[i + 1][j + nums[i]] or dp[i + 1][j]
                else:
                    dp[i][j] = dp[i + 1][j]
        return dp[0][0]
