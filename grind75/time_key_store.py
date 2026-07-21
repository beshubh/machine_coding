import collections


class TimeMap:
    def __init__(self):
        self.store = collections.defaultdict(list)

    def set(self, key: str, value: str, timestamp: int) -> None:
        self.store[key].append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        if key not in self.store:
            return ""
        arr = self.store[key]
        left, right = 0, len(arr) - 1
        while left <= right:
            mid = left + (right - left) // 2
            mid_ts = arr[mid][0]
            if timestamp >= mid_ts:
                # if target timestamp was equal to mid ts we would have gone to right
                left = mid + 1
            else:
                # now equal case is handled so the target timestamp cannot ever be at mid so right = mid - 1 is correct
                right = mid - 1
        if right < 0:
            return ""
        return arr[right][1]


# Your TimeMap object will be instantiated and called as such:
# obj = TimeMap()
# obj.set(key,value,timestamp)
# param_2 = obj.get(key,timestamp)
#
#
