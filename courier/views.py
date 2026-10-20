"""View-функции приложения courier (работа с SQLite)."""

import sqlite3

from django.shortcuts import render

DB_PATH = "data/courier.sqlite"


def couriers_list(request):
    """Страница /couriers/: список курьеров из SQLite."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    couriers = conn.execute("""
        SELECT id, name, transport, zone, status
        FROM couriers
        ORDER BY name;
    """).fetchall()
    conn.close()

    context = {"couriers": couriers}
    return render(request, "courier/courier_list.html", context)


def courier_detail(request, courier_id):
    """Страница /couriers/<int:courier_id>/."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    courier = conn.execute("""
        SELECT * FROM couriers WHERE id = ?;
    """, (courier_id,)).fetchone()
    conn.close()

    context = {"courier": courier}
    return render(
        request,
        "courier/courier_detail.html",
        context,
        status=404 if courier is None else 200,
    )


def courier_search(request):
    """Страница поиска курьеров по зоне (параметризованный запрос)."""
    zone_query = request.GET.get("zone", "").strip()
    couriers = []

    if zone_query:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        couriers = conn.execute("""
            SELECT id, name, transport, zone, status
            FROM couriers
            WHERE zone LIKE ?
            ORDER BY name;
        """, (f"%{zone_query}%",)).fetchall()
        conn.close()

    context = {
        "couriers": couriers,
        "zone_query": zone_query,
    }
    return render(request, "courier/courier_search.html", context)
