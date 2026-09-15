import couriers
import orders


def print_header():
    """Выводит заголовок."""
    print("\n" + "=" * 60)
    print("  СИСТЕМА УПРАВЛЕНИЯ КУРЬЕРАМИ")
    print("=" * 60)


def print_menu():
    """Выводит главное меню."""
    print("\n--- ГЛАВНОЕ МЕНЮ ---")
    print("1. Добавить курьера")
    print("2. Показать всех курьеров")
    print("3. Найти курьера по имени")
    print("4. Удалить курьера")
    print("5. Изменить статус курьера")
    print("6. Показать свободных курьеров")
    print("7. Создать заказ")
    print("8. Показать все заказы")
    print("9. Назначить заказ курьеру")
    print("10. Изменить статус заказа")
    print("11. Удалить заказ")
    print("0. Выход")
    print("-" * 40)


def menu_add_courier():
    """Пункт меню: добавить курьера."""
    print("\n--- ДОБАВЛЕНИЕ КУРЬЕРА ---")
    name = input("Введите имя курьера: ")
    phone = input("Введите телефон: ")
    transport = input("Введите транспорт (автомобиль/велосипед/пешком): ")
    zone = input("Введите зону обслуживания: ")
    
    courier = couriers.add_courier(name, phone, transport, zone)
    print(f"\n✅ Курьер добавлен! ID: {courier['id']}")


def menu_show_couriers():
    """Пункт меню: показать всех курьеров."""
    couriers.print_all_couriers()


def menu_find_courier():
    """Пункт меню: найти курьера по имени."""
    print("\n--- ПОИСК КУРЬЕРА ---")
    name_part = input("Введите часть имени: ")
    found = couriers.find_couriers_by_name(name_part)
    
    if not found:
        print(f"\n⚠ Курьеры по запросу '{name_part}' не найдены.")
        return
    
    print(f"\n✅ Найдено курьеров: {len(found)}")
    print("=" * 40)
    for courier in found:
        couriers.print_courier(courier)


def menu_delete_courier():
    """Пункт меню: удалить курьера."""
    print("\n--- УДАЛЕНИЕ КУРЬЕРА ---")
    couriers.print_all_couriers()
    
    if not couriers.couriers:
        return
    
    try:
        courier_id = int(input("\nВведите ID курьера для удаления: "))
    except ValueError:
        print("❌ Некорректный ID.")
        return
    
    if couriers.delete_courier(courier_id):
        print(f"✅ Курьер с ID {courier_id} удалён.")
    else:
        print(f"❌ Курьер с ID {courier_id} не найден.")


def menu_change_courier_status():
    """Пункт меню: изменить статус курьера."""
    print("\n--- ИЗМЕНЕНИЕ СТАТУСА КУРЬЕРА ---")
    couriers.print_all_couriers()
    
    if not couriers.couriers:
        return
    
    try:
        courier_id = int(input("\nВведите ID курьера: "))
    except ValueError:
        print("❌ Некорректный ID.")
        return
    
    print("Выберите новый статус:")
    print("1. свободен")
    print("2. занят")
    print("3. не работает")
    choice = input("Ваш выбор: ")
    
    statuses = {"1": "свободен", "2": "занят", "3": "не работает"}
    if choice not in statuses:
        print("❌ Некорректный выбор.")
        return
    
    if couriers.update_courier_status(courier_id, statuses[choice]):
        print(f"✅ Статус изменён на '{statuses[choice]}'.")
    else:
        print(f"❌ Курьер с ID {courier_id} не найден.")


def menu_show_available():
    """Пункт меню: показать свободных курьеров."""
    available = couriers.get_available_couriers()
    
    if not available:
        print("\n⚠ Нет свободных курьеров.")
        return
    
    print(f"\n✅ СВОБОДНЫХ КУРЬЕРОВ: {len(available)}")
    print("=" * 40)
    for courier in available:
        couriers.print_courier(courier)


def menu_add_order():
    """Пункт меню: создать заказ."""
    print("\n--- СОЗДАНИЕ ЗАКАЗА ---")
    address = input("Введите адрес доставки: ")
    recipient = input("Введите имя получателя: ")
    phone = input("Введите телефон получателя: ")
    
    try:
        weight = float(input("Введите вес заказа (кг): "))
        cost = float(input("Введите стоимость заказа (руб.): "))
    except ValueError:
        print("❌ Некорректное число.")
        return
    
    order = orders.add_order(address, recipient, phone, weight, cost)
    print(f"\n✅ Заказ создан! Номер: {order['number']}, ID: {order['id']}")


def menu_show_orders():
    """Пункт меню: показать все заказы."""
    orders.print_all_orders()


def menu_assign_order():
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
    
    try:
        order_id = int(input("Введите ID заказа: "))
    except ValueError:
        print("❌ Некорректный ID.")
        return
    
    available = couriers.get_available_couriers()
    if not available:
        print("\n⚠ Нет свободных курьеров.")
        return
    
    print("\n📦 Свободные курьеры:")
    print("=" * 40)
    for courier in available:
        couriers.print_courier(courier)
    
    try:
        courier_id = int(input("Введите ID курьера: "))
    except ValueError:
        print("❌ Некорректный ID.")
        return
    
    success, message = orders.assign_order_to_courier(order_id, courier_id)
    if success:
        couriers.update_courier_status(courier_id, "занят")
        print(f"\n✅ {message}")
    else:
        print(f"\n❌ {message}")


def menu_change_order_status():
    """Пункт меню: изменить статус заказа."""
    print("\n--- ИЗМЕНЕНИЕ СТАТУСА ЗАКАЗА ---")
    orders.print_all_orders()
    
    if not orders.orders:
        return
    
    try:
        order_id = int(input("\nВведите ID заказа: "))
    except ValueError:
        print("❌ Некорректный ID.")
        return
    
    print("Выберите новый статус:")
    print("1. новый")
    print("2. в пути")
    print("3. доставлен")
    print("4. отменен")
    choice = input("Ваш выбор: ")
    
    statuses = {"1": "новый", "2": "в пути", "3": "доставлен", "4": "отменен"}
    if choice not in statuses:
        print("❌ Некорректный выбор.")
        return
    
    if orders.update_order_status(order_id, statuses[choice]):
        print(f"✅ Статус заказа изменён на '{statuses[choice]}'.")
    else:
        print(f"❌ Заказ с ID {order_id} не найден.")


def menu_delete_order():
    """Пункт меню: удалить заказ."""
    print("\n--- УДАЛЕНИЕ ЗАКАЗА ---")
    orders.print_all_orders()
    
    if not orders.orders:
        return
    
    try:
        order_id = int(input("\nВведите ID заказа для удаления: "))
    except ValueError:
        print("❌ Некорректный ID.")
        return
    
    if orders.delete_order(order_id):
        print(f"✅ Заказ с ID {order_id} удалён.")
    else:
        print(f"❌ Заказ с ID {order_id} не найден.")


def main():
    """Главная функция - запускает программу."""
    print_header()
    print("\nДобро пожаловать в систему управления курьерами!")
    
    while True:
        print_menu()
        choice = input("Выберите пункт меню: ")
        
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