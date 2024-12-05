import pytest
from unittest.mock import patch, mock_open
from io import StringIO
from main import (
    parse_yaml_file_with_comments,
    validate_name,
    evaluate_constants,
    convert_to_custom_language
)


# Тест для функции parse_yaml_file_with_comments
@patch("builtins.open", new_callable=mock_open, read_data="key: value\n")
def test_parse_yaml_file_with_comments(mock_file):
    comment, data = parse_yaml_file_with_comments("mock.yml")
    assert comment is None
    assert data["key"] == "value"
    mock_file.assert_called_once_with("mock.yml", "r", encoding="utf-8")

# Тест для функции validate_name
def test_validate_name_valid():
    assert validate_name("VALIDNAME") == "VALIDNAME"


def test_validate_name_invalid():
    with pytest.raises(ValueError, match="Недопустимое имя: InvalidName"):
        validate_name("InvalidName")


# Тест для функции evaluate_constants
def test_evaluate_constants_valid():
    context = {"x": 10}
    result = evaluate_constants("|x + 2|", context)
    assert result == 12


def test_evaluate_constants_invalid():
    with pytest.raises(ValueError):
        evaluate_constants("|x + 2|")  # x не определен в контексте


