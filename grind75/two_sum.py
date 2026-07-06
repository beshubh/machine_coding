class Solution:
    # brute force
    # two loops go from i -> n - 1, j -> (i + 1, n - 1)
    # return answer
    # time = O(N^2) | Space: O(1)
    # OPTIMIZATION
    # the goal is to find the pairs that sum to target.
    # if we sort the array
    # we can begin with the largest number and the smallest number
    # smallest = a[0] | largest = a[-1]
    # now two pairs, i, j if they are closer to the target that means we have go in the direction that will increase their sum. so move the left pointer forward
    # if the pair sum is greater than target then we have to move decrease right pointer.
    # sorting is gonna gurantee us that we don't discard any potential candidates
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        a = [(x, i) for i, x in enumerate(nums)]
        a.sort()
        left, right = 0, len(nums) - 1
        while left < right:
            s = a[left][0] + a[right][0]
            if s < target:
                left += 1

            elif s > target:
                right -= 1
            else:
                return [a[left][1], a[right][1]]
        raise ValueError("No solution found")
