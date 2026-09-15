couriers = []


def add_courier(name, phone, transport, zone):
    """Добавляет нового курьера в систему."""
    courier = {
        "id": len(couriers) + 1,
        "name": name,
        "phone": phone,
        "transport": transport,
        "zone": zone,
        "status": "свободен",  # свободен / занят / не работает
        "orders_done": 0
    }
    couriers.append(courier)
    return courier


def find_courier_by_id(courier_id):
    """Ищет курьера по ID. Возвращает словарь или None."""
    for courier in couriers:
        if courier["id"] == courier_id:
            return courier
    return None


def find_couriers_by_name(name_part):
    """Ищет курьеров по части имени. Возвращает список."""
    result = []
    for courier in couriers:
        if name_part.lower() in courier["name"].lower():
            result.append(courier)
    return result


def delete_courier(courier_id):
    """Удаляет курьера по ID. Возвращает True/False."""
    courier = find_courier_by_id(courier_id)
    if courier is None:
        return False
    couriers.remove(courier)
    return True


def update_courier_status(courier_id, new_status):
    """Меняет статус курьера."""
    courier = find_courier_by_id(courier_id)
    if courier is None:
        return False
    courier["status"] = new_status
    return True


def get_available_couriers():
    """Возвращает список свободных курьеров."""
    result = []
    for courier in couriers:
        if courier["status"] == "свободен":
            result.append(courier)
    return result


def print_courier(courier):
    """Красиво выводит одного курьера."""
    print(f"  ID: {courier['id']}")
    print(f"  Имя: {courier['name']}")
    print(f"  Телефон: {courier['phone']}")
    print(f"  Транспорт: {courier['transport']}")
    print(f"  Зона: {courier['zone']}")
    print(f"  Статус: {courier['status']}")
    print(f"  Выполнено заказов: {courier['orders_done']}")
    print("-" * 40)


def print_all_couriers():
    """Выводит всех курьеров."""
    if not couriers:
        print("\n⚠ Список курьеров пуст.")
        return
    print(f"\n📋 ВСЕГО КУРЬЕРОВ: {len(couriers)}")
    print("=" * 40)
    for courier in couriers:
        print_courier(courier)