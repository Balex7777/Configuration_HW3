import argparse
import re
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap


def parse_yaml_file_with_comments(file_path):
    """Считывает YAML файл с сохранением комментариев."""
    yaml = YAML()
    yaml.preserve_quotes = True
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return yaml.load(file)
    except FileNotFoundError:
        raise ValueError(f"Файл {file_path} не найден.")
    except Exception as e:
        raise ValueError(f"Ошибка парсинга YAML: {e}")


def validate_name(name):
    """Проверяет, что имя соответствует правилам."""
    if not re.fullmatch(r"[A-Z]+", name):
        raise ValueError(f"Недопустимое имя: {name}")
    return name


def format_value(value, indent=4):
    """Форматирует значения в синтаксисе учебного языка."""
    if isinstance(value, str):
        return f"q({value})"
    elif isinstance(value, (int, float)):
        return str(value)
    elif isinstance(value, list):
        formatted_items = ", ".join(format_value(item) for item in value)
        return f"{{ {formatted_items} }}"
    elif isinstance(value, dict):
        return format_nested_dict(value, indent=indent)
    else:
        raise ValueError(f"Неподдерживаемый тип значения: {type(value)}")


def format_nested_dict(data, indent=4):
    """Форматирует вложенные словари в синтаксисе учебного языка."""
    lines = []
    nested_indent = " " * indent
    for key, value in data.items():
        validate_name(key)
        formatted_value = format_value(value, indent=indent + 4)
        lines.append(f"{nested_indent}{key} = {formatted_value};")
    return f"{{\n{chr(10).join(lines)}\n{' ' * (indent - 4)}}}"


def extract_comments(node, key):
    """Извлекает комментарий для заданного ключа."""
    if hasattr(node, "ca") and node.ca.items.get(key):
        comment = node.ca.items[key][2]  # Взять комментарий после ключа
        if comment:
            return comment.value.strip()
    return None


def convert_to_custom_language(data, indent=4):
    """Преобразует YAML данные в учебный конфигурационный язык."""
    if not isinstance(data, CommentedMap):
        raise ValueError("Топ-уровень YAML должен быть объектом (dict).")

    lines = []
    for key, value in data.items():
        validate_name(key)
        comment = extract_comments(data, key)
        if comment:
            lines.append(f":: {comment}")  # Добавляем комментарий
        formatted_value = format_value(value, indent=indent + 4)
        lines.append(f"{key} = {formatted_value};\n")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Преобразование YAML в учебный конфигурационный язык с сохранением комментариев.")
    parser.add_argument("input", help="Путь к входному YAML файлу.")
    parser.add_argument("-o", "--output", required=True, help="Путь к выходному файлу.")
    args = parser.parse_args()

    try:
        yaml_data = parse_yaml_file_with_comments(args.input)
        output_data = convert_to_custom_language(yaml_data)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output_data)
        print(f"Конфигурация успешно записана в {args.output}")
    except ValueError as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
