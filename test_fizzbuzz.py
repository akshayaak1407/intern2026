import pytest

from fizzbuzz import (
    DEFAULT_MAPPINGS,
    add_streams,
    fizzbuzz,
    fizzbuzz_stream,
    word_stream,
)


@pytest.fixture
def fizzbuzz_func():
    return fizzbuzz


@pytest.mark.parametrize(
    "n,expected",
    [
        (1, "1\n"),
        (3, "1\n2\nFizz\n"),
        (5, "1\n2\nFizz\n4\nBuzz\n"),
        (
            15,
            "1\n2\nFizz\n4\nBuzz\nFizz\n7\n8\nFizz\nBuzz\n11\nFizz\n13\n14\nFizzBuzz\n",
        ),
    ],
    ids=[
        "prints_number_for_non_divisible_value",
        "prints_fizz_for_multiple_of_three",
        "prints_buzz_for_multiple_of_five",
        "prints_fizzbuzz_for_multiple_of_three_and_five",
    ],
)
def test_fizzbuzz_outputs_expected_sequence(fizzbuzz_func, capfd, n, expected):
    fizzbuzz_func(n)
    captured = capfd.readouterr()
    assert captured.out == expected


def test_word_stream_yields_word_or_empty_string():
    assert list(word_stream(3, "Fizz", 6)) == ["", "", "Fizz", "", "", "Fizz"]


def test_add_streams_concatenates_element_wise():
    assert list(
        add_streams(
            word_stream(2, "A", 4),
            word_stream(2, "B", 4),
        )
    ) == ["", "AB", "", "AB"]


def test_fizzbuzz_stream_uses_default_mappings():
    assert list(fizzbuzz_stream(5, DEFAULT_MAPPINGS)) == [
        "1",
        "2",
        "Fizz",
        "4",
        "Buzz",
    ]


def test_fizzbuzz_stream_order_sensitive():
    forwards = list(fizzbuzz_stream(14, [(2, "Boom"), (7, "Baz")]))
    reverse = list(fizzbuzz_stream(14, [(7, "Baz"), (2, "Boom")]))

    assert forwards[-1] == "BoomBaz"
    assert reverse[-1] == "BazBoom"
    assert forwards[:-1] == reverse[:-1]


def test_fizzbuzz_stream_empty_mappings_yields_numbers():
    assert list(fizzbuzz_stream(5, [])) == ["1", "2", "3", "4", "5"]


@pytest.mark.parametrize(
    "mappings,n,expected",
    [
        (
            [(2, "Boom"), (7, "Baz")],
            14,
            "1\nBoom\n3\nBoom\n5\nBoom\nBaz\nBoom\n9\nBoom\n11\nBoom\n13\nBoomBaz\n",
        ),
        (
            [(7, "Baz"), (2, "Boom")],
            14,
            "1\nBoom\n3\nBoom\n5\nBoom\nBaz\nBoom\n9\nBoom\n11\nBoom\n13\nBazBoom\n",
        ),
        (
            [(2, "A"), (4, "B"), (5, "C")],
            20,
            "1\nA\n3\nAB\nC\nA\n7\nAB\n9\nAC\n11\nAB\n13\nA\nC\nAB\n17\nA\n19\nABC\n",
        ),
    ],
    ids=[
        "custom_two_mappings_in_order",
        "custom_two_mappings_reversed",
        "three_mappings_concatenate_in_order",
    ],
)
def test_fizzbuzz_custom_mappings(fizzbuzz_func, capfd, mappings, n, expected):
    fizzbuzz_func(n, mappings)
    captured = capfd.readouterr()
    assert captured.out == expected


def test_fizzbuzz_empty_mappings_prints_numbers(fizzbuzz_func, capfd):
    fizzbuzz_func(5, [])
    captured = capfd.readouterr()
    assert captured.out == "1\n2\n3\n4\n5\n"


def test_fizzbuzz_rejects_zero_multiple(fizzbuzz_func):
    with pytest.raises(ValueError):
        fizzbuzz_func(10, [(0, "Zero")])
