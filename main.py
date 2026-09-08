from datetime import date


# ===== ДОБАВЛЯЕМ ФУНКЦИЮ =====
def check_courier_availability(courier_status, order_status, order_weight):
    """
    Функция проверяет, может ли курьер взять заказ.
    
    Параметры:
    courier_status - статус курьера ("свободен", "занят", "не работает")
    order_status - статус заказа ("новый", "в пути", "доставлен", "отменен")
    order_weight - вес заказа в кг
    
    Возвращает:
    (available, reason) - кортеж с результатом и причиной
    """
    
    # Проверка статуса курьера
    if courier_status == "свободен":
        courier_available = True
    elif courier_status == "занят":
        courier_available = False
        return False, "Курьер уже занят другим заказом"
    else:  # "не работает"
        courier_available = False
        return False, "Курьер не работает сегодня"
    
    # Проверка статуса заказа
    if order_status == "новый":
        order_can_be_assigned = True
    elif order_status == "в пути":
        order_can_be_assigned = False
        return False, "Заказ уже в пути"
    elif order_status == "доставлен":
        order_can_be_assigned = False
        return False, "Заказ уже доставлен"
    else:  # "отменен"
        order_can_be_assigned = False
        return False, "Заказ отменен"
    
    # Проверка веса заказа
    if order_weight > 10:
        return False, f"Вес заказа {order_weight} кг превышает допустимый лимит (10 кг)"
    
    # Если все проверки пройдены
    return True, "Заказ может быть назначен"

# ===== ОСНОВНАЯ ПРОГРАММА =====

# Данные о курьере
courier_name = "Алексей Иванов"
courier_phone = "+7 (999) 123-45-67"
courier_transport = "автомобиль"
courier_status = "свободен"
courier_zone = "Центральный район"

# Данные о заказе
order_number = "ORD-2026-001"
order_address = "ул. Ленина, д. 15, кв. 8"
order_weight = 3.5  # кг
order_cost = 450.0  # рублей
order_status = "новый"
order_date = date.today()

# Контактные данные получателя
recipient_name = "Мария Петрова"
recipient_phone = "+7 (888) 765-43-21"

# ===== ВЫВОД ИНФОРМАЦИИ =====
print("=" * 60)
print("СИСТЕМА УПРАВЛЕНИЯ КУРЬЕРАМИ")
print("Проверка возможности назначения заказа")
print("=" * 60)

print("\n📦 ИНФОРМАЦИЯ О КУРЬЕРЕ:")
print(f"  Имя: {courier_name}")
print(f"  Телефон: {courier_phone}")
print(f"  Транспорт: {courier_transport}")
print(f"  Текущий статус: {courier_status}")
print(f"  Зона обслуживания: {courier_zone}")

print("\n📋 ИНФОРМАЦИЯ О ЗАКАЗЕ:")
print(f"  Номер заказа: {order_number}")
print(f"  Адрес доставки: {order_address}")
print(f"  Вес: {order_weight} кг")
print(f"  Стоимость: {order_cost} руб.")
print(f"  Текущий статус: {order_status}")
print(f"  Дата создания: {order_date}")
print(f"  Получатель: {recipient_name}")
print(f"  Телефон получателя: {recipient_phone}")

# ===== ВЫЗОВ ФУНКЦИИ =====
print("\n" + "=" * 60)
print("РЕЗУЛЬТАТ ПРОВЕРКИ (с использованием функции)")
print("=" * 60)

# Вызываем функцию и получаем результат
is_available, message = check_courier_availability(
    courier_status, 
    order_status, 
    order_weight
)

# Выводим результат на основе возвращенных данных
if is_available:
    print("\n✅ ЗАКАЗ МОЖЕТ БЫТЬ НАЗНАЧЕН КУРЬЕРУ")
    print(f"   Курьер: {courier_name}")
    print(f"   Заказ: {order_number}")
    print(f"   Вес: {order_weight} кг")
    print(f"   Статус курьера: {courier_status}")
    print(f"   Статус заказа: {order_status}")
    print(f"   Примерное время доставки: 30-45 минут")
else:
    print("\n❌ ЗАКАЗ НЕ МОЖЕТ БЫТЬ НАЗНАЧЕН")
    print(f"   Причина: {message}")

print("\n" + "=" * 60)
print("Конец проверки")
print("=" * 60)

print("\n📚 ИНФОРМАЦИЯ О МОДУЛЯХ:")
print(f"  Модуль datetime использован для даты: {date.today()}")