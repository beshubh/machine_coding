"""
You're given sorted ping timestamps for one sensor and a `queryTime`. Check the next five 60-second slots:

- slot k is `[queryTime + 60k, queryTime + 60(k+1))`, for k = 0 to 4
- a slot is **active** if it contains at least one ping

Return `false` if any **three consecutive slots are inactive**; otherwise return `true`.

Signature: `wasAlive(pingTimestamps: int[], queryTime: int) → boolean`

Examples:
- `[0,30,180]`, q=0 → `true`: slots 1 and 2 are empty, but that's only two in a row.
- `[0,20,240]`, q=0 → `false`: slots 1, 2 and 3 are all empty.
- `[59,60,179,300]`, q=0 → `true`: 300 falls outside the window.

Constraints: up to 200,000 pings, timestamps ≤ 1e9, `queryTime` ≤ 999,999,700.
"""

from bisect import bisect_left


def wasAlive(ping_timestamps: list[int], queryTime: int) -> bool:

    run = 0
    for k in range(5):
        s = queryTime + 60 * k
        e = s + 60
        i = bisect_left(ping_timestamps, s)
        if i < len(ping_timestamps) and ping_timestamps[i] < e:
            run = 0
        else:
            run += 1
            if run >= 3:
                return False
    return True
