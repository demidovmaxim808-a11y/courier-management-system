import json
import os
from typing import List

from models import Courier, Order, User
from models.couriers import find_courier_by_id
from models.users import find_user_by_id

DATA_DIR = "data"
COURIERS_FILE = os.path.join(DATA_DIR, "couriers.json")
ORDERS_FILE = os.path.join(DATA_DIR, "orders.json")
USERS_FILE = os.path.join(DATA_DIR, "users.json")


def ensure_data_dir() -> None:
    """Создать каталог data, если его нет."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def _load_raw(filename: str) -> list:
    """Прочитать JSON-файл, вернуть список словарей."""
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except (json.JSONDecodeError, OSError) as e:
        print(f"Ошибка чтения {filename}: {e}")
        return []


def _save_raw(filename: str, data: list) -> None:
    """Записать список словарей в JSON-файл."""
    ensure_data_dir()
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except OSError as e:
        print(f"Ошибка записи {filename}: {e}")


def load_couriers() -> List[Courier]:
    """Загрузить курьеров из JSON в объекты Courier."""
    raw = _load_raw(COURIERS_FILE)
    couriers = []
    for item in raw:
        courier = Courier(
            courier_id=item["id"],
            name=item["name"],
            phone=item["phone"],
            transport=item["transport"],
            zone=item["zone"],
            status=item.get("status", "свободен"),
            orders_done=item.get("orders_done", 0),
        )
        couriers.append(courier)
    return couriers


def save_couriers(couriers: List[Courier]) -> None:
    """Сохранить курьеров в JSON."""
    data = []
    for c in couriers:
        data.append({
            "id": c.id,
            "name": c.name,
            "phone": c.phone,
            "transport": c.transport,
            "zone": c.zone,
            "status": c.status,
            "orders_done": c.orders_done,
        })
    _save_raw(COURIERS_FILE, data)


def load_users() -> List[User]:
    """Загрузить пользователей из JSON в объекты User."""
    raw = _load_raw(USERS_FILE)
    users = []
    for item in raw:
        users.append(User.from_data(item))
    return users


def save_users(users: List[User]) -> None:
    """Сохранить пользователей в JSON."""
    data = []
    for u in users:
        data.append({
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "role": u.role,
        })
    _save_raw(USERS_FILE, data)


def load_orders(
    couriers: List[Courier], users: List[User]
) -> List[Order]:
    """Загрузить заказы из JSON, восстановив связи с Courier и User."""
    raw = _load_raw(ORDERS_FILE)
    orders = []
    for item in raw:
        courier = None
        user = None
        if item.get("courier_id") is not None:
            courier = find_courier_by_id(couriers, item["courier_id"])
        if item.get("user_id") is not None:
            user = find_user_by_id(users, item["user_id"])
        order = Order(
            order_id=item["id"],
            number=item["number"],
            address=item["address"],
            recipient=item["recipient"],
            phone=item["phone"],
            weight=item["weight"],
            cost=item["cost"],
            order_date=item["date"],
            courier=courier,
            user=user,
            status=item.get("status", "новый"),
        )
        orders.append(order)
    return orders


def save_orders(orders: List[Order]) -> None:
    """Сохранить заказы в JSON (объекты → ID)."""
    data = []
    for o in orders:
        courier_id = None
        if o.courier is not None:
            courier_id = o.courier.id
        user_id = None
        if o.user is not None:
            user_id = o.user.id
        data.append({
            "id": o.id,
            "number": o.number,
            "address": o.address,
            "recipient": o.recipient,
            "phone": o.phone,
            "weight": o.weight,
            "cost": o.cost,
            "date": o.date,
            "status": o.status,
            "courier_id": courier_id,
            "user_id": user_id,
        })
    _save_raw(ORDERS_FILE, data)