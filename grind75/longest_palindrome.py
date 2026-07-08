import collections


class Solution:
    def longestPalindrome(self, s: str) -> int:
        counter = collections.Counter(s)
        result = 0
        for ch in set(s):
            if counter[ch] % 2 == 0:
                result += counter[ch]
            else:
                result += counter[ch] - 1

        for ch in set(s):
            if counter[ch] % 2 != 0:
                result += 1
                break
        return result
