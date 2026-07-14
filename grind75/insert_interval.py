class Solution:
    def insert(
        self, intervals: list[list[int]], newInterval: list[int]
    ) -> list[list[int]]:
        result = []
        new_start, new_end = newInterval
        idx = 0
        current_start, current_end = new_start, new_end
        while idx < len(intervals):
            start, end = intervals[idx]
            if end < new_start:
                result.append(intervals[idx])
            else:
                current_start = min(start, current_start)
                break
            idx += 1

        if idx == len(intervals):
            result.append(newInterval)
            return result
        current_end = new_end
        while idx < len(intervals):
            # merge
            start, _ = intervals[idx]
            if start > new_end:
                break
            current_end = max(current_end, intervals[idx][1])
            idx += 1
        result.append([current_start, current_end])
        while idx < len(intervals):
            result.append(intervals[idx])
            idx += 1
        return result
