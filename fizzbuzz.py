from collections.abc import Iterator, Sequence


DEFAULT_MAPPINGS: Sequence[tuple[int, str]] = ((3, "Fizz"), (5, "Buzz"))


def word_stream(multiple: int, word: str, n: int) -> Iterator[str]:
    """Yield ``word`` when the current index is divisible by ``multiple``.

    Indices are 1-based so that they line up with the FizzBuzz sequence.
    """
    for i in range(1, n + 1):
        yield word if i % multiple == 0 else ""


def add_streams(*streams: Iterator[str]) -> Iterator[str]:
    """Combine several string streams element-wise by concatenation."""
    for items in zip(*streams):
        yield "".join(items)


def fizzbuzz_stream(
    n: int,
    mappings: Sequence[tuple[int, str]],
) -> Iterator[str]:
    """Yield the FizzBuzz-like sequence for the given mappings.

    For each number from 1 to ``n``, the matching words are concatenated in
    mapping-list order. If no mapping matches, the number itself is yielded.
    """
    if not mappings:
        for i in range(1, n + 1):
            yield str(i)
        return

    streams = [word_stream(multiple, word, n) for multiple, word in mappings]
    for i, joined in enumerate(add_streams(*streams), start=1):
        yield joined or str(i)


def fizzbuzz(
    n: int = 100,
    mappings: Sequence[tuple[int, str]] | None = None,
) -> None:
    """Print the FizzBuzz sequence from 1 to ``n``.

    ``mappings`` is a sequence of ``(multiple, word)`` pairs. They are applied
    in order; matching words are concatenated. The default mappings produce the
    classic FizzBuzz output.
    """
    if mappings is None:
        mappings = DEFAULT_MAPPINGS

    for multiple, _word in mappings:
        if multiple == 0:
            raise ValueError("mapping multiples must be non-zero")

    for value in fizzbuzz_stream(n, mappings):
        print(value)


if __name__ == "__main__":
    fizzbuzz()
