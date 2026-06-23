
import collections
from sortedcontainers import SortedList
from dataclasses import dataclass


class EventCounter:

    def __init__(self):
        self._events = collections.defaultdict(SortedList)

    def record_event(self, event_name: str, timestamp: int) -> None:
        self._events[event_name].add(timestamp)

    def get_counts_per_frequency(
        self,
        frequency: str,
        event_name: str,
        start_time: int,
        end_time: int
    ) -> list[int]:

        interval = {
            'minute': 60,
            'hour': 3600,
            'day': 86400,
            }[frequency]
        result = []
        bucket_start = start_time
        events = self._events[event_name]
        while bucket_start <= end_time:
            bucket_end = min(end_time, bucket_start + interval - 1)
            left = events.bisect_left(bucket_start)
            right = events.bisect_right(bucket_end)
            result.append(right - left)
            bucket_start += interval
        return result
