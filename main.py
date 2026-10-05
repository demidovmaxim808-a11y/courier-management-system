"""Система управления курьерами — точка входа."""

from typing import List

import storage
from models import Courier, Order, Route, User
from models.couriers import (
    add_courier,
    delete_courier,
    find_couriers_by_name,
    get_available_couriers,
    show_couriers,
    sort_couriers_by_name,
)
from models.orders import (
    add_order,
    assign_order_to_courier,
    cancel_order,
    delete_order,
    get_new_orders,
    show_orders,
)
from models.routes import (
    add_route,
    delete_route,
    find_routes_by_courier,
    get_active_routes,
    show_routes,
)
from models.users import add_user, find_user, find_user_by_id, show_users
from utils import input_float, input_int, input_non_empty


def print_header() -> None:
    """Заголовок программы."""
    print("\n" + "=" * 60)
    print("  СИСТЕМА УПРАВЛЕНИЯ КУРЬЕРАМИ")
    print("=" * 60)


def print_menu() -> None:
    """Главное меню."""
    print("\n--- ГЛАВНОЕ МЕНЮ ---")
    print("1.  Добавить курьера")
    print("2.  Показать всех курьеров")
    print("3.  Найти курьера по имени")
    print("4.  Удалить курьера")
    print("5.  Показать свободных курьеров")
    print("6.  Отсортировать курьеров по имени")
    print("7.  Добавить пользователя")
    print("8.  Показать пользователей")
    print("9.  Найти пользователя")
    print("10. Создать заказ")
    print("11. Показать все заказы")
    print("12. Назначить заказ курьеру")
    print("13. Отменить заказ")
    print("14. Удалить заказ")
    print("15. Создать маршрут")
    print("16. Показать маршруты")
    print("17. Маршруты курьера")
    print("18. Активные маршруты")
    print("19. Удалить маршрут")
    print("0.  Выход")
    print("-" * 40)


def menu_add_courier(couriers: List[Courier]) -> None:
    """Добавить курьера."""
    print("\n--- ДОБАВЛЕНИЕ КУРЬЕРА ---")
    name = input_non_empty("Имя: ")
    phone = input_non_empty("Телефон: ")
    transport = input_non_empty("Транспорт: ")
    zone = input_non_empty("Зона: ")
    courier = add_courier(couriers, name, phone, transport, zone)
    storage.save_couriers(couriers)
    print(f"Курьер добавлен. ID: {courier.id}")


def menu_find_courier(couriers: List[Courier]) -> None:
    """Найти курьера по имени."""
    query = input_non_empty("Часть имени: ")
    found = find_couriers_by_name(couriers, query)
    if not found:
        print("Курьеры не найдены.")
        return
    for c in found:
        print(f"  ID {c.id}: {c}")


def menu_delete_courier(couriers: List[Courier]) -> None:
    """Удалить курьера."""
    show_couriers(couriers)
    cid = input_int("ID курьера: ")
    if delete_courier(couriers, cid):
        storage.save_couriers(couriers)
        print(f"Курьер {cid} удалён.")
    else:
        print("Курьер не найден.")


def menu_show_available(couriers: List[Courier]) -> None:
    """Показать свободных курьеров."""
    available = get_available_couriers(couriers)
    if not available:
        print("Нет свободных курьеров.")
        return
    for c in available:
        print(f"  ID {c.id}: {c}")


def menu_sort_couriers(couriers: List[Courier]) -> None:
    """Сортировка курьеров по имени."""
    sorted_couriers = sort_couriers_by_name(couriers)
    for c in sorted_couriers:
        print(f"  ID {c.id}: {c}")


def menu_add_user(users: List[User]) -> None:
    """Добавить пользователя."""
    print("\n--- ДОБАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯ ---")
    name = input_non_empty("Имя: ")
    email = input_non_empty("Email: ")
    role = input_non_empty("Роль (диспетчер/админ): ")
    user = add_user(users, name, email, role)
    storage.save_users(users)
    print(f"Пользователь добавлен. ID: {user.id}")


def menu_find_user(users: List[User]) -> None:
    """Найти пользователя."""
    query = input_non_empty("Часть имени или email: ")
    found = find_user(users, query)
    if not found:
        print("Пользователи не найдены.")
        return
    for u in found:
        print(f"  ID {u.id}: {u}")


def menu_add_order(orders: List[Order]) -> None:
    """Создать заказ."""
    print("\n--- СОЗДАНИЕ ЗАКАЗА ---")
    address = input_non_empty("Адрес: ")
    recipient = input_non_empty("Получатель: ")
    phone = input_non_empty("Телефон: ")
    weight = input_float("Вес (кг): ")
    cost = input_float("Стоимость (руб.): ")
    order = add_order(orders, address, recipient, phone, weight, cost)
    storage.save_orders(orders)
    print(f"Заказ создан. ID: {order.id}, номер: {order.number}")


def menu_assign_order(
    orders: List[Order], couriers: List[Courier], users: List[User]
) -> None:
    """Назначить заказ курьеру."""
    new_orders = get_new_orders(orders)
    if not new_orders:
        print("Нет новых заказов.")
        return
    show_orders(new_orders)
    oid = input_int("ID заказа: ")

    available = get_available_couriers(couriers)
    if not available:
        print("Нет свободных курьеров.")
        return
    for c in available:
        print(f"  ID {c.id}: {c}")
    cid = input_int("ID курьера: ")

    if not users:
        print("Нет пользователей. Добавьте пользователя.")
        return
    show_users(users)
    uid = input_int("ID пользователя: ")

    courier = next((c for c in couriers if c.id == cid), None)
    user = find_user_by_id(users, uid)
    if courier is None or user is None:
        print("Курьер или пользователь не найден.")
        return

    if assign_order_to_courier(orders, oid, courier, user):
        storage.save_orders(orders)
        storage.save_couriers(couriers)
        print("Заказ назначен.")
    else:
        print("Не удалось назначить заказ (проверьте статус/вес).")


def menu_cancel_order(orders: List[Order], couriers: List[Courier]) -> None:
    """Отменить заказ."""
    show_orders(orders)
    oid = input_int("ID заказа: ")
    if cancel_order(orders, oid):
        storage.save_orders(orders)
        storage.save_couriers(couriers)
        print("Заказ отменён.")
    else:
        print("Заказ не найден.")


def menu_delete_order(orders: List[Order]) -> None:
    """Удалить заказ."""
    show_orders(orders)
    oid = input_int("ID заказа: ")
    if delete_order(orders, oid):
        storage.save_orders(orders)
        print("Заказ удалён.")
    else:
        print("Заказ не найден.")


def menu_add_route(
    routes: List[Route], couriers: List[Courier]
) -> None:
    """Создать маршрут для курьера."""
    print("\n--- СОЗДАНИЕ МАРШРУТА ---")
    if not couriers:
        print("Нет курьеров.")
        return
    show_couriers(couriers)
    cid = input_int("ID курьера: ")
    courier = next((c for c in couriers if c.id == cid), None)
    if courier is None:
        print("Курьер не найден.")
        return
    route_date = input_non_empty("Дата маршрута (ГГГГ-ММ-ДД): ")
    route = add_route(routes, courier, route_date)
    storage.save_routes(routes)
    print(f"Маршрут создан. ID: {route.id}")


def menu_show_routes(routes: List[Route]) -> None:
    """Показать все маршруты."""
    show_routes(routes)


def menu_routes_by_courier(
    routes: List[Route], couriers: List[Courier]
) -> None:
    """Показать маршруты конкретного курьера."""
    if not couriers:
        print("Нет курьеров.")
        return
    show_couriers(couriers)
    cid = input_int("ID курьера: ")
    courier = next((c for c in couriers if c.id == cid), None)
    if courier is None:
        print("Курьер не найден.")
        return
    found = find_routes_by_courier(routes, courier)
    if not found:
        print("Маршрутов нет.")
        return
    show_routes(found)


def menu_active_routes(routes: List[Route]) -> None:
    """Показать активные маршруты."""
    active = get_active_routes(routes)
    if not active:
        print("Активных маршрутов нет.")
        return
    show_routes(active)


def menu_delete_route(routes: List[Route]) -> None:
    """Удалить маршрут."""
    show_routes(routes)
    rid = input_int("ID маршрута: ")
    if delete_route(routes, rid):
        storage.save_routes(routes)
        print("Маршрут удалён.")
    else:
        print("Маршрут не найден.")


def main() -> None:
    """Точка запуска приложения."""
    print_header()

    couriers = storage.load_couriers()
    users = storage.load_users()
    orders = storage.load_orders(couriers, users)
    routes = storage.load_routes(couriers, orders)

    print(f"Загружено курьеров: {len(couriers)}")
    print(f"Загружено пользователей: {len(users)}")
    print(f"Загружено заказов: {len(orders)}")
    print(f"Загружено маршрутов: {len(routes)}")

    while True:
        print_menu()
        choice = input("Выбор: ").strip()

        if choice == "1":
            menu_add_courier(couriers)
        elif choice == "2":
            show_couriers(couriers)
        elif choice == "3":
            menu_find_courier(couriers)
        elif choice == "4":
            menu_delete_courier(couriers)
        elif choice == "5":
            menu_show_available(couriers)
        elif choice == "6":
            menu_sort_couriers(couriers)
        elif choice == "7":
            menu_add_user(users)
        elif choice == "8":
            show_users(users)
        elif choice == "9":
            menu_find_user(users)
        elif choice == "10":
            menu_add_order(orders)
        elif choice == "11":
            show_orders(orders)
        elif choice == "12":
            menu_assign_order(orders, couriers, users)
        elif choice == "13":
            menu_cancel_order(orders, couriers)
        elif choice == "14":
            menu_delete_order(orders)
        elif choice == "15":
            menu_add_route(routes, couriers)
        elif choice == "16":
            menu_show_routes(routes)
        elif choice == "17":
            menu_routes_by_courier(routes, couriers)
        elif choice == "18":
            menu_active_routes(routes)
        elif choice == "19":
            menu_delete_route(routes)
        elif choice == "0":
            print("\nДо свидания!")
            break
        else:
            print("Некорректный выбор.")


if __name__ == "__main__":
    main()
