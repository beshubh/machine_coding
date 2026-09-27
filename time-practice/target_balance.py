def can_reach_target(
    transactions: list[int],
    target: int,
) -> bool:
    """
    Return True if there exists a non-empty subset of transactions
    whose sum equals target.

    Each transaction may be used at most once.
    Transactions may contain positive and negative integers.
    """
    n = len(transactions)
    mid = n // 2
    left = transactions[:mid]  # n / 2
    right = transactions[mid:]  # n / 2

    def subset_sums(nums: list[int]):  # M
        sums = set()  # space

        def go(i: int, current: int, used: bool):  # space O(M)
            if i >= len(nums):
                if used:
                    sums.add(current)
                return
            # two decisions # O(2 ^(M))
            # take
            go(i + 1, current + nums[i], True)
            # skip
            go(i + 1, current, used)

        go(0, 0, False)
        return sums

    left_sums = subset_sums(left)  # O(2^M)
    right_sums = subset_sums(right)  # O(2^M)

    # M = N / 2
    # time: O(2^(N/2)), space: O

    if not left_sums and not right_sums:
        return False
    if target in left_sums or target in right_sums:
        return True

    for s in left_sums:
        if target - s in right_sums:
            return True
    return False


def run_tests():
    tests = [
        ([3, -2, 7, 1], 8, True),
        ([5, -3, 2], 4, True),
        ([2, 4, 6], 5, False),
        ([10], 10, True),
        ([10], 5, False),
        ([0, 2, 4], 0, True),
        ([1, -1, 5], 0, True),
        ([], 0, False),
        ([3, 3, 3], 6, True),
        ([8, -4, -3, 10], 1, True),
        ([1, 2, 3, 4], 100, False),
        ([-5, -2, -3], -10, True),
        ([-5, -2, -3], 1, False),
        ([1000000000, -1000000000], 0, True),
        ([7, 7, -14], 0, True),
    ]

    for i, (transactions, target, expected) in enumerate(tests, 1):
        actual = can_reach_target(transactions, target)

        assert actual == expected, (
            f"Test {i} failed:\n"
            f"transactions = {transactions}\n"
            f"target = {target}\n"
            f"returned {actual}, expected {expected}"
        )

    print("All tests passed!")


if __name__ == "__main__":
    run_tests()
