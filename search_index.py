from dataclasses import dataclass
from pathlib import Path
from typing import Iterator
import unicodedata
import pytest


@dataclass(frozen=True)
class LineMatch:
    line_number: int
    byte_offset: int | None = None


def tokenize(text: str) -> list[str]:
    """Return normalized tokens according to the contract."""
    tokens = []
    current = []
    for ch in text:
        category = unicodedata.category(ch)
        if category[0] in {"L", "N", "M"}:
            current.append(ch)
        else:
            if current:
                current = "".join(current)
                current = unicodedata.normalize("NFC", current)
                current = current.casefold()
                current = unicodedata.normalize("NFC", current)
                tokens.append(current)
                current = []
    if current:
        current = "".join(current)
        current = unicodedata.normalize("NFC", current)
        current = current.casefold()
        current = unicodedata.normalize("NFC", current)
        tokens.append(current)
    return tokens


def search_word(
    file_path: str | Path,
    query: str,
) -> Iterator[LineMatch]:
    """Search the source file without a persistent index."""
    if len(query.strip()) <= 0:
        raise ValueError()
    query = query.strip()
    if not query:
        raise ValueError("query should be one token")
    if len(tokenize(query)) != 1:
        raise ValueError("query should just have one token")
    offset = 1
    needle = tokenize(query)[0]
    with open(file_path, "r", encoding="utf8") as f:
        for line in f:
            hay = tokenize(line)
            if needle in hay:
                yield LineMatch(line_number=offset)
            offset += 1


def contains_needle(haystack: list[str], needle: list[str]):
    n = len(needle)
    for i in range(len(haystack) - n + 1):
        if haystack[i : i + n] == needle:
            return True
    return False


def search_phrase(
    file_path: str | Path,
    query: str,
) -> Iterator[LineMatch]:
    """Search for consecutive tokens within individual lines."""
    if len(query.strip()) <= 0:
        raise ValueError()
    query = query.strip()
    if not query:
        raise ValueError("query should be atleast one token")
    needle = tokenize(query)
    if len(needle) < 1:
        raise ValueError("query should have atleast one token")
    offset = 1
    with open(file_path, "r", encoding="utf8") as f:
        for line in f:
            hay = tokenize(line)
            if contains_needle(hay, needle):
                yield LineMatch(line_number=offset)
            offset += 1


def file_exists(directory: str | Path, filename: str) -> bool:
    path = Path(directory) / filename
    return path.is_file()


class SearchIndex:
    def __init__(self, index_dir: str | Path) -> None:
        """Open an existing index or prepare an unbuilt index."""
        self._index_dir = index_dir
        self._index = None
        if file_exists(index_dir, "index"):
            self._index = open(Path(index_dir) / "index", "rw", encoding="utf8")

    def build(self, file_path: str | Path) -> None:
        """Create or replace a persistent snapshot of the source file."""
        with open(file_path, "r", encoding="utf8") as f:
            for line in f:
                tokens = tokenize(line)

    def search_word(self, query: str) -> Iterator[LineMatch]:
        """Search the latest completed snapshot."""
        raise NotImplementedError

    def search_phrase(self, query: str) -> Iterator[LineMatch]:
        """Search the latest completed snapshot."""
        raise NotImplementedError

    def refresh(self) -> None:
        """Make the current contents of the recorded source searchable."""
        raise NotImplementedError

    def close(self) -> None:
        """Release resources. Calling close repeatedly should be safe."""
        raise NotImplementedError


@pytest.fixture
def indexed_sample(tmp_path):
    source = tmp_path / "sentences.txt"
    source.write_bytes(
        (
            "Hello, world! Hello world.\r\n"  # 1
            "quick brown fox\n"  # 2
            "QUICK blue fox\n"  # 3
            "\n"  # 4
            "Straße café cafe\u0301\n"  # 5
            "red red red blue\n"  # 6
            "boundary alpha\n"  # 7
            "beta boundary\n"  # 8
            "cat concatenate cat_2\n"  # 9
            "last line"  # 10: no final newline
        ).encode("utf-8")
    )

    index = SearchIndex(tmp_path / "index")
    try:
        index.build(source)
        yield index
    finally:
        index.close()


def result_lines(results):
    # Check that the API returns an iterator, not a list.
    assert iter(results) is results

    matches = list(results)
    assert all(isinstance(match, LineMatch) for match in matches)

    numbers = [match.line_number for match in matches]
    assert numbers == sorted(set(numbers)), (
        "Results must be ordered and must not repeat a line"
    )
    return numbers


@pytest.mark.parametrize(
    "query, expected",
    [
        ("hello", [1]),
        ("HELLO!", [1]),
        ("quick", [2, 3]),
        ("strasse", [5]),
        ("CAFÉ", [5]),
        ("cafe\u0301", [5]),
        ("red", [6]),
        ("cat", [9]),
        ("concatenate", [9]),
        ("2", [9]),
        ("last", [10]),
        ("missing", []),
    ],
)
def test_index_word_search(indexed_sample, query, expected):
    assert result_lines(indexed_sample.search_word(query)) == expected


@pytest.mark.parametrize(
    "query, expected",
    [
        ("hello world", [1]),
        ("HELLO---WORLD", [1]),
        ("world hello", [1]),
        ("quick brown fox", [2]),
        ("quick blue fox", [3]),
        ("quick fox", []),  # Tokens must be adjacent.
        ("brown quick", []),  # Order matters.
        ("café café", [5]),
        ("red red", [6]),  # Return line 6 only once.
        ("red red red", [6]),
        ("red red red red", []),  # Cannot reuse a token position.
        ("red blue", [6]),
        ("alpha beta", []),  # Cannot cross line boundaries.
        ("cat 2", [9]),
        ("last line", [10]),
        ("quick", [2, 3]),  # One-token phrases are valid.
        ("missing phrase", []),
    ],
)
def test_index_phrase_search(indexed_sample, query, expected):
    assert result_lines(indexed_sample.search_phrase(query)) == expected


@pytest.mark.parametrize("query", ["", "   ", "!!!", "two words", "don't"])
def test_index_invalid_word_query(indexed_sample, query):
    with pytest.raises(ValueError):
        list(indexed_sample.search_word(query))


@pytest.mark.parametrize("query", ["", "   ", "!!!🐈"])
def test_index_invalid_phrase_query(indexed_sample, query):
    with pytest.raises(ValueError):
        list(indexed_sample.search_phrase(query))


def test_index_persists_without_source(tmp_path):
    source = tmp_path / "source.txt"
    source.write_bytes(b"alpha beta\nbeta gamma\n")
    index_dir = tmp_path / "index"

    index = SearchIndex(index_dir)
    try:
        index.build(source)
    finally:
        index.close()

    # Queries must use persistent index data.
    source.unlink()

    reopened = SearchIndex(index_dir)
    try:
        assert result_lines(reopened.search_word("beta")) == [1, 2]
        assert result_lines(reopened.search_phrase("alpha beta")) == [1]
    finally:
        reopened.close()


def test_append_is_invisible_until_refresh(tmp_path):
    source = tmp_path / "source.txt"
    source.write_bytes(b"alpha")  # Deliberately no final newline.

    index = SearchIndex(tmp_path / "index")
    try:
        index.build(source)

        with source.open("ab") as handle:
            handle.write(b" beta\nalpha beta\n")

        # The previous snapshot still has only "alpha".
        assert result_lines(index.search_word("alpha")) == [1]
        assert result_lines(index.search_word("beta")) == []
        assert result_lines(index.search_phrase("alpha beta")) == []

        index.refresh()

        assert result_lines(index.search_word("beta")) == [1, 2]
        assert result_lines(index.search_phrase("alpha beta")) == [1, 2]

        # Refreshing again must not duplicate stored results.
        index.refresh()
        assert result_lines(index.search_word("alpha")) == [1, 2]
    finally:
        index.close()


@pytest.mark.parametrize("change", ["edit", "truncate", "replace"])
def test_refresh_removes_stale_data(tmp_path, change):
    source = tmp_path / "source.txt"
    source.write_bytes(b"old token\nkeep token\n")

    index = SearchIndex(tmp_path / "index")
    try:
        index.build(source)

        if change == "edit":
            # Same length as the original file.
            source.write_bytes(b"new token\nkeep token\n")
        elif change == "truncate":
            source.write_bytes(b"")
        else:
            replacement = tmp_path / "replacement.txt"
            replacement.write_bytes(b"new token\n")
            replacement.replace(source)

        assert result_lines(index.search_word("old")) == [1]

        index.refresh()

        assert result_lines(index.search_word("old")) == []
        expected = [] if change == "truncate" else [1]
        assert result_lines(index.search_phrase("new token")) == expected
        expected_keep = [2] if change == "edit" else []
        assert result_lines(index.search_word("keep")) == expected_keep
    finally:
        index.close()


def test_refresh_after_reopening(tmp_path):
    source = tmp_path / "source.txt"
    source.write_bytes(b"before\n")
    index_dir = tmp_path / "index"

    index = SearchIndex(index_dir)
    try:
        index.build(source)
    finally:
        index.close()

    source.write_bytes(b"after\n")

    reopened = SearchIndex(index_dir)
    try:
        assert result_lines(reopened.search_word("before")) == [1]
        assert result_lines(reopened.search_word("after")) == []

        # The source path must have been saved persistently.
        reopened.refresh()

        assert result_lines(reopened.search_word("before")) == []
        assert result_lines(reopened.search_word("after")) == [1]
    finally:
        reopened.close()


def test_build_replaces_previous_index(tmp_path):
    first = tmp_path / "first.txt"
    second = tmp_path / "second.txt"
    first.write_bytes(b"old token\n")
    second.write_bytes(b"new token\n")

    index = SearchIndex(tmp_path / "index")
    try:
        index.build(first)
        index.build(second)

        assert result_lines(index.search_word("old")) == []
        assert result_lines(index.search_word("new")) == [1]

        # Refresh must now follow the second source.
        second.write_bytes(b"latest token\n")
        index.refresh()

        assert result_lines(index.search_word("new")) == []
        assert result_lines(index.search_word("latest")) == [1]
    finally:
        index.close()


@pytest.mark.parametrize("raw", [b"", b"\n\n"])
def test_empty_or_blank_file(tmp_path, raw):
    source = tmp_path / "source.txt"
    source.write_bytes(raw)

    index = SearchIndex(tmp_path / "index")
    try:
        index.build(source)
        assert result_lines(index.search_word("anything")) == []
        assert result_lines(index.search_phrase("any phrase")) == []
    finally:
        index.close()


def test_optional_byte_offsets(tmp_path):
    source = tmp_path / "source.txt"
    first_line = "café\r\n".encode("utf-8")
    source.write_bytes(first_line + b"target\n")

    index = SearchIndex(tmp_path / "index")
    try:
        index.build(source)
        matches = list(index.search_word("target"))

        assert len(matches) == 1
        assert matches[0].line_number == 2
        assert matches[0].byte_offset in (None, len(first_line))
    finally:
        index.close()


def test_close_twice(tmp_path):
    source = tmp_path / "source.txt"
    source.write_bytes(b"hello\n")

    index = SearchIndex(tmp_path / "index")
    index.build(source)
    index.close()
    index.close()


@pytest.fixture
def streaming_source(tmp_path):
    source = tmp_path / "streaming.txt"
    source.write_bytes(
        (
            "Hello, world! Hello world.\r\n"  # 1
            "\n"  # 2
            "QUICK brown fox\n"  # 3
            "Straße café cafe\u0301\n"  # 4
            "red red red blue\n"  # 5
            "boundary alpha\n"  # 6
            "beta boundary\n"  # 7
            "cat concatenate cat_2\n"  # 8
            "last line"  # 9: no final newline
        ).encode("utf-8")
    )
    return source


def streaming_line_numbers(results):
    assert iter(results) is results, "Return an iterator"
    matches = list(results)
    assert all(isinstance(match, LineMatch) for match in matches)
    return [match.line_number for match in matches]


@pytest.mark.parametrize(
    "text, expected",
    [
        ("hello", ["hello"]),
        ("Hello, WORLD!", ["hello", "world"]),
        ("Don't stop", ["don", "t", "stop"]),
        ("state-of-the-art", ["state", "of", "the", "art"]),
        ("Straße", ["strasse"]),
        ("cafe\u0301", ["café"]),
        ("cat_2🐈dog", ["cat", "2", "dog"]),
        ("中文 １２３", ["中文", "１２３"]),
        ("!!!", []),
        ("", []),
    ],
)
def test_tokenize_standalone(text, expected):
    assert tokenize(text) == expected


@pytest.mark.parametrize(
    "query, expected",
    [
        ("hello", [1]),
        ("HELLO!", [1]),
        ("quick", [3]),
        ("strasse", [4]),
        ("CAFÉ", [4]),
        ("red", [5]),  # Return the line only once.
        ("boundary", [6, 7]),
        ("cat", [8]),
        ("concatenate", [8]),
        ("2", [8]),
        ("last", [9]),
        ("missing", []),
    ],
)
def test_streaming_word(streaming_source, query, expected):
    results = search_word(streaming_source, query)
    assert streaming_line_numbers(results) == expected


@pytest.mark.parametrize(
    "query, expected",
    [
        ("hello world", [1]),
        ("HELLO---WORLD", [1]),
        ("world hello", [1]),
        ("quick brown fox", [3]),
        ("quick fox", []),
        ("brown quick", []),
        ("café café", [4]),
        ("red red", [5]),
        ("red red red", [5]),
        ("red red red red", []),
        ("red blue", [5]),
        ("alpha beta", []),  # Cannot cross lines.
        ("cat 2", [8]),
        ("last line", [9]),
        ("boundary", [6, 7]),  # One-token phrase.
    ],
)
def test_streaming_phrase(streaming_source, query, expected):
    results = search_phrase(streaming_source, query)
    assert streaming_line_numbers(results) == expected


@pytest.mark.parametrize("query", ["", "   ", "!!!", "two words", "don't"])
def test_streaming_invalid_word(streaming_source, query):
    with pytest.raises(ValueError):
        list(search_word(streaming_source, query))


@pytest.mark.parametrize("query", ["", "   ", "!!!🐈"])
def test_streaming_invalid_phrase(streaming_source, query):
    with pytest.raises(ValueError):
        list(search_phrase(streaming_source, query))


@pytest.mark.parametrize("search", [search_word, search_phrase])
@pytest.mark.parametrize(
    "raw, expected",
    [
        (b"", []),
        (b"\n\n", []),
        (b"target", [1]),
        (b"target\n", [1]),
        (b"\r\n\ntarget\r\n", [3]),
    ],
)
def test_streaming_line_boundaries(tmp_path, search, raw, expected):
    source = tmp_path / "boundaries.txt"
    source.write_bytes(raw)

    assert streaming_line_numbers(search(source, "target")) == expected


@pytest.mark.parametrize("search", [search_word, search_phrase])
def test_streaming_optional_offsets(tmp_path, search):
    source = tmp_path / "offsets.txt"
    first_line = "café\r\n".encode("utf-8")
    source.write_bytes(first_line + b"target\n")

    matches = list(search(source, "target"))

    assert len(matches) == 1
    assert matches[0].line_number == 2
    assert matches[0].byte_offset in (None, len(first_line))
