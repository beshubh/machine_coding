import collections


def count_windows(delta: list[int], k: int) -> int:
    seen_prefix_sums = collections.defaultdict(int)
    seen_prefix_sums[0] = 1
    s = ans = 0
    for i, d in enumerate(delta):
        s += d
        if s - k in seen_prefix_sums:
            ans += seen_prefix_sums[s - k]
        seen_prefix_sums[s] += 1
    return ans


print(count_windows([0, 0, 0], k=0))
print(count_windows([1, 2, -1, 1], k=2))
