from typing import List, Optional


class Courier:
    """Курьер службы доставки."""

    def __init__(
        self,
        courier_id: int,
        name: str,
        phone: str,
        transport: str,
        zone: str,
        status: str = "свободен",
        orders_done: int = 0,
    ) -> None:
        """Создать объект курьера."""
        self.id = courier_id
        self.name = name
        self.phone = phone
        self.transport = transport
        self.zone = zone
        self.status = status
        self.orders_done = orders_done

    def is_available(self) -> bool:
        """Проверить, свободен ли курьер."""
        return self.status == "свободен"

    def can_take_order(self, weight: float) -> bool:
        """Проверить, может ли курьер взять заказ заданного веса."""
        return self.is_available() and weight <= 10

    def complete_order(self) -> None:
        """Отметить выполнение заказа."""
        self.orders_done += 1
        self.status = "свободен"

    def set_status(self, new_status: str) -> None:
        """Изменить статус курьера."""
        self.status = new_status

    def __str__(self) -> str:
        """Строковое представление курьера."""
        return (
            f"{self.name} ({self.transport}), зона: {self.zone}, "
            f"статус: {self.status}"
        )


def find_courier_by_id(
    couriers: List[Courier], courier_id: int
) -> Optional[Courier]:
    """Найти курьера по идентификатору."""
    for courier in couriers:
        if courier.id == courier_id:
            return courier
    return None


def find_couriers_by_name(
    couriers: List[Courier], query: str
) -> List[Courier]:
    """Найти курьеров по части имени."""
    result = []
    for courier in couriers:
        if query.lower() in courier.name.lower():
            result.append(courier)
    return result


def get_available_couriers(couriers: List[Courier]) -> List[Courier]:
    """Получить список свободных курьеров."""
    return [c for c in couriers if c.is_available()]


def sort_couriers_by_name(couriers: List[Courier]) -> List[Courier]:
    """Отсортировать курьеров по имени (lambda-функция)."""
    return sorted(couriers, key=lambda c: c.name)


def add_courier(
    couriers: List[Courier],
    name: str,
    phone: str,
    transport: str,
    zone: str,
) -> Courier:
    """Создать объект Courier и добавить его в коллекцию."""
    new_id = len(couriers) + 1
    courier = Courier(new_id, name, phone, transport, zone)
    couriers.append(courier)
    return courier


def delete_courier(couriers: List[Courier], courier_id: int) -> bool:
    """Удалить курьера по идентификатору."""
    courier = find_courier_by_id(couriers, courier_id)
    if courier is None:
        return False
    couriers.remove(courier)
    return True


def show_couriers(couriers: List[Courier]) -> None:
    """Вывести список курьеров."""
    if not couriers:
        print("\nСписок курьеров пуст.")
        return
    print(f"\nВСЕГО КУРЬЕРОВ: {len(couriers)}")
    print("-" * 50)
    for courier in couriers:
        print(f"  ID {courier.id}: {courier}")
    print("-" * 50)