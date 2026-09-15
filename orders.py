from datetime import date
import storage

orders: list[dict] = storage.load_orders()


def save() -> None:
    """Сохраняет заказы в файл."""
    storage.save_orders(orders)


def add_order(address: str, recipient: str, phone: str,
              weight: float, cost: float) -> dict:
    """Создаёт новый заказ."""
    order = {
        "id": len(orders) + 1,
        "number": f"ORD-2026-{len(orders) + 1:03d}",
        "address": address,
        "recipient": recipient,
        "phone": phone,
        "weight": weight,
        "cost": cost,
        "status": "новый",
        "courier_id": None,
        "date": str(date.today())
    }
    orders.append(order)
    save()
    return order


def find_order_by_id(order_id: int) -> dict | None:
    """Ищет заказ по ID."""
    for order in orders:
        if order["id"] == order_id:
            return order
    return None


def delete_order(order_id: int) -> bool:
    """Удаляет заказ."""
    order = find_order_by_id(order_id)
    if order is None:
        return False
    orders.remove(order)
    save()
    return True


def assign_order_to_courier(order_id: int, courier_id: int) -> tuple[bool, str]:
    """Назначает заказ курьеру."""
    order = find_order_by_id(order_id)
    if order is None:
        return False, "Заказ не найден"
    if order["status"] != "новый":
        return False, f"Заказ имеет статус '{order['status']}'"
    if order["weight"] > 10:
        return False, f"Вес {order['weight']} кг превышает лимит"
    order["courier_id"] = courier_id
    order["status"] = "в пути"
    save()
    return True, "Заказ успешно назначен"


def update_order_status(order_id: int, new_status: str) -> bool:
    """Обновляет статус заказа."""
    order = find_order_by_id(order_id)
    if order is None:
        return False
    order["status"] = new_status
    save()
    return True


def get_new_orders() -> list[dict]:
    """Возвращает новые заказы."""
    return [o for o in orders if o["status"] == "новый"]


def print_order(order: dict) -> None:
    """Выводит один заказ."""
    courier_info = "не назначен"
    if order["courier_id"] is not None:
        courier_info = f"ID {order['courier_id']}"
    print(f"  ID: {order['id']}")
    print(f"  Номер: {order['number']}")
    print(f"  Адрес: {order['address']}")
    print(f"  Получатель: {order['recipient']} ({order['phone']})")
    print(f"  Вес: {order['weight']} кг")
    print(f"  Стоимость: {order['cost']} руб.")
    print(f"  Статус: {order['status']}")
    print(f"  Курьер: {courier_info}")
    print(f"  Дата: {order['date']}")
    print("-" * 40)


def print_all_orders() -> None:
    """Выводит все заказы."""
    if not orders:
        print("\n⚠ Список заказов пуст.")
        return
    print(f"\n📋 ВСЕГО ЗАКАЗОВ: {len(orders)}")
    print("=" * 40)
    for order in orders:
        print_order(order)