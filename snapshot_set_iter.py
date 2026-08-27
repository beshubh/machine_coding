from dataclasses import dataclass


@dataclass
class Record:
    value: int
    added_at: float
    removed_at: float = float("inf")


@dataclass
class IteratorState:
    offset: int
    snapshot: float
    limit: int


def solution(operations: list[str], args_list: list[list[int]]):
    history: list[Record] = []
    mp = {}
    result: list[int] = []
    iterators: list[IteratorState] = []
    clock = 0
    for i, op in enumerate(operations):
        args = args_list[i]
        match op:
            case "add":
                if args[0] not in mp:
                    clock += 1
                    history.append(Record(value=args[0], added_at=clock))
                    result.append(1)
                    mp[args[0]] = len(history) - 1
                else:
                    result.append(0)
            case "remove":
                if args[0] in mp:
                    clock += 1
                    record = history[mp[args[0]]]
                    record.removed_at = clock
                    del mp[record.value]
                    result.append(1)
                else:
                    result.append(0)
            case "contains":
                if args[0] in mp:
                    result.append(1)
                else:
                    result.append(0)
            case "iterator":
                iterators.append(
                    IteratorState(offset=0, snapshot=clock, limit=len(history))
                )
                result.append(len(iterators) - 1)
            case "next":
                handle = args[0]
                iter = iterators[handle]
                while iter.offset < iter.limit:
                    record = history[iter.offset]
                    if record.removed_at > iter.snapshot:
                        break
                    iter.offset += 1

                if iter.offset < iter.limit:
                    result.append(history[iter.offset].value)
                    iter.offset += 1
            case "has_next":
                handle = args[0]
                iter = iterators[handle]
                while iter.offset < iter.limit:
                    record = history[iter.offset]
                    if record.removed_at > iter.snapshot:
                        break
                    iter.offset += 1

                if iter.offset < iter.limit:
                    result.append(1)
                else:
                    result.append(0)
    return result
