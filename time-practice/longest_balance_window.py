def longest_balanced(produced: list[int], consumed: list[int]) -> int:
    best = 0
    first = {0: -1}
    s = 0
    for i, p, c in enumerate(zip(produced, consumed)):
        s += p - c
        if s in first:
            best = max(best, i - first[s])
        else:
            first[s] = i
    return best


if __name__ == "__main__":
    print(longest_balanced([3, 1, 2, 0, 4], [1, 2, 1, 2, 1]))
    print(longest_balanced([3, 1, 2, 0, 4, 5, 1], [1, 2, 1, 2, 1, 7, 2]))
