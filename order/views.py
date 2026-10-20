"""View-функции приложения order (работа с SQLite)."""

import sqlite3

from django.shortcuts import render

DB_PATH = "data/courier.sqlite"


def orders_list(request):
    """Страница /orders/: список заказов с именами курьеров (JOIN)."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    orders = conn.execute("""
        SELECT o.id, o.number, o.address, o.status,
               c.name AS courier_name
        FROM orders o
        LEFT JOIN couriers c ON o.courier_id = c.id
        ORDER BY o.date DESC;
    """).fetchall()
    conn.close()

    context = {"orders": orders}
    return render(request, "order/order_list.html", context)


def order_detail(request, order_id):
    """Страница /orders/<int:order_id>/."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    order = conn.execute("""
        SELECT o.*,
               c.name AS courier_name,
               u.name AS user_name
        FROM orders o
        LEFT JOIN couriers c ON o.courier_id = c.id
        LEFT JOIN users u ON o.user_id = u.id
        WHERE o.id = ?;
    """, (order_id,)).fetchone()
    conn.close()

    context = {"order": order}
    return render(
        request,
        "order/order_detail.html",
        context,
        status=404 if order is None else 200,
    )


def order_statistics(request):
    """Страница статистики: количество заказов у каждого курьера (GROUP BY)."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    stats = conn.execute("""
        SELECT c.name AS courier_name, COUNT(o.id) AS orders_count
        FROM couriers c
        LEFT JOIN orders o ON c.id = o.courier_id
        GROUP BY c.id, c.name
        ORDER BY orders_count DESC;
    """).fetchall()
    conn.close()

    context = {"stats": stats}
    return render(request, "order/order_statistics.html", context)
