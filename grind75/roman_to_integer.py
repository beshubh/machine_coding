MAP = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}


class Solution:
    def romanToInt(self, s: str) -> int:
        answer = 0
        for i in reversed(range(len(s))):
            ch = s[i]
            if ch not in MAP:
                raise ValueError(f"No such roman: {ch}")
            num = MAP[ch]
            if i != len(s) - 1:
                if num < MAP[s[i + 1]]:
                    answer -= num
                else:
                    answer += num
            else:
                answer += num
        return answer
