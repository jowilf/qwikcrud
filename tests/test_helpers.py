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


@pytest.mark.parametrize(
    "markdown_text, expected_result",
    [
        (
            """
        Here is a JSON object:

        ```json
        {"key":"value","number":42,"comment":"JSON within a code block"}
        ```
        End of JSON.
        """,
            '{"key":"value","number":42,"comment":"JSON within a code block"}',
        ),
        (
            '{"key":"value","number":42,"comment":"Entire text considered as JSON"}',
            '{"key":"value","number":42,"comment":"Entire text considered as JSON"}',
        ),
    ],
)
def test_extract_json_from_markdown(markdown_text, expected_result):
    parse_result = h.extract_json_from_markdown(markdown_text)
    assert parse_result.strip() == expected_result.strip()
