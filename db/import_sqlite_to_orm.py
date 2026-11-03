"""Перенос данных из базы ПР7 в Django ORM."""

import os
import sqlite3
import sys
from datetime import date
from pathlib import Path

import django
from django.db import transaction

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "couriermanager.settings")
django.setup()

# pylint: disable=wrong-import-position
from courier.models import Courier
from users.models import User
from order.models import Order
# pylint: enable=wrong-import-position

SOURCE_DB = BASE_DIR / "data" / "courier.sqlite"


def main() -> None:
    """Запуск скрипта переноса."""
    if not SOURCE_DB.exists():
        raise FileNotFoundError(f"База не найдена: {SOURCE_DB}")

    with sqlite3.connect(SOURCE_DB) as connection:
        connection.row_factory = sqlite3.Row

        users = connection.execute("SELECT * FROM users").fetchall()
        couriers = connection.execute("SELECT * FROM couriers").fetchall()
        orders = connection.execute("SELECT * FROM orders").fetchall()

        with transaction.atomic():
            # 1. Перенос пользователей
            for row in users:
                data = dict(row)
                User.objects.update_or_create(
                    pk=data["id"],
                    defaults={
                        "name": data["name"],
                        "email": data["email"],
                        "role": data.get("role", "диспетчер"),
                    },
                )

            # 2. Перенос курьеров
            for row in couriers:
                data = dict(row)
                Courier.objects.update_or_create(
                    pk=data["id"],
                    defaults={
                        "name": data["name"],
                        "phone": data["phone"],
                        "transport": data["transport"],
                        "zone": data["zone"],
                        "status": data["status"],
                        "orders_done": data["orders_done"],
                    },
                )

            # 3. Перенос заказов
            for row in orders:
                data = dict(row)
                order_date = date.fromisoformat(data["date"])
                Order.objects.update_or_create(
                    pk=data["id"],
                    defaults={
                        "number": data["number"],
                        "address": data["address"],
                        "recipient": data["recipient"],
                        "phone": data["phone"],
                        "weight": data["weight"],
                        "cost": data["cost"],
                        "date": order_date,
                        "status": data["status"],
                        "courier_id": data.get("courier_id"),
                        "user_id": data.get("user_id"),
                    },
                )

    print("✅ Данные успешно перенесены в Django ORM")


if __name__ == "__main__":
    main()