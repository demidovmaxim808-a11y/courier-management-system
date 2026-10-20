-- ========================================================
-- Запросы для Системы управления курьерами (ПР7)
-- ========================================================

-- 1. ВЫБОРКА СПИСКА: Все курьеры, отсортированные по имени
SELECT id, name, transport, zone, status
FROM couriers
ORDER BY name;

-- 2. ВЫБОРКА СПИСКА: Все заказы, отсортированные по дате
SELECT id, number, address, weight, cost, date, status
FROM orders
ORDER BY date DESC;

-- 3. ФИЛЬТРАЦИЯ (WHERE): Курьеры в определённой зоне
SELECT id, name, phone
FROM couriers
WHERE zone = 'Центральный район';

-- 4. ФИЛЬТРАЦИЯ (WHERE): Тяжёлые заказы (вес больше 5 кг)
SELECT id, number, weight, cost
FROM orders
WHERE weight > 5.0
ORDER BY weight DESC;

-- 5. СОЕДИНЕНИЕ (JOIN): Заказы с именами назначенных курьеров
SELECT o.id, o.number, o.status, c.name AS courier_name
FROM orders o
JOIN couriers c ON o.courier_id = c.id
ORDER BY o.date;

-- 6. СОЕДИНЕНИЕ (JOIN): Заказы с именами диспетчеров (пользователей)
SELECT o.id, o.number, u.name AS user_name, u.email
FROM orders o
JOIN users u ON o.user_id = u.id;

-- 7. АГРЕГАТНАЯ ФУНКЦИЯ: Общее количество курьеров
SELECT COUNT(*) AS total_couriers FROM couriers;

-- 8. АГРЕГАТНАЯ ФУНКЦИЯ: Количество свободных курьеров
SELECT COUNT(*) AS free_couriers
FROM couriers
WHERE status = 'свободен';

-- 9. ГРУППИРОВКА (GROUP BY): Количество заказов у каждого курьера
SELECT c.name AS courier_name, COUNT(o.id) AS orders_count
FROM couriers c
LEFT JOIN orders o ON c.id = o.courier_id
GROUP BY c.id, c.name
ORDER BY orders_count DESC;

-- 10. ФИЛЬТРАЦИЯ ГРУПП (HAVING): Курьеры, выполнившие больше 0 заказов
SELECT c.name AS courier_name, COUNT(o.id) AS orders_count
FROM couriers c
JOIN orders o ON c.id = o.courier_id
GROUP BY c.id, c.name
HAVING COUNT(o.id) > 0
ORDER BY orders_count DESC;