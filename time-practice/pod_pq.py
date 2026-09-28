import heapq


def process(ops: list[str]) -> list[str]:
    pq = []
    result = []
    offset = 0
    podset = set()
    for op in ops:
        parts = op.split(maxsplit=3)
        kind = parts[0]
        match kind:
            case "ADD":
                pid, p = parts[1], int(parts[2])
                podset.add(pid)
                heapq.heappush(
                    pq,
                    (
                        p - offset,
                        pid,
                    ),
                )
            case "POP":
                while pq and pq[0][1] not in podset:
                    heapq.heappop(pq)
                if pq:
                    s, pid = heapq.heappop(pq)
                    podset.remove(pid)
                    result.append(f"{pid} {s + offset}")
                else:
                    result.append("EMPTY")
            case "INC":
                offset += int(parts[1])
            case "REMOVE":
                pid = parts[1]
                podset.discard(pid)

    return result


if __name__ == "__main__":
    ops = [
        "ADD a 5",
        "ADD b 3",
        "INC 2",
        "ADD c 4",
        "POP",
        "INC 1",
        "POP",
        "POP",
        "POP",
    ]
    print(process(ops))
