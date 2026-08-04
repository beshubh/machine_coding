class Solution:
    def wordBreak(self, s: str, wordDict: list[str]) -> bool:
        cache = {}

        def go(word: str):
            if word in cache:
                return cache[word]
            if len(word) == 0:
                return True
            for w in wordDict:
                if w == word:
                    cache[word] = True
                    return True
                if word.startswith(w):
                    if go(word[len(w) :]):
                        cache[word] = True
                        return True
            cache[word] = False
            return False

        return go(s)
