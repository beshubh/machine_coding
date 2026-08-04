class Solution:
    def myAtoi(self, s: str) -> int:
        acc = 0
        sign = 1
        read = False
        for i, c in enumerate(s):
            if not read:
                if c.isspace():
                    continue
                if c == "-":
                    read = True
                    sign = -1
                elif c == "+":
                    read = True
                    sign = 1
                elif c.isnumeric():
                    read = True
                    acc *= 10
                    acc += ord(c) - ord("0")
                else:
                    break
            else:
                if not c.isnumeric():
                    break
                read = True
                acc *= 10
                acc += ord(c) - ord("0")

        acc *= sign
        if acc < 0:
            return max(-(2**31), acc)
        return min(2**31 - 1, acc)
