import unicodedata
from collections import defaultdict


def tokenize(text: str):

    tokens = []
    current = []
    for ch in text:
        if unicodedata.category(ch) in {"L", "N", "M"}:
            current.append(ch)
        else:
            if current:
                current = "".join(current)
                current = unicodedata.normalize("NFC", current)
                current = current.casefold()
                current = unicodedata.normalize("NFC", current)
                tokens.append(current)
                current = []


class PhraseSearch:
    def __init__(self, documents: dict[int, str]) -> None:
        self.index: dict[str, dict[int, list[int]]] = defaultdict(
            lambda: defaultdict(list)
        )
        for doc_id, text in documents.items():
            for pos, word in enumerate(text.split()):
                self.index[word][doc_id].append(pos)

    def search(self, phrase: str) -> list[int]:
        words = phrase.split()
        if not words:
            return []

        for word in words:
            if word not in self.index:
                return []

        # documents containing the first word
        candidate_docs = set(self.index[words[0]].keys())

        for word in words[1:]:
            candidate_docs &= self.index[word].keys()
            if not candidate_docs:
                return []

        result = []

        for doc_id in candidate_docs:
            first_positions = self.index[words[0]][doc_id]
            later_positions = [set(self.index[word][doc_id]) for word in words[1:]]

            for start in first_positions:
                matched = True
                for offset, positions in enumerate(later_positions, 1):
                    if start + offset not in positions:
                        matched = False
                        break
                if matched:
                    result.append(doc_id)
                    break
        return sorted(result)
