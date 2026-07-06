class Solution:
    def isPalindrome(self, s: str) -> bool:
        s = s.lower()
        temp = []
        for c in s:
            if c.isalnum():
                temp.append(c)
        temp = "".join(temp)
        left, right = 0, len(temp) - 1
        while left < right:
            if temp[left] != temp[right]:
                return False
            left += 1
            right -= 1
        return True
