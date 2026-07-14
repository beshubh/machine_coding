class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        nums.sort()
        result = []
        i = 0
        while i < len(nums):
            left, right = i + 1, len(nums) - 1
            while left < right:
                s = nums[i] + nums[left] + nums[right]
                if s == 0:
                    result.append([nums[i], nums[left], nums[right]])
                    left += 1
                    right -= 1
                    while left < right and nums[left - 1] == nums[left]:
                        left += 1
                    while (
                        left < right
                        and right + 1 < len(nums)
                        and nums[right + 1] == nums[right]
                    ):
                        right -= 1
                elif s < 0:
                    left += 1
                    while left < right and nums[left - 1] == nums[left]:
                        left += 1
                else:
                    right -= 1

                    while (
                        left < right
                        and right + 1 < len(nums)
                        and nums[right + 1] == nums[right]
                    ):
                        right -= 1

            i += 1
            while i < len(nums) and nums[i - 1] == nums[i]:
                i += 1
        return result
