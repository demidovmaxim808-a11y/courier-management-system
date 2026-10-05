from typing import List, Optional

from .couriers import Courier
from .orders import Order


class Route:
    """Маршрут курьера на определённую дату."""

    def __init__(
        self,
        route_id: int,
        courier: Courier,
        route_date: str,
        orders: Optional[List[Order]] = None,
        is_completed: bool = False,
    ) -> None:
        """Создать объект маршрута."""
        self.id = route_id
        self.courier = courier
        self.date = route_date
        self.orders: List[Order] = orders if orders is not None else []
        self.is_completed = is_completed

    def add_order(self, order: Order) -> None:
        """Добавить заказ в маршрут."""
        if order not in self.orders:
            self.orders.append(order)

    def remove_order(self, order: Order) -> bool:
        """Удалить заказ из маршрута."""
        if order in self.orders:
            self.orders.remove(order)
            return True
        return False

    def get_total_weight(self) -> float:
        """Подсчитать общий вес заказов в маршруте."""
        total = 0.0
        for order in self.orders:
            total += order.weight
        return total

    def get_total_cost(self) -> float:
        """Подсчитать общую стоимость заказов."""
        total = 0.0
        for order in self.orders:
            total += order.cost
        return total

    def get_orders_count(self) -> int:
        """Вернуть количество заказов в маршруте."""
        return len(self.orders)

    def complete(self) -> None:
        """Отметить маршрут как выполненный."""
        self.is_completed = True

    def __str__(self) -> str:
        """Строковое представление маршрута."""
        status = "выполнен" if self.is_completed else "активен"
        return (
            f"Маршрут #{self.id} ({self.date}) | "
            f"курьер: {self.courier.name} | "
            f"заказов: {self.get_orders_count()} | "
            f"вес: {self.get_total_weight()} кг | "
            f"статус: {status}"
        )


def find_route_by_id(
    routes: List[Route], route_id: int
) -> Optional[Route]:
    """Найти маршрут по идентификатору."""
    for route in routes:
        if route.id == route_id:
            return route
    return None


def find_routes_by_courier(
    routes: List[Route], courier: Courier
) -> List[Route]:
    """Найти все маршруты конкретного курьера."""
    return [r for r in routes if r.courier is courier]


def find_routes_by_date(
    routes: List[Route], route_date: str
) -> List[Route]:
    """Найти все маршруты на указанную дату."""
    return [r for r in routes if r.date == route_date]


def get_active_routes(routes: List[Route]) -> List[Route]:
    """Получить список активных маршрутов."""
    return [r for r in routes if not r.is_completed]


def add_route(
    routes: List[Route],
    courier: Courier,
    route_date: str,
) -> Route:
    """Создать объект Route и добавить его в коллекцию."""
    new_id = len(routes) + 1
    route = Route(new_id, courier, route_date)
    routes.append(route)
    return route


def delete_route(routes: List[Route], route_id: int) -> bool:
    """Удалить маршрут по идентификатору."""
    route = find_route_by_id(routes, route_id)
    if route is None:
        return False
    routes.remove(route)
    return True


def sort_routes_by_date(routes: List[Route]) -> List[Route]:
    """Отсортировать маршруты по дате."""
    return sorted(routes, key=lambda r: r.date)


def show_routes(routes: List[Route]) -> None:
    """Вывести список маршрутов."""
    if not routes:
        print("\nСписок маршрутов пуст.")
        return
    print(f"\nВСЕГО МАРШРУТОВ: {len(routes)}")
    print("-" * 60)
    for route in routes:
        print(f"  ID {route.id}: {route}")
    print("-" * 60)