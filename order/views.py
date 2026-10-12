"""View-функции приложения order."""

from django.shortcuts import render

from models.orders import find_order_by_id
from storage import load_couriers, load_orders, load_users


def orders_list(request):
    """Страница /orders/: список заказов."""
    couriers = load_couriers()
    users = load_users()
    orders = load_orders(couriers, users)

    context = {
        "orders": orders,
    }

    return render(
        request,
        "order/order_list.html",
        context,
    )


def order_detail(request, order_id):
    """Страница /orders/<int:order_id>/."""
    couriers = load_couriers()
    users = load_users()
    orders = load_orders(couriers, users)

    order = find_order_by_id(orders, order_id)

    context = {
        "order": order,
    }

    return render(
        request,
        "order/order_detail.html",
        context,
        status=404 if order is None else 200,
    )
