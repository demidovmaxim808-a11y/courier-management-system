from models import Courier
from models.couriers import (
    add_courier,
    delete_courier,
    find_courier_by_id,
    find_couriers_by_name,
    get_available_couriers,
    sort_couriers_by_name,
)


def test_courier_creation() -> None:
    """Проверка создания объекта Courier."""
    courier = Courier(1, "Иван", "+7-000", "авто", "Центр")
    assert courier.id == 1
    assert courier.name == "Иван"
    assert courier.status == "свободен"


def test_courier_is_available() -> None:
    """Проверка метода is_available()."""
    courier = Courier(1, "Иван", "+7-000", "авто", "Центр")
    assert courier.is_available()
    courier.set_status("занят")
    assert not courier.is_available()


def test_courier_can_take_order() -> None:
    """Проверка метода can_take_order()."""
    courier = Courier(1, "Иван", "+7-000", "авто", "Центр")
    assert courier.can_take_order(5.0)
    assert not courier.can_take_order(15.0)


def test_courier_str() -> None:
    """Проверка строкового представления."""
    courier = Courier(1, "Иван", "+7-000", "авто", "Центр")
    text = str(courier)
    assert "Иван" in text
    assert "свободен" in text


def test_add_courier() -> None:
    """Проверка добавления курьера в коллекцию."""
    couriers = []
    add_courier(couriers, "Иван", "+7-000", "авто", "Центр")
    assert len(couriers) == 1
    assert isinstance(couriers[0], Courier)


def test_find_courier_by_id() -> None:
    """Проверка поиска по ID."""
    couriers = []
    c = add_courier(couriers, "Иван", "+7-000", "авто", "Центр")
    found = find_courier_by_id(couriers, c.id)
    assert found is c


def test_find_couriers_by_name() -> None:
    """Проверка поиска по имени."""
    couriers = []
    add_courier(couriers, "Иван Петров", "+7-000", "авто", "Центр")
    add_courier(couriers, "Мария", "+7-111", "пешком", "Север")
    result = find_couriers_by_name(couriers, "иван")
    assert len(result) == 1


def test_delete_courier() -> None:
    """Проверка удаления курьера."""
    couriers = []
    c = add_courier(couriers, "Иван", "+7-000", "авто", "Центр")
    assert delete_courier(couriers, c.id)
    assert len(couriers) == 0


def test_get_available_couriers() -> None:
    """Проверка получения свободных курьеров."""
    couriers = []
    c1 = add_courier(couriers, "Свободный", "+7-000", "авто", "Центр")
    c2 = add_courier(couriers, "Занятый", "+7-111", "авто", "Центр")
    c2.set_status("занят")
    available = get_available_couriers(couriers)
    assert len(available) == 1
    assert available[0].id == c1.id


def test_sort_couriers_by_name() -> None:
    """Проверка сортировки по имени."""
    couriers = []
    add_courier(couriers, "Яна", "+7-000", "авто", "Центр")
    add_courier(couriers, "Анна", "+7-111", "пешком", "Север")
    sorted_list = sort_couriers_by_name(couriers)
    assert sorted_list[0].name == "Анна"