import pytest

from qwikcrud import helpers as h


@pytest.mark.parametrize(
    "input_str, expected_output",
    [
        ("camelCaseString", "camel_case_string"),
        ("AnotherExample", "another_example"),
        ("Single", "single"),
        ("mixedCase123", "mixed_case123"),
    ],
)
def test_snake_case(input_str, expected_output) -> None:
    assert h.snake_case(input_str) == expected_output
