import collections


class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        s_counter = collections.Counter(s)
        t_counter = collections.Counter(t)
        for c in s:
            if s_counter[c] != t_counter[c]:
                return False
        return True


class Solution2:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        s_counter = collections.Counter(s)
        for c in t:
            s_counter[c] -= 1
            if s_counter[c] < 0:
                return False
        return True
