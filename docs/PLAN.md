# Refactor Plan: Ordered, Mapping-Driven FizzBuzz with Generator Streams

## 1. Goal

Replace the hard-coded `3 → Fizz`, `5 → Buzz` logic with a generic, order-preserving design.
The user supplies any number of `(multiple, word)` pairs; for each integer the program concatenates the matching words in the order the mappings were provided.

The core mechanism will be **adding streams** via Python generators: one stream per mapping, each stream emitting either its word or `""` for every number, then combining them element-wise with `"".join`.

## 2. Proposed API

- `fizzbuzz(n: int = 100, mappings: Sequence[tuple[int, str]] | None = None) -> None`
  - If `mappings` is `None`, defaults to `[(3, "Fizz"), (5, "Buzz")]` so existing behavior stays intact.
  - Prints one value per line.
- Add small generator helpers (all typed, all lazy):
  - `word_stream(multiple, word, n)` → yields `word` when the current index is divisible, else `""`.
  - `add_streams(*streams)` → yields `"".join(items)` for each position (the “stream addition”).
  - `fizzbuzz_stream(n, mappings)` → yields the final value for each number (joined words, or the number itself if joined words are empty).

## 3. Stream Design

For mappings `[(2, "Boom"), (7, "Baz")]` and `n = 14`:

```text
index:        1   2      3   ... 14
stream 2:     ""  "Boom" ""  ... "Boom"
stream 7:     ""  ""     ""  ... "Baz"
added:        ""  "Boom" ""  ... "BoomBaz"
final:        "1" "Boom" "3" ... "BoomBaz"
```

Because streams are produced in mapping-list order and are zipped in that order, the concatenation naturally preserves insertion order:

- `[(2, "Boom"), (7, "Baz")]` → `14` → `BoomBaz`
- `[(7, "Baz"), (2, "Boom")]` → `14` → `BazBoom`

## 4. File-by-File Changes

### `fizzbuzz.py`

1. Define a default constant:
   ```python
   DEFAULT_MAPPINGS: Sequence[tuple[int, str]] = ((3, "Fizz"), (5, "Buzz"))
   ```
2. Add helper generators:
   - `word_stream(multiple: int, word: str, n: int) -> Iterator[str]`
   - `add_streams(*streams: Iterator[str]) -> Iterator[str]`
3. Add `fizzbuzz_stream(n: int, mappings: Sequence[tuple[int, str]]) -> Iterator[str]`:
   - Build one `word_stream` per mapping.
   - Feed them through `add_streams`.
   - If the concatenated result is empty, emit `str(i)`, otherwise emit the concatenated result.
4. Rewrite `fizzbuzz(...)` to:
   - Validate that every multiple is non-zero (raise `ValueError` for zero).
   - Loop over `fizzbuzz_stream(n, mappings)` and print each yielded item.
5. Keep `if __name__ == "__main__":` calling `fizzbuzz()` so the module still runs standalone.

### `test_fizzbuzz.py`

1. Keep the existing default-output tests; they should still pass because the default mappings preserve the classic order (`Fizz` before `Buzz`).
2. Add new parametrized tests:
   - Custom two-mapping order test: `[(2, "Boom"), (7, "Baz")]` for `n=14`, expect `...BoomBaz`.
   - Reverse-order test: `[(7, "Baz"), (2, "Boom")]` for `n=14`, expect `...BazBoom`.
   - More than two mappings, e.g. `[(2, "Boom"), (7, "Baz"), (9, "Bam")]` for a suitable `n`.
   - Empty mappings → just numbers.
   - `ValueError` on a mapping with multiple `0`.
3. Add at least one direct stream test to verify the “addition of streams” mechanics independently (inputs/outputs not relying on `capfd`).

### `main.py`

- Leave untouched for this refactor; it is not part of the current FizzBuzz module. If desired later, it can call `fizzbuzz(...)` with custom mappings.

## 5. Behavior / Edge Cases to Cover

- **No mappings:** outputs the plain number sequence.
- **No match for a number:** outputs the number.
- **Multiple matches:** concatenates words in mapping-list order.
- **Zero multiple:** raises `ValueError` immediately.
- **Default call:** identical to original FizzBuzz output.
- **Order sensitivity:** tested explicitly.

## 6. Implementation Order

1. Add generator helpers and refactored `fizzbuzz` function to `fizzbuzz.py`.
2. Run existing tests to confirm default behavior is unchanged.
3. Add new tests for custom mappings, order preservation, error handling, and empty mappings.
4. Run full test suite.
5. (Optional) Update `README.md` with the new API usage examples.

## 7. Validation

Run the test suite:

```bash
uv run pytest
```

Expected result: all tests pass, including the original default-output cases plus the new ordered-mapping cases.
