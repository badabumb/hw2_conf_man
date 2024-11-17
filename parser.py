import re


def remove_comments(text):
    """
    Убирает однострочные и многострочные комментарии из текста.
    """
    # Убираем однострочные комментарии
    text = re.sub(r'C .*', '', text)
    # Убираем многострочные комментарии
    text = re.sub(r'\(\*.*?\*\)', '', text, flags=re.DOTALL)
    return text.strip()


def parse_constants(text):
    """
    Находит константы вида `def имя = значение` и возвращает словарь констант.
    """
    constants = {}
    remaining_lines = []

    for line in text.splitlines():
        line = line.strip()
        if line.startswith("def "):
            # Парсим константу
            match = re.match(r"def\s+([_a-z]+)\s*=\s*(\d+)", line)
            if not match:
                raise ValueError(f"Неверный формат константы: {line}")
            name, value = match.groups()
            constants[name] = int(value)
        else:
            remaining_lines.append(line)

    return constants, "\n".join(remaining_lines)


def parse_dict(text, constants):
    """
    Парсит словарь формата {key = value, ...}, поддерживает вложенность.
    """
    if not text.startswith('{') or not text.endswith('}'):
        raise ValueError("Неверный формат словаря: должен начинаться с '{' и заканчиваться '}'")

    text = text[1:-1].strip()  # Убираем внешние фигурные скобки
    result = {}
    buffer = ""  # Буфер для накопления элементов

    depth = 0  # Уровень вложенности
    for char in text:
        if char == ',' and depth == 0:  # Разделитель верхнего уровня
            if buffer.strip():  # Игнорируем пустые строки
                key, value = parse_key_value(buffer.strip(), constants)
                result[key] = value
                buffer = ""  # Сбрасываем буфер
        else:
            buffer += char
            if char == '{':
                depth += 1
            elif char == '}':
                depth -= 1

    # Добавляем последний элемент
    if buffer.strip():
        key, value = parse_key_value(buffer.strip(), constants)
        result[key] = value

    return result


def parse_key_value(item, constants):
    """
    Парсит строку `key = value` и возвращает ключ и значение.
    """
    key_value = item.split('=', 1)
    if len(key_value) != 2:
        raise ValueError(f"Неверный формат элемента: {item}")

    key = key_value[0].strip()
    value = key_value[1].strip()

    # Преобразуем значение
    if value.isdigit():
        value = int(value)
    elif value in constants:
        value = constants[value]
    elif value.startswith('{') and value.endswith('}'):
        value = parse_dict(value, constants)
    else:
        value = value.strip('"')  # Считаем строкой

    return key, value