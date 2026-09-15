# tests/test_orders.py
import orders


def test_add_order():
    orders.orders.clear()
    orders.add_order("ул. Тест", "Пётр", "+7-000", 2.0, 100.0)
    assert len(orders.orders) == 1


def test_assign_order_weight_limit():
    orders.orders.clear()
    o = orders.add_order("ул. Тест", "Пётр", "+7-000", 15.0, 100.0)
    success, msg = orders.assign_order_to_courier(o["id"], 1)
    assert success is False
    assert "превышает" in msg


def test_assign_order_success():
    orders.orders.clear()
    o = orders.add_order("ул. Тест", "Пётр", "+7-000", 3.0, 100.0)
    success, msg = orders.assign_order_to_courier(o["id"], 1)
    assert success is True
    assert o["status"] == "в пути"


def test_find_order_by_id():
    orders.orders.clear()
    o = orders.add_order("ул. Тест", "Пётр", "+7-000", 2.0, 100.0)
    found = orders.find_order_by_id(o["id"])
    assert found is not None


def test_delete_order():
    orders.orders.clear()
    o = orders.add_order("ул. Тест", "Пётр", "+7-000", 2.0, 100.0)
    assert orders.delete_order(o["id"]) is True
    assert len(orders.orders) == 0
