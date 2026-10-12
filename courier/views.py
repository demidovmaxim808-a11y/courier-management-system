"""View-функции приложения courier."""

from django.shortcuts import render

from models.couriers import find_courier_by_id
from storage import load_couriers


def couriers_list(request):
    """Страница /couriers/: список курьеров."""
    couriers_list_data = load_couriers()

    context = {
        "couriers": couriers_list_data,
    }

    return render(
        request,
        "courier/courier_list.html",
        context,
    )


def courier_detail(request, courier_id):
    """Страница /couriers/<int:courier_id>/."""
    couriers_list_data = load_couriers()
    courier = find_courier_by_id(couriers_list_data, courier_id)

    context = {
        "courier": courier,
    }

    return render(
        request,
        "courier/courier_detail.html",
        context,
        status=404 if courier is None else 200,
    )
