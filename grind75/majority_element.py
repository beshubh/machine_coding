class Solution:
    def majorityElement(self, nums: list[int]) -> int:
        candidate = None
        votes = 0
        for num in nums:
            if votes == 0:
                candidate = num
            if num == candidate:
                votes += 1
            else:
                votes -= 1
        return candidate
