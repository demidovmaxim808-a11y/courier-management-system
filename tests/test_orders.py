from models import Courier, Order, User
from models.orders import (
    add_order,
    assign_order_to_courier,
    cancel_order,
    delete_order,
    find_order_by_id,
    get_new_orders,
)


def _make_courier() -> Courier:
    """Создать тестового курьера."""
    return Courier(1, "Иван", "+7-000", "авто", "Центр")


def _make_user() -> User:
    """Создать тестового пользователя."""
    return User(1, "Диспетчер", "disp@example.com")


def test_order_creation() -> None:
    """Проверка создания объекта Order."""
    order = Order(
        1, "ORD-001", "ул. Ленина 15", "Мария",
        "+7-111", 3.5, 450.0, "2026-09-15"
    )
    assert order.id == 1
    assert order.status == "новый"
    assert order.courier is None


def test_order_assign() -> None:
    """Проверка метода assign_to()."""
    order = Order(
        1, "ORD-001", "ул. Ленина 15", "Мария",
        "+7-111", 3.5, 450.0, "2026-09-15"
    )
    courier = _make_courier()
    user = _make_user()
    order.assign_to(courier, user)
    assert order.courier is courier
    assert order.user is user
    assert order.status == "в пути"
    assert courier.status == "занят"


def test_order_cancel() -> None:
    """Проверка метода cancel()."""
    order = Order(
        1, "ORD-001", "ул. Ленина 15", "Мария",
        "+7-111", 3.5, 450.0, "2026-09-15"
    )
    courier = _make_courier()
    user = _make_user()
    order.assign_to(courier, user)
    order.cancel()
    assert order.status == "отменен"
    assert courier.status == "свободен"


def test_order_complete() -> None:
    """Проверка метода complete()."""
    order = Order(
        1, "ORD-001", "ул. Ленина 15", "Мария",
        "+7-111", 3.5, 450.0, "2026-09-15"
    )
    courier = _make_courier()
    user = _make_user()
    order.assign_to(courier, user)
    order.complete()
    assert order.status == "доставлен"
    assert courier.orders_done == 1


def test_order_str() -> None:
    """Проверка строкового представления."""
    order = Order(
        1, "ORD-001", "ул. Ленина 15", "Мария",
        "+7-111", 3.5, 450.0, "2026-09-15"
    )
    text = str(order)
    assert "ORD-001" in text
    assert "новый" in text


def test_add_order() -> None:
    """Проверка добавления заказа."""
    orders = []
    add_order(orders, "ул. Ленина 15", "Мария", "+7-111", 3.5, 450.0)
    assert len(orders) == 1
    assert isinstance(orders[0], Order)


def test_assign_order_to_courier() -> None:
    """Проверка функции назначения заказа."""
    orders = []
    o = add_order(orders, "ул. Ленина 15", "Мария", "+7-111", 3.5, 450.0)
    courier = _make_courier()
    user = _make_user()
    assert assign_order_to_courier(orders, o.id, courier, user)
    assert o.status == "в пути"


def test_assign_order_weight_limit() -> None:
    """Проверка запрета при весе > 10 кг."""
    orders = []
    o = add_order(orders, "ул. Ленина 15", "Мария", "+7-111", 15.0, 450.0)
    courier = _make_courier()
    user = _make_user()
    assert not assign_order_to_courier(orders, o.id, courier, user)


def test_cancel_order() -> None:
    """Проверка отмены заказа."""
    orders = []
    o = add_order(orders, "ул. Ленина 15", "Мария", "+7-111", 3.5, 450.0)
    assert cancel_order(orders, o.id)
    assert o.status == "отменен"


def test_delete_order() -> None:
    """Проверка удаления заказа."""
    orders = []
    o = add_order(orders, "ул. Ленина 15", "Мария", "+7-111", 3.5, 450.0)
    assert delete_order(orders, o.id)
    assert len(orders) == 0


def test_get_new_orders() -> None:
    """Проверка получения новых заказов."""
    orders = []
    add_order(orders, "ул. Ленина 15", "Мария", "+7-111", 3.5, 450.0)
    o2 = add_order(orders, "ул. Мира 20", "Пётр", "+7-222", 2.0, 300.0)
    o2.status = "в пути"
    new_orders = get_new_orders(orders)
    assert len(new_orders) == 1


def test_find_order_by_id() -> None:
    """Проверка поиска заказа."""
    orders = []
    o = add_order(orders, "ул. Ленина 15", "Мария", "+7-111", 3.5, 450.0)
    assert find_order_by_id(orders, o.id) is o