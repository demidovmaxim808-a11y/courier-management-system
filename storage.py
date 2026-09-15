import json
import os

DATA_DIR = "data"
COURIERS_FILE = os.path.join(DATA_DIR, "couriers.json")
ORDERS_FILE = os.path.join(DATA_DIR, "orders.json")


def ensure_data_dir() -> None:
    """Создаёт каталог data, если его нет."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def load_data(filename: str) -> list:
    """Загружает список словарей из JSON-файла."""
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(f"⚠ Ошибка чтения {filename}: {e}")
        return []


def save_data(filename: str, data: list) -> None:
    """Сохраняет список словарей в JSON-файл."""
    ensure_data_dir()
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except OSError as e:
        print(f"⚠ Ошибка записи {filename}: {e}")


def load_couriers() -> list:
    """Загружает курьеров."""
    return load_data(COURIERS_FILE)


def save_couriers(couriers: list) -> None:
    """Сохраняет курьеров."""
    save_data(COURIERS_FILE, couriers)


def load_orders() -> list:
    """Загружает заказы."""
    return load_data(ORDERS_FILE)


def save_orders(orders: list) -> None:
    """Сохраняет заказы."""
    save_data(ORDERS_FILE, orders)