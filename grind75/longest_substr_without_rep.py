class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        window = {}
        left = 0
        answer = 0
        for right in range(len(s)):
            window[s[right]] = 1 + window.get(s[right], 0)
            while window[s[right]] > 1:
                window[s[left]] -= 1
                left += 1
            answer = max(answer, right - left + 1)
        return answer
