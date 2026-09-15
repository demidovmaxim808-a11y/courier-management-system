import storage

# Хранилище курьеров (загружается из файла)
couriers: list[dict] = storage.load_couriers()


def save() -> None:
    """Сохраняет курьеров в файл."""
    storage.save_couriers(couriers)


def add_courier(name: str, phone: str, transport: str, zone: str) -> dict:
    """Добавляет нового курьера."""
    courier = {
        "id": len(couriers) + 1,
        "name": name,
        "phone": phone,
        "transport": transport,
        "zone": zone,
        "status": "свободен",
        "orders_done": 0
    }
    couriers.append(courier)
    save()
    return courier


def find_courier_by_id(courier_id: int) -> dict | None:
    """Ищет курьера по ID."""
    for courier in couriers:
        if courier["id"] == courier_id:
            return courier
    return None


def find_couriers_by_name(name_part: str) -> list[dict]:
    """Ищет курьеров по части имени."""
    result = []
    for courier in couriers:
        if name_part.lower() in courier["name"].lower():
            result.append(courier)
    return result


def delete_courier(courier_id: int) -> bool:
    """Удаляет курьера по ID."""
    courier = find_courier_by_id(courier_id)
    if courier is None:
        return False
    couriers.remove(courier)
    save()
    return True


def update_courier_status(courier_id: int, new_status: str) -> bool:
    """Меняет статус курьера."""
    courier = find_courier_by_id(courier_id)
    if courier is None:
        return False
    courier["status"] = new_status
    save()
    return True


def get_available_couriers() -> list[dict]:
    """Возвращает список свободных курьеров."""
    return [c for c in couriers if c["status"] == "свободен"]


def print_courier(courier: dict) -> None:
    """Выводит одного курьера."""
    print(f"  ID: {courier['id']}")
    print(f"  Имя: {courier['name']}")
    print(f"  Телефон: {courier['phone']}")
    print(f"  Транспорт: {courier['transport']}")
    print(f"  Зона: {courier['zone']}")
    print(f"  Статус: {courier['status']}")
    print(f"  Выполнено заказов: {courier['orders_done']}")
    print("-" * 40)


def print_all_couriers() -> None:
    """Выводит всех курьеров."""
    if not couriers:
        print("\n⚠ Список курьеров пуст.")
        return
    print(f"\n📋 ВСЕГО КУРЬЕРОВ: {len(couriers)}")
    print("=" * 40)
    for courier in couriers:
        print_courier(courier)