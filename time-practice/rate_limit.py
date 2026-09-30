import collections
from dataclasses import dataclass


@dataclass
class ReqEntry:
    last_ts: int


def rate_limit(requests: list[tuple[int, str]], W: int, L: int) -> list[bool]:
    request_log: dict[str, collections.deque[int]] = collections.defaultdict(
        collections.deque
    )
    result = []
    for req in requests:
        ts, user = req
        if user not in request_log:
            request_log[user].append(ts)
            result.append(True)
        else:
            ts_log = request_log[user]
            while ts_log and ts_log[0] <= ts - W:
                ts_log.popleft()
            if len(ts_log) < L:
                ts_log.append(ts)
                result.append(True)
            else:
                result.append(False)

    return result


print(
    rate_limit([(1, "a"), (2, "a"), (3, "a"), (11, "a"), (12, "a"), (12, "b")], 10, 2)
)
