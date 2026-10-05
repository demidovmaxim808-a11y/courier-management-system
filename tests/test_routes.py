"""Тесты класса Route."""

from models import Courier, Order, Route
from models.routes import (
    add_route,
    delete_route,
    find_route_by_id,
    find_routes_by_courier,
    get_active_routes,
    sort_routes_by_date,
)


def _make_courier(cid: int = 1, name: str = "Иван") -> Courier:
    """Создать тестового курьера."""
    return Courier(cid, name, "+7-000", "авто", "Центр")


def _make_order(oid: int = 1, weight: float = 3.0) -> Order:
    """Создать тестовый заказ."""
    return Order(
        oid, f"ORD-{oid:03d}", "ул. Ленина 15", "Мария",
        "+7-111", weight, 450.0, "2026-09-15"
    )


def test_route_creation() -> None:
    """Проверка создания объекта Route."""
    courier = _make_courier()
    route = Route(1, courier, "2026-09-15")
    assert route.id == 1
    assert route.courier is courier
    assert route.date == "2026-09-15"
    assert route.get_orders_count() == 0


def test_route_add_order() -> None:
    """Проверка добавления заказа в маршрут."""
    courier = _make_courier()
    route = Route(1, courier, "2026-09-15")
    order = _make_order()
    route.add_order(order)
    assert route.get_orders_count() == 1
    assert order in route.orders


def test_route_remove_order() -> None:
    """Проверка удаления заказа из маршрута."""
    courier = _make_courier()
    route = Route(1, courier, "2026-09-15")
    order = _make_order()
    route.add_order(order)
    assert route.remove_order(order)
    assert route.get_orders_count() == 0


def test_route_total_weight() -> None:
    """Проверка подсчёта общего веса."""
    courier = _make_courier()
    route = Route(1, courier, "2026-09-15")
    route.add_order(_make_order(1, 3.0))
    route.add_order(_make_order(2, 2.0))
    assert route.get_total_weight() == 5.0


def test_route_total_cost() -> None:
    """Проверка подсчёта общей стоимости."""
    courier = _make_courier()
    route = Route(1, courier, "2026-09-15")
    route.add_order(_make_order(1))
    route.add_order(_make_order(2))
    assert route.get_total_cost() == 900.0


def test_route_complete() -> None:
    """Проверка завершения маршрута."""
    courier = _make_courier()
    route = Route(1, courier, "2026-09-15")
    route.complete()
    assert route.is_completed


def test_route_str() -> None:
    """Проверка строкового представления."""
    courier = _make_courier()
    route = Route(1, courier, "2026-09-15")
    text = str(route)
    assert "Маршрут #1" in text
    assert "Иван" in text


def test_add_route() -> None:
    """Проверка добавления маршрута в коллекцию."""
    routes = []
    courier = _make_courier()
    add_route(routes, courier, "2026-09-15")
    assert len(routes) == 1
    assert isinstance(routes[0], Route)


def test_find_route_by_id() -> None:
    """Проверка поиска по ID."""
    routes = []
    courier = _make_courier()
    r = add_route(routes, courier, "2026-09-15")
    assert find_route_by_id(routes, r.id) is r


def test_find_routes_by_courier() -> None:
    """Проверка поиска маршрутов курьера."""
    routes = []
    c1 = _make_courier(1, "Иван")
    c2 = _make_courier(2, "Пётр")
    add_route(routes, c1, "2026-09-15")
    add_route(routes, c1, "2026-09-16")
    add_route(routes, c2, "2026-09-15")
    found = find_routes_by_courier(routes, c1)
    assert len(found) == 2


def test_get_active_routes() -> None:
    """Проверка фильтра активных маршрутов."""
    routes = []
    courier = _make_courier()
    r1 = add_route(routes, courier, "2026-09-15")
    r2 = add_route(routes, courier, "2026-09-16")
    r2.complete()
    active = get_active_routes(routes)
    assert len(active) == 1
    assert active[0].id == r1.id


def test_delete_route() -> None:
    """Проверка удаления маршрута."""
    routes = []
    courier = _make_courier()
    r = add_route(routes, courier, "2026-09-15")
    assert delete_route(routes, r.id)
    assert len(routes) == 0


def test_sort_routes_by_date() -> None:
    """Проверка сортировки маршрутов по дате."""
    routes = []
    courier = _make_courier()
    add_route(routes, courier, "2026-09-20")
    add_route(routes, courier, "2026-09-15")
    sorted_routes = sort_routes_by_date(routes)
    assert sorted_routes[0].date == "2026-09-15"
