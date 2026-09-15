from datetime import datetime


def input_int(prompt: str) -> int:
    """Запрашивает целое число, повторяет при ошибке."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("❌ Ошибка: введите целое число.")


def input_float(prompt: str) -> float:
    """Запрашивает дробное число, повторяет при ошибке."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("❌ Ошибка: введите число.")


def input_non_empty(prompt: str) -> str:
    """Запрашивает непустую строку."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("❌ Ошибка: поле не может быть пустым.")


def input_date(prompt: str) -> str:
    """Запрашивает дату в формате ДД.ММ.ГГГГ."""
    while True:
        value = input(prompt)
        try:
            datetime.strptime(value, "%d.%m.%Y")
            return value
        except ValueError:
            print("❌ Ошибка: введите дату в формате ДД.ММ.ГГГГ.")