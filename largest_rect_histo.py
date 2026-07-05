class Solution:
    def largestRectangleArea(self, heights: list[int]) -> int:
        # Trick
        # a increasing monotonic stack maintains all heights in strictly increasing order
        # a sentinel 0 at the end of the heights forces all heights to be considered.
        # if we encounter a height smaller than the stack top we should calculate the area
        # for all the heights that are larger than or equal to current because they cannot be
        # considered for the area calculation of future heights, this is because the current is
        # smallest of all (atleast the top) adding the current has the chance of decreasing the area so
        # we do the area calculation from the stack.
        # left boundary is maintained by the heigh left to the popped_idx, for 0 it will be -1
        # all this works because smallest height can make rectangles with heights >= itself
        # and all this is only O(N) because stacks elements are popped just once

        monotonic_stack = []
        heights.append(0)
        answer = 0
        for i in range(len(heights)):
            h = heights[i]
            while monotonic_stack and heights[monotonic_stack[-1]] >= h:
                popped_idx = monotonic_stack.pop()
                height = heights[popped_idx]
                left = -1
                if monotonic_stack:
                    left = monotonic_stack[-1]
                width = i - left - 1
                answer = max(answer, height * width)
            monotonic_stack.append(i)
        return answer
