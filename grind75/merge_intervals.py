class Solution:
    def merge(self, intervals: list[list[int]]) -> list[list[int]]:
        if len(intervals) <= 0:
            return intervals
        intervals.sort()
        result = []
        start, end = intervals[0]
        for i in range(1, len(intervals)):
            s, e = intervals[i]
            if s <= end:
                end = max(end, e)
            else:
                result.append([start, end])
                start = s
                end = e
            if i == len(intervals) - 1:
                result.append([start, end])
        return result
