"""Подключение к базе данных SQLite."""

import sqlite3

DB_PATH = "data/courier.sqlite"


def get_connection() -> sqlite3.Connection:
    """Создать соединение с БД с поддержкой внешних ключей."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
