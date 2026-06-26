import pytest

from fizzbuzz import fizzbuzz


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
