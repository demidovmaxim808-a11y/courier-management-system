from datetime import date

# ===== ДАННЫЕ О КУРЬЕРЕ =====
courier_name = "Алексей Иванов"
courier_phone = "+7 (999) 123-45-67"
courier_transport = "автомобиль"
courier_status = "свободен"  # возможные: "свободен", "занят", "не работает"
courier_zone = "Центральный район"

# ===== ДАННЫЕ О ЗАКАЗЕ =====
order_number = "ORD-2026-001"
order_address = "ул. Ленина, д. 15, кв. 8"
order_weight = 3.5  # кг
order_cost = 450.0  # рублей
order_status = "новый"  # возможные: "новый", "в пути", "доставлен", "отменен"
order_date = date.today()

# Контактные данные получателя
recipient_name = "Мария Петрова"
recipient_phone = "+7 (888) 765-43-21"

# ===== ПРОВЕРКА ВОЗМОЖНОСТИ НАЗНАЧЕНИЯ ЗАКАЗА =====
print("=" * 60)
print("СИСТЕМА УПРАВЛЕНИЯ КУРЬЕРАМИ")
print("Проверка возможности назначения заказа")
print("=" * 60)

# Вывод информации о курьере
print("\n📦 ИНФОРМАЦИЯ О КУРЬЕРЕ:")
print(f"  Имя: {courier_name}")
print(f"  Телефон: {courier_phone}")
print(f"  Транспорт: {courier_transport}")
print(f"  Текущий статус: {courier_status}")
print(f"  Зона обслуживания: {courier_zone}")

# Вывод информации о заказе
print("\n📋 ИНФОРМАЦИЯ О ЗАКАЗЕ:")
print(f"  Номер заказа: {order_number}")
print(f"  Адрес доставки: {order_address}")
print(f"  Вес: {order_weight} кг")
print(f"  Стоимость: {order_cost} руб.")
print(f"  Текущий статус: {order_status}")
print(f"  Дата создания: {order_date}")
print(f"  Получатель: {recipient_name}")
print(f"  Телефон получателя: {recipient_phone}")

# ===== АНАЛИЗ ВОЗМОЖНОСТИ НАЗНАЧЕНИЯ =====
print("\n" + "=" * 60)
print("ПРОВЕРКА ВОЗМОЖНОСТИ НАЗНАЧЕНИЯ ЗАКАЗА")
print("=" * 60)

# Проверка статуса курьера
if courier_status == "свободен":
    courier_available = True
    print("✓ Курьер доступен для работы")
elif courier_status == "занят":
    courier_available = False
    print("✗ Курьер уже занят другим заказом")
else:  # "не работает"
    courier_available = False
    print("✗ Курьер не работает сегодня")

# Проверка статуса заказа
if order_status == "новый":
    order_can_be_assigned = True
    print("✓ Заказ может быть назначен")
elif order_status == "в пути":
    order_can_be_assigned = False
    print("✗ Заказ уже в пути")
elif order_status == "доставлен":
    order_can_be_assigned = False
    print("✗ Заказ уже доставлен")
else:  # "отменен"
    order_can_be_assigned = False
    print("✗ Заказ отменен")

# ===== ИТОГОВОЕ РЕШЕНИЕ =====
print("\n" + "=" * 60)
print("ИТОГОВОЕ РЕШЕНИЕ")
print("=" * 60)

# Проверка веса заказа (дополнительное условие)
if order_weight > 10:
    print("⚠ ВНИМАНИЕ: вес заказа превышает 10 кг")
    # Изменяем статус, если доступность не определена
    if courier_available and order_can_be_assigned:
        courier_available = False
        print("  → Курьер не может взять заказ из-за большого веса")

# Вывод финального решения
if courier_available and order_can_be_assigned:
    print("\n✅ ЗАКАЗ МОЖЕТ БЫТЬ НАЗНАЧЕН КУРЬЕРУ")
    print(f"   Курьер: {courier_name}")
    print(f"   Заказ: {order_number}")
    print(f"   Примерное время доставки: 30-45 минут")
else:
    print("\n❌ ЗАКАЗ НЕ МОЖЕТ БЫТЬ НАЗНАЧЕН")
    if not courier_available:
        print("   Причина: курьер недоступен")
    elif not order_can_be_assigned:
        print("   Причина: заказ не готов к назначению")

print("\n" + "=" * 60)
print("Конец проверки")
print("=" * 60)

# ===== ИНФОРМАЦИЯ ДЛЯ ИМПОРТА (демонстрация импорта) =====
print("\n📚 ИНФОРМАЦИЯ О МОДУЛЯХ:")
print(f"  Модуль datetime использован для даты: {date.today()}")