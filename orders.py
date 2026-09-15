from datetime import date

# Хранилище заказов
orders = []


def add_order(address, recipient, phone, weight, cost):
    """Создаёт новый заказ."""
    order = {
        "id": len(orders) + 1,
        "number": f"ORD-2026-{len(orders) + 1:03d}",
        "address": address,
        "recipient": recipient,
        "phone": phone,
        "weight": weight,
        "cost": cost,
        "status": "новый",  # новый / в пути / доставлен / отменен
        "courier_id": None,
        "date": date.today()
    }
    orders.append(order)
    return order


def find_order_by_id(order_id):
    """Ищет заказ по ID."""
    for order in orders:
        if order["id"] == order_id:
            return order
    return None


def find_order_by_number(number):
    """Ищет заказ по номеру."""
    for order in orders:
        if order["number"] == number:
            return order
    return None


def delete_order(order_id):
    """Удаляет заказ."""
    order = find_order_by_id(order_id)
    if order is None:
        return False
    orders.remove(order)
    return True


def assign_order_to_courier(order_id, courier_id):
    """Назначает заказ курьеру."""
    order = find_order_by_id(order_id)
    if order is None:
        return False, "Заказ не найден"
    if order["status"] != "новый":
        return False, f"Заказ имеет статус '{order['status']}' и не может быть назначен"
    if order["weight"] > 10:
        return False, f"Вес заказа {order['weight']} кг превышает лимит (10 кг)"
    order["courier_id"] = courier_id
    order["status"] = "в пути"
    return True, "Заказ успешно назначен"


def update_order_status(order_id, new_status):
    """Обновляет статус заказа."""
    order = find_order_by_id(order_id)
    if order is None:
        return False
    order["status"] = new_status
    return True


def get_new_orders():
    """Возвращает список новых заказов."""
    result = []
    for order in orders:
        if order["status"] == "новый":
            result.append(order)
    return result


def print_order(order):
    """Красиво выводит один заказ."""
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


def print_all_orders():
    """Выводит все заказы."""
    if not orders:
        print("\n⚠ Список заказов пуст.")
        return
    print(f"\n📋 ВСЕГО ЗАКАЗОВ: {len(orders)}")
    print("=" * 40)
    for order in orders:
        print_order(order)