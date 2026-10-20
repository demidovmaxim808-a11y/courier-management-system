"""Перенос данных из JSON-файлов в SQLite."""
import json
import sqlite3

from db.database import get_connection

COURIERS_FILE = "data/couriers.json"
USERS_FILE = "data/users.json"
ORDERS_FILE = "data/orders.json"


def load_json(filename: str) -> list:
    """Загрузить JSON-файл."""
    with open(filename, encoding="utf-8") as file:
        return json.load(file)


def import_couriers(conn: sqlite3.Connection) -> None:
    """Импорт курьеров."""
    couriers = load_json(COURIERS_FILE)
    conn.executemany(
        """
        INSERT INTO couriers (id, name, phone, transport, zone, status, orders_done)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                c["id"],
                c["name"],
                c["phone"],
                c["transport"],
                c["zone"],
                c["status"],
                c["orders_done"],
            )
            for c in couriers
        ],
    )


def import_users(conn: sqlite3.Connection) -> None:
    """Импорт пользователей."""
    users = load_json(USERS_FILE)
    conn.executemany(
        """
        INSERT INTO users (id, name, email, role)
        VALUES (?, ?, ?, ?)
        """,
        [
            (
                u["id"],
                u["name"],
                u["email"],
                u["role"],
            )
            for u in users
        ],
    )


def import_orders(conn: sqlite3.Connection) -> None:
    """Импорт заказов."""
    orders = load_json(ORDERS_FILE)
    conn.executemany(
        """
        INSERT INTO orders (
            id, number, address, recipient, phone,
            weight, cost, date, status, courier_id, user_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                o["id"],
                o["number"],
                o["address"],
                o["recipient"],
                o["phone"],
                o["weight"],
                o["cost"],
                o["date"],
                o["status"],
                o.get("courier_id"),
                o.get("user_id"),
            )
            for o in orders
        ],
    )


def main() -> None:
    """Запуск импорта."""
    conn = get_connection()
    try:
        import_couriers(conn)
        import_users(conn)
        import_orders(conn)
        conn.commit()
        print("✅ Импорт завершён успешно")
    except Exception as e:
        conn.rollback()
        print(f"❌ Ошибка импорта: {e}")
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
