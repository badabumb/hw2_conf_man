import argparse
from parser import remove_comments, parse_dict, parse_constants
from evaluator import evaluate_postfix
import json
import sys

def to_json(data):
    """
    Преобразует данные в JSON.
    """
    return json.dumps(data, indent=4)

if __name__ == "__main__":
    # Аргументы командной строки
    parser = argparse.ArgumentParser(description="CLI для трансляции конфигураций в JSON")
    parser.add_argument("--input", required=True, help="Путь к входному файлу")
    args = parser.parse_args()

    try:
        # Шаг 1. Чтение файла
        with open(args.input, 'r') as f:
            raw_text = f.read()

        # Шаг 2. Убираем комментарии
        cleaned_text = remove_comments(raw_text)

        # Шаг 3. Парсим константы
        constants, remaining_text = parse_constants(cleaned_text)

        # Шаг 4. Парсим словари
        parsed_data = parse_dict(remaining_text, constants)

        # Шаг 5. Вывод JSON
        json_output = to_json(parsed_data)
        print(json_output)

    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)