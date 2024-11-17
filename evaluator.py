def evaluate_postfix(tokens, constants):
    """
    Вычисляет постфиксное выражение (например, `?[a 1 +]`).
    """
    stack = []
    i = 0  # Индекс для перебора токенов

    while i < len(tokens):
        token = tokens[i]

        if token.isdigit():
            stack.append(int(token))
        elif token in constants:
            stack.append(constants[token])
        elif token == '+':
            if len(stack) < 2:
                raise ValueError("Недостаточно операндов для выполнения операции.")
            b, a = stack.pop(), stack.pop()
            stack.append(a + b)
        elif token == '-':
            if len(stack) < 2:
                raise ValueError("Недостаточно операндов для выполнения операции.")
            b, a = stack.pop(), stack.pop()
            stack.append(a - b)
        elif token == '*':
            if len(stack) < 2:
                raise ValueError("Недостаточно операндов для выполнения операции.")
            b, a = stack.pop(), stack.pop()
            stack.append(a * b)
        elif token == '/':
            if len(stack) < 2:
                raise ValueError("Недостаточно операндов для выполнения операции.")
            b, a = stack.pop(), stack.pop()
            stack.append(a / b)
        elif token == 'max':
            if len(stack) < 1:
                raise ValueError("Недостаточно операндов для операции max.")
            args = stack.pop()
            if isinstance(args, list):
                stack.append(max(args))
            else:
                raise ValueError("Ожидается список для функции max.")
        elif token == '[':
            # Начало массива, ищем элементы до ']'
            array_elements = []
            i += 1  # Переходим к следующему токену
            while i < len(tokens) and tokens[i] != ']':
                array_elements.append(int(tokens[i]))
                i += 1
            if i < len(tokens) and tokens[i] == ']':
                stack.append(array_elements)
        else:
            raise ValueError(f"Неизвестный токен: {token}")

        i += 1

    if len(stack) != 1:
        raise ValueError("Ошибка в выражении")

    return stack[0]