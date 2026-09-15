import couriers
import orders
from utils import input_int, input_float, input_non_empty


def print_header() -> None:
    """Выводит заголовок программы."""
    print("\n" + "=" * 60)
    print("  СИСТЕМА УПРАВЛЕНИЯ КУРЬЕРАМИ")
    print("=" * 60)


def print_menu() -> None:
    """Выводит главное меню."""
    print("\n--- ГЛАВНОЕ МЕНЮ ---")
    print("1.  Добавить курьера")
    print("2.  Показать всех курьеров")
    print("3.  Найти курьера по имени")
    print("4.  Удалить курьера")
    print("5.  Изменить статус курьера")
    print("6.  Показать свободных курьеров")
    print("7.  Создать заказ")
    print("8.  Показать все заказы")
    print("9.  Назначить заказ курьеру")
    print("10. Изменить статус заказа")
    print("11. Удалить заказ")
    print("0.  Выход")
    print("-" * 40)


def menu_add_courier() -> None:
    """Пункт меню: добавить курьера."""
    print("\n--- ДОБАВЛЕНИЕ КУРЬЕРА ---")
    name = input_non_empty("Введите имя курьера: ")
    phone = input_non_empty("Введите телефон: ")
    transport = input_non_empty("Введите транспорт (автомобиль/велосипед/пешком): ")
    zone = input_non_empty("Введите зону обслуживания: ")

    courier = couriers.add_courier(name, phone, transport, zone)
    print(f"\n✅ Курьер добавлен! ID: {courier['id']}")


def menu_show_couriers() -> None:
    """Пункт меню: показать всех курьеров."""
    couriers.print_all_couriers()


def menu_find_courier() -> None:
    """Пункт меню: найти курьера по имени."""
    print("\n--- ПОИСК КУРЬЕРА ---")
    name_part = input_non_empty("Введите часть имени: ")
    found = couriers.find_couriers_by_name(name_part)

    if not found:
        print(f"\n⚠ Курьеры по запросу '{name_part}' не найдены.")
        return

    print(f"\n✅ Найдено курьеров: {len(found)}")
    print("=" * 40)
    for courier in found:
        couriers.print_courier(courier)


def menu_delete_courier() -> None:
    """Пункт меню: удалить курьера."""
    print("\n--- УДАЛЕНИЕ КУРЬЕРА ---")
    couriers.print_all_couriers()

    if not couriers.couriers:
        return

    courier_id = input_int("\nВведите ID курьера для удаления: ")

    if couriers.delete_courier(courier_id):
        print(f"✅ Курьер с ID {courier_id} удалён.")
    else:
        print(f"❌ Курьер с ID {courier_id} не найден.")


def menu_change_courier_status() -> None:
    """Пункт меню: изменить статус курьера."""
    print("\n--- ИЗМЕНЕНИЕ СТАТУСА КУРЬЕРА ---")
    couriers.print_all_couriers()

    if not couriers.couriers:
        return

    courier_id = input_int("\nВведите ID курьера: ")

    print("Выберите новый статус:")
    print("1. свободен")
    print("2. занят")
    print("3. не работает")
    choice = input("Ваш выбор: ").strip()

    statuses = {"1": "свободен", "2": "занят", "3": "не работает"}
    if choice not in statuses:
        print("❌ Некорректный выбор.")
        return

    if couriers.update_courier_status(courier_id, statuses[choice]):
        print(f"✅ Статус изменён на '{statuses[choice]}'.")
    else:
        print(f"❌ Курьер с ID {courier_id} не найден.")


def menu_show_available() -> None:
    """Пункт меню: показать свободных курьеров."""
    available = couriers.get_available_couriers()

    if not available:
        print("\n⚠ Нет свободных курьеров.")
        return

    print(f"\n✅ СВОБОДНЫХ КУРЬЕРОВ: {len(available)}")
    print("=" * 40)
    for courier in available:
        couriers.print_courier(courier)


def menu_add_order() -> None:
    """Пункт меню: создать заказ."""
    print("\n--- СОЗДАНИЕ ЗАКАЗА ---")
    address = input_non_empty("Введите адрес доставки: ")
    recipient = input_non_empty("Введите имя получателя: ")
    phone = input_non_empty("Введите телефон получателя: ")
    weight = input_float("Введите вес заказа (кг): ")
    cost = input_float("Введите стоимость заказа (руб.): ")

    order = orders.add_order(address, recipient, phone, weight, cost)
    print(f"\n✅ Заказ создан! Номер: {order['number']}, ID: {order['id']}")


def menu_show_orders() -> None:
    """Пункт меню: показать все заказы."""
    orders.print_all_orders()


def menu_assign_order() -> None:
    """Пункт меню: назначить заказ курьеру."""
    print("\n--- НАЗНАЧЕНИЕ ЗАКАЗА КУРЬЕРУ ---")

    new_orders = orders.get_new_orders()
    if not new_orders:
        print("\n⚠ Нет новых заказов для назначения.")
        return

    print("\n📋 Новые заказы:")
    print("=" * 40)
    for order in new_orders:
        orders.print_order(order)

    order_id = input_int("Введите ID заказа: ")

    available = couriers.get_available_couriers()
    if not available:
        print("\n⚠ Нет свободных курьеров.")
        return

    print("\n📦 Свободные курьеры:")
    print("=" * 40)
    for courier in available:
        couriers.print_courier(courier)

    courier_id = input_int("Введите ID курьера: ")

    success, message = orders.assign_order_to_courier(order_id, courier_id)
    if success:
        couriers.update_courier_status(courier_id, "занят")
        print(f"\n✅ {message}")
    else:
        print(f"\n❌ {message}")


def menu_change_order_status() -> None:
    """Пункт меню: изменить статус заказа."""
    print("\n--- ИЗМЕНЕНИЕ СТАТУСА ЗАКАЗА ---")
    orders.print_all_orders()

    if not orders.orders:
        return

    order_id = input_int("\nВведите ID заказа: ")

    print("Выберите новый статус:")
    print("1. новый")
    print("2. в пути")
    print("3. доставлен")
    print("4. отменен")
    choice = input("Ваш выбор: ").strip()

    statuses = {"1": "новый", "2": "в пути", "3": "доставлен", "4": "отменен"}
    if choice not in statuses:
        print("❌ Некорректный выбор.")
        return

    if orders.update_order_status(order_id, statuses[choice]):
        print(f"✅ Статус заказа изменён на '{statuses[choice]}'.")
    else:
        print(f"❌ Заказ с ID {order_id} не найден.")


def menu_delete_order() -> None:
    """Пункт меню: удалить заказ."""
    print("\n--- УДАЛЕНИЕ ЗАКАЗА ---")
    orders.print_all_orders()

    if not orders.orders:
        return

    order_id = input_int("\nВведите ID заказа для удаления: ")

    if orders.delete_order(order_id):
        print(f"✅ Заказ с ID {order_id} удалён.")
    else:
        print(f"❌ Заказ с ID {order_id} не найден.")


def main() -> None:
    """Точка запуска приложения."""
    print_header()
    print("\nДобро пожаловать в систему управления курьерами!")
    print(f"Загружено курьеров: {len(couriers.couriers)}")
    print(f"Загружено заказов: {len(orders.orders)}")

    while True:
        print_menu()
        choice = input("Выберите пункт меню: ").strip()

        if choice == "1":
            menu_add_courier()
        elif choice == "2":
            menu_show_couriers()
        elif choice == "3":
            menu_find_courier()
        elif choice == "4":
            menu_delete_courier()
        elif choice == "5":
            menu_change_courier_status()
        elif choice == "6":
            menu_show_available()
        elif choice == "7":
            menu_add_order()
        elif choice == "8":
            menu_show_orders()
        elif choice == "9":
            menu_assign_order()
        elif choice == "10":
            menu_change_order_status()
        elif choice == "11":
            menu_delete_order()
        elif choice == "0":
            print("\n👋 До свидания!")
            break
        else:
            print("\n❌ Некорректный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()