class Solution:
    def productExceptSelf(self, nums: list[int]) -> list[int]:
        prefix = [0] * len(nums)
        suffix = [0] * len(nums)
        prefix[0] = nums[0]
        suffix[-1] = nums[-1]
        answer = [-1] * len(nums)

        # prefix build
        for i in range(1, len(nums)):
            prefix[i] = nums[i] * prefix[i - 1]

        for i in range(len(nums) - 2, -1, -1):
            suffix[i] = nums[i] * suffix[i + 1]

        for i in range(len(nums)):
            if i > 0 and i < len(nums) - 1:
                answer[i] = prefix[i - 1] * suffix[i + 1]
            else:
                if i == 0:
                    answer[i] = suffix[i + 1]
                else:
                    answer[i] = prefix[i - 1]
        return answer
