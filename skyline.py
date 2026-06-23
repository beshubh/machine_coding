from __future__ import annotations
from dataclasses import dataclass
from sortedcontainers import SortedList


@dataclass
class BuildingPoint:
    x: int
    height: int
    isStart: bool

    def __lt__(self, b: BuildingPoint):
        # comparen by x
        if self.x != b.x:
            return self.x < b.x

        # if one is start and other is end, process the start event first
        if self.isStart != b.isStart:
            return self.isStart

        # if x's are same, and both are start, process larger height first
        if self.isStart and b.isStart:
            return self.height > b.height

        # if x's are same, both are ends, process smaller height first
        if not self.isStart and not b.isStart:
            return self.height < b.height


def compute_skyline(buildings):
    events = []
    for b in buildings:
        events.append(
            BuildingPoint(
                x=b[0],
                height=b[2],
                isStart=True
            )
        )
        events.append(
            BuildingPoint(
                x=b[1],
                height=b[2],
                isStart=False
            )
        )

    events.sort()
    heights = SortedList()
    heights.add(0)
    outputs = []
    for i in range(len(events)):
        current_max = heights[-1]
        event = events[i]
        if event.isStart:
            heights.add(event.height)
            new_max = heights[-1]
            if new_max != current_max:
                outputs.append([event.x, new_max])
        else:
            heights.remove(event.height)
            new_max = heights[-1]
            if new_max != current_max:
                outputs.append([event.x, new_max])
    return outputs



def solution():
    return compute_skyline([[2, 9, 10], [3, 7, 15], [5, 12, 12]])


if __name__ == '__main__':
    print(solution())
