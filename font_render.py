

# part 1
def solution1(font_map, ch):
    matrix = font_map[ch]
    output = []
    for row in matrix:
        output.append(' '.join([str(x) for x in row]))
    return '\n'.join(output)


print(solution1({'J': [[0, 1, 0], [0, 1, 0], [1, 0, 0]]}, 'J'))


# part 2

# run-length encoding
def solution2(bitmap):
    rows = len(bitmap)
    cols = 0
    if rows:
        cols = len(bitmap[0])

    result = [[[rows, cols]]]
    for row in bitmap:
        prev = None
        count = 0
        row_result = []
        for c in range(len(row)):
            if row[c] == prev:
                count += 1
            elif prev is None:
                count = 1
                prev = row[c]
            else:
                row_result.append([prev, count])
                prev = row[c]
                count = 1
        row_result.append([prev, count])
        result.append(row_result)
    return result


# decode rle
def solution(compressed):
    rows = compressed[0][0][0]
    cols = compressed[0][0][1]
    result = []
    for row in compressed[1:]:
        row_result = []
        for tup in row:
            bit = 0 if tup[0] == 1 else 1
            count = tup[1]
            for _ in range(count):
                row_result.append(bit)
        result.append(row_result)
    return result
