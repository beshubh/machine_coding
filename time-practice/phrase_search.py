import collections


class PhraseSearch:
    def __init__(self, documents: dict[int, str]):
        """
        Build whatever index/state you need.

        documents:
            doc_id -> document text

        Documents contain lowercase words separated by spaces.
        """
        # index mapping from word -> {doc_id: [1, 2, 3]}
        self._index: dict[str, dict[int, list[int]]] = collections.defaultdict(
            lambda: collections.defaultdict(list)
        )
        for doc_id, content in documents.items():
            for pos, word in enumerate(content.split()):
                self._index[word][doc_id].append(pos)

    def search(self, phrase: str) -> list[int]:
        """
        Return document IDs containing the exact phrase as
        consecutive words, in ascending order.

        Example:
            document: "the quick brown fox"
            phrase:   "quick brown"

        matches because the words occur consecutively.
        """

        for word in phrase.split():
            if word not in self._index:
                return []

        words = phrase.split()
        if len(words) == 0:
            return []
        # start with the docs starting that has the starting word
        candidate_docs = set(self._index[words[0]].keys())

        for word in words[1:]:
            candidate_docs &= self._index[word].keys()
            if not candidate_docs:
                return []
        result = []
        for doc_id in candidate_docs:
            first_positions = self._index[words[0]][doc_id]

            later_positions = [set(self._index[word][doc_id]) for word in words[1:]]

            for start in first_positions:
                matched = True
                for offset, positions in enumerate(later_positions, 1):
                    if start + offset not in positions:
                        matched = False
                        break
                if matched:
                    result.append(doc_id)
                    break

        return result


def run_tests():
    documents = {
        1: "the quick brown fox jumps",
        2: "quick brown dog",
        3: "the fox is quick and brown",
        4: "quick brown fox",
        5: "brown quick brown",
        6: "quick fox brown",
        7: "a a a a",
    }

    engine = PhraseSearch(documents)

    tests = [
        ("quick brown", [1, 2, 4, 5]),
        ("brown fox", [1, 4]),
        ("quick fox", [6]),
        ("the quick", [1]),
        ("brown", [1, 2, 3, 4, 5, 6]),
        ("quick brown fox", [1, 4]),
        ("fox jumps", [1]),
        ("dog", [2]),
        ("not present", []),
        # Words exist in the document, but are not adjacent
        ("quick fox", [6]),
        # Repeated words
        ("a a", [7]),
        ("a a a", [7]),
        ("a a a a", [7]),
        ("a a a a a", []),
        # Phrase longer than documents
        ("the quick brown fox jumps again", []),
        # Empty phrase
        ("", []),
    ]

    for i, (phrase, expected) in enumerate(tests, 1):
        actual = engine.search(phrase)

        assert actual == expected, (
            f"Test {i} failed:\n"
            f"phrase = {phrase!r}\n"
            f"returned {actual}\n"
            f"expected {expected}"
        )

    print("All tests passed!")


if __name__ == "__main__":
    run_tests()
