def can_reach_target(
    transactions: list[int],
    target: int,
) -> bool:
    n = len(transactions)
    mid = n // 2
    left = transactions[:mid]
    right = transactions[mid:]

    def subset_sums(nums: list[int]) -> set[int]:
        sums = set()

        def go(i: int, current: int, used: bool):
            if i == len(nums):
                if used:
                    sums.add(current)
                return
            go(i + 1, current, used)
            go(i + 1, current + nums[i], True)

        go(0, 0, False)
        return sums

    left_sums = subset_sums(left)
    right_sums = subset_sums(right)
    if target in left_sums or target in right_sums:
        return True
    for x in left_sums:
        if target - x in right_sums:
            return True
    return False


def test_basic():
    assert can_reach_target([3, -2, 7, 1], 8) is True


def test_negative_values():
    assert can_reach_target([5, -3, 2], 4) is True


test_negative_values()


def test_impossible():
    assert can_reach_target([2, 4, 6], 5) is False


# test_impossible()


def test_single_element():
    assert can_reach_target([10], 10) is True


def test_single_element_no_match():
    assert can_reach_target([10], 5) is False


def test_zero_target_with_zero():
    assert can_reach_target([0, 2, 4], 0) is True


def test_zero_target_without_zero():
    assert can_reach_target([1, -1, 5], 0) is True


def test_empty_input():
    assert can_reach_target([], 0) is False


def test_duplicates():
    assert can_reach_target([3, 3, 3], 6) is True


def test_requires_multiple_negative_and_positive():
    assert can_reach_target([8, -4, -3, 10], 1) is True


def test_large_target():
    assert can_reach_target([1, 2, 3, 4], 100) is False
