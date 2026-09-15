# tests/test_couriers.py
import couriers


def test_add_courier():
    couriers.couriers.clear()
    couriers.add_courier("Тест", "+7-000", "пешком", "Тестовая")
    assert len(couriers.couriers) == 1


def test_find_courier_by_id():
    couriers.couriers.clear()
    c = couriers.add_courier("Иван", "+7-111", "авто", "Центр")
    found = couriers.find_courier_by_id(c["id"])
    assert found is not None
    assert found["name"] == "Иван"


def test_find_couriers_by_name():
    couriers.couriers.clear()
    couriers.add_courier("Алексей Иванов", "+7-222", "авто", "Центр")
    couriers.add_courier("Мария Петрова", "+7-333", "пешком", "Север")
    result = couriers.find_couriers_by_name("алексей")
    assert len(result) == 1


def test_delete_courier():
    couriers.couriers.clear()
    c = couriers.add_courier("Удаляемый", "+7-444", "авто", "Юг")
    assert couriers.delete_courier(c["id"]) is True
    assert len(couriers.couriers) == 0


def test_get_available_couriers():
    couriers.couriers.clear()
    couriers.add_courier("Свободный", "+7-555", "авто", "Центр")
    c2 = couriers.add_courier("Занятый", "+7-666", "авто", "Центр")
    couriers.update_courier_status(c2["id"], "занят")
    available = couriers.get_available_couriers()
    assert len(available) == 1
    assert available[0]["name"] == "Свободный"
