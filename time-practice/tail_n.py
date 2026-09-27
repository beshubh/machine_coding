from pathlib import Path
import tempfile


def tail(path: Path, n: int) -> list[str]:
    """
    Return the last n lines from the file, in original order.

    Returned strings must not contain trailing newline characters.

    The file may be too large to fit in memory.
    """
    if n <= 0:
        return []
    block_size = 8192
    chunks = []
    with open(path, "rb") as f:
        f.seek(0, 2)  # seek to end
        pos = f.tell()
        newlines = 0
        while pos > 0 and newlines <= n:
            read_size = min(block_size, pos)
            pos -= read_size
            f.seek(pos)
            chunk = f.read(read_size)
            chunks.append(chunk)
            newlines += chunk.count(b"\n")

        data = b"".join(reversed(chunks))
        lines = data.splitlines()
        return [line.decode("utf-8") for line in lines[-n:]]


def run_tests():
    def make_file(contents: str) -> Path:
        f = tempfile.NamedTemporaryFile(
            mode="w",
            delete=False,
            encoding="utf-8",
        )
        f.write(contents)
        f.close()
        return Path(f.name)

    # Basic
    path = make_file("line1\nline2\nline3\nline4\nline5\n")

    assert tail(path, 2) == [
        "line4",
        "line5",
    ]

    assert tail(path, 5) == [
        "line1",
        "line2",
        "line3",
        "line4",
        "line5",
    ]

    # Asking for more lines than exist
    assert tail(path, 100) == [
        "line1",
        "line2",
        "line3",
        "line4",
        "line5",
    ]

    # n = 0
    assert tail(path, 0) == []

    # Single line
    path = make_file("hello")
    assert tail(path, 1) == ["hello"]

    # Single line with newline
    path = make_file("hello\n")
    assert tail(path, 1) == ["hello"]

    # No trailing newline
    path = make_file("a\nb\nc")

    assert tail(path, 2) == [
        "b",
        "c",
    ]

    # Empty file
    path = make_file("")
    assert tail(path, 10) == []

    # Blank lines are real lines
    path = make_file("a\n\nb\n\nc\n")

    assert tail(path, 4) == [
        "",
        "b",
        "",
        "c",
    ]

    # File consisting only of blank lines
    path = make_file("\n\n\n")

    assert tail(path, 2) == [
        "",
        "",
    ]

    # Long lines
    long_line = "x" * 100_000

    path = make_file(f"first\n{long_line}\nlast\n")

    assert tail(path, 2) == [
        long_line,
        "last",
    ]

    # Unicode
    path = make_file("hello\nनमस्ते\nこんにちは\n🙂🙂🙂\n")

    assert tail(path, 3) == [
        "नमस्ते",
        "こんにちは",
        "🙂🙂🙂",
    ]

    # Many lines
    contents = "".join(f"line-{i}\n" for i in range(10_000))

    path = make_file(contents)

    assert tail(path, 3) == [
        "line-9997",
        "line-9998",
        "line-9999",
    ]

    print("All tests passed!")


if __name__ == "__main__":
    run_tests()
