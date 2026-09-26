def matches(s: str, pattern: str) -> bool:

    def go(i: int, j: int):
        if i >= len(s) and j >= len(pattern):
            return True
        if j >= len(pattern):
            return False
        if i >= len(s):
            return all(c == "*" for c in pattern[j:])
        if s[i] == pattern[j]:
            return go(i + 1, j + 1)

        if pattern[j] == "*":
            return (
                go(i, j + 1)  # * matches 0 characters
                or go(i + 1, j)  # * consumes one character and stays active
            )
        return False

    return go(0, 0)


def matches_greedy(s: str, pattern: str) -> bool:

    i, j = 0, 0
    star = -1
    match_start = 0
    # hel.lowthere
    # h*.l^lo*re
    while i < len(s):
        if j < len(pattern) and pattern[j] == s[i]:
            i += 1
            j += 1
        elif j < len(pattern) and pattern[j] == "*":
            star = j
            match_start = i
            j += 1
        elif star != -1:
            match_start += 1
            i = match_start
            j = star + 1
        else:
            return False

    while j < len(pattern) and pattern[j] == "*":
        j += 1
    return j == len(pattern)


def run_tests():
    tests = [
        ("hello", "hello", True),
        ("hello", "hell", False),
        ("abcdef", "abc*", True),
        ("abcdef", "*def", True),
        ("abcdef", "a*f", True),
        ("abcdef", "abc*def", True),
        ("anything", "*", True),
        ("", "*", True),
        ("", "", True),
        ("", "abc", False),
        ("abcdefgh", "a*c*f*h", True),
        ("abcdefgh", "a*d*x", False),
        ("abcdef", "a**f", True),
        ("aaaaaaaaab", "a*b", True),
        ("xxabcxx", "abc", False),
    ]

    for i, (s, pattern, expected) in enumerate(tests, 1):
        actual = matches_greedy(s, pattern)
        assert actual == expected, (
            f"Test {i} failed: "
            f"matches({s!r}, {pattern!r}) "
            f"returned {actual}, expected {expected}"
        )

    print("All tests passed!")


if __name__ == "__main__":
    run_tests()
