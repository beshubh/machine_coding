MAP = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}


class Solution:
    def romanToInt(self, s: str) -> int:
        stack = []
        for i, ch in enumerate(reversed(s)):
            if ch not in MAP:
                raise ValueError(f"No such roman: {ch}")
            num = MAP[ch]
            if stack:
                if num < stack[-1]:
                    stack.append(-num)
                else:
                    stack.append(num)
            else:
                stack.append(num)
        return sum(stack)
