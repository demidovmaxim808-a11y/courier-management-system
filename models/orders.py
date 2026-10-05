"""Класс Order и функции работы с коллекцией заказов."""

from datetime import date
from typing import List, Optional, TYPE_CHECKING

from .couriers import Courier
from .users import User

if TYPE_CHECKING:
    from .routes import Route


class Order:
    """Заказ на доставку."""

    def __init__(
        self,
        order_id: int,
        number: str,
        address: str,
        recipient: str,
        phone: str,
        weight: float,
        cost: float,
        order_date: str,
        courier: Optional[Courier] = None,
        user: Optional[User] = None,
        status: str = "новый",
        route: Optional["Route"] = None,
    ) -> None:
        """Создать объект заказа."""
        self.id = order_id
        self.number = number
        self.address = address
        self.recipient = recipient
        self.phone = phone
        self.weight = weight
        self.cost = cost
        self.date = order_date
        self.courier = courier
        self.user = user
        self.status = status
        self.route = route

    def assign_to_route(self, route: "Route") -> None:
        """Добавить заказ в маршрут."""
        self.route = route
        route.add_order(self)

    def is_in_route(self) -> bool:
        """Проверить, привязан ли заказ к маршруту."""
        return self.route is not None

    def assign_to(self, courier: Courier, user: User) -> None:
        """Назначить заказ курьеру."""
        self.courier = courier
        self.user = user
        self.status = "в пути"
        courier.set_status("занят")

    def cancel(self) -> None:
        """Отменить заказ."""
        self.status = "отменен"
        if self.courier is not None and self.courier.status == "занят":
            self.courier.set_status("свободен")
        if self.route is not None:
            self.route.remove_order(self)
            self.route = None

    def complete(self) -> None:
        """Завершить заказ."""
        self.status = "доставлен"
        if self.courier is not None:
            self.courier.complete_order()

    def is_new(self) -> bool:
        """Проверить, новый ли заказ."""
        return self.status == "новый"

    def __str__(self) -> str:
        """Строковое представление заказа."""
        courier_info = "не назначен"
        if self.courier is not None:
            courier_info = self.courier.name
        route_info = ""
        if self.route is not None:
            route_info = f" | маршрут #{self.route.id}"
        return (
            f"{self.number}: {self.address} | "
            f"вес {self.weight} кг | статус: {self.status} | "
            f"курьер: {courier_info}{route_info}"
        )


def find_order_by_id(
    orders: List[Order], order_id: int
) -> Optional[Order]:
    """Найти заказ по идентификатору."""
    for order in orders:
        if order.id == order_id:
            return order
    return None


def get_new_orders(orders: List[Order]) -> List[Order]:
    """Получить список новых заказов."""
    return [o for o in orders if o.is_new()]


def add_order(
    orders: List[Order],
    address: str,
    recipient: str,
    phone: str,
    weight: float,
    cost: float,
) -> Order:
    """Создать объект Order и добавить его в коллекцию."""
    new_id = len(orders) + 1
    number = f"ORD-2026-{new_id:03d}"
    order_date = str(date.today())
    order = Order(
        order_id=new_id,
        number=number,
        address=address,
        recipient=recipient,
        phone=phone,
        weight=weight,
        cost=cost,
        order_date=order_date,
    )
    orders.append(order)
    return order


def assign_order_to_courier(
    orders: List[Order],
    order_id: int,
    courier: Courier,
    user: User,
) -> bool:
    """Назначить заказ курьеру с проверками."""
    order = find_order_by_id(orders, order_id)
    if order is None:
        return False
    if not order.is_new():
        return False
    if not courier.can_take_order(order.weight):
        return False
    order.assign_to(courier, user)
    return True


def cancel_order(orders: List[Order], order_id: int) -> bool:
    """Отменить заказ."""
    order = find_order_by_id(orders, order_id)
    if order is None:
        return False
    order.cancel()
    return True


def delete_order(orders: List[Order], order_id: int) -> bool:
    """Удалить заказ из коллекции."""
    order = find_order_by_id(orders, order_id)
    if order is None:
        return False
    orders.remove(order)
    return True


def show_orders(orders: List[Order]) -> None:
    """Вывести список заказов."""
    if not orders:
        print("\nСписок заказов пуст.")
        return
    print(f"\nВСЕГО ЗАКАЗОВ: {len(orders)}")
    print("-" * 50)
    for order in orders:
        print(f"  ID {order.id}: {order}")
    print("-" * 50)