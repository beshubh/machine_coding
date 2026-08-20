def unionIntervals(first: list[list[int]], second: list[list[int]]):
    intermediate = []
    i, j = 0, 0
    while i < len(first) and j < len(second):
        if first[i][0] < second[j][0]:
            intermediate.append(first[i])
            i += 1
        else:
            intermediate.append(second[j])
            j += 1

    while i < len(first):
        intermediate.append(first[i])
        i += 1

    while j < len(second):
        intermediate.append(second[j])
        j += 1
    if not intermediate:
        return []
    s, e = intermediate[0]
    result = []
    for i in range(1, len(intermediate)):
        start, end = intermediate[i]
        if start <= e:
            e = max(e, end)
        else:
            result.append([s, e])
            s, e = start, end
    result.append([s, e])
    return result


def main():
    print(unionIntervals([[1, 3], [7, 9]], [[2, 6], [8, 10], [12, 13]]))


if __name__ == "__main__":
    main()
