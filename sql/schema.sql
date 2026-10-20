-- ============================================
-- Система управления курьерами: структура БД
-- ============================================

CREATE TABLE IF NOT EXISTS couriers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    transport TEXT NOT NULL,
    zone TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'свободен',
    orders_done INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'диспетчер'
);

CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    number TEXT NOT NULL,
    address TEXT NOT NULL,
    recipient TEXT NOT NULL,
    phone TEXT NOT NULL,
    weight REAL NOT NULL,
    cost REAL NOT NULL,
    date TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'новый',
    courier_id INTEGER,
    user_id INTEGER,
    FOREIGN KEY (courier_id) REFERENCES couriers(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);