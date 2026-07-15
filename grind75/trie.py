from __future__ import annotations


class TrieNode:
    def __init__(self) -> None:
        self.children = {}
        self.is_end = False


class Trie:
    def __init__(self):
        self._root = TrieNode()

    def insert(self, word: str) -> None:
        current = self._root
        for w in word:
            if w not in current.children:
                current.children[w] = TrieNode()
            current = current.children[w]
        current.is_end = True

    def search(self, word: str) -> bool:
        current = self._root
        for w in word:
            if w not in current.children:
                return False
            current = current.children[w]
        return current.is_end

    def startsWith(self, prefix: str) -> bool:
        current = self._root
        for w in prefix:
            if w not in current.children:
                return False
            current = current.children[w]
        return True


# Your Trie object will be instantiated and called as such:
# obj = Trie()
# obj.insert(word)
# param_2 = obj.search(word)
# param_3 = obj.startsWith(prefix)
