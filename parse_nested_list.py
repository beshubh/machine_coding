def parseDepthWeightedSum(text):
    n = len(text)

    def build(i: int, depth: int = 0):
        stack = []
        acc = 0
        while i < n:  # Amortized O(N) | Space O(N)
            ch = text[i]
            match ch:
                case _ if ch.isspace():
                    pass
                case num if ch.isnumeric():
                    acc = acc * 10 + int(num)
                case ",":
                    stack.append(acc * depth)
                    acc = 0
                case "[":
                    i, value = build(i + 1, depth=depth + 1)
                    stack.append(value)
                    continue
                case "]":
                    stack.append(acc * depth)
                    acc = 0
                    return i + 1, sum(stack)
            i += 1
        return i, sum(stack)

    answer = build(0)[1]
    return answer


def main():
    assert parseDepthWeightedSum("[3, 8, [2, 14], [2, [91]]]") == 320


if __name__ == "__main__":
    main()
