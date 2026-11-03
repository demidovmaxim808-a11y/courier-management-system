"""View-функции приложения courier (Django ORM)."""

from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from courier.models import Courier


def couriers_list(request):
    """Страница /couriers/: список курьеров."""
    couriers = Courier.objects.all().order_by("name")
    context = {"couriers": couriers}
    return render(request, "courier/courier_list.html", context)


def courier_detail(request, courier_id):
    """Страница /couriers/<int:courier_id>/."""
    courier = get_object_or_404(Courier, pk=courier_id)
    context = {"courier": courier}
    return render(request, "courier/courier_detail.html", context)


def courier_search(request):
    """Страница поиска курьеров (по имени или зоне)."""
    query = request.GET.get("q", "").strip()
    couriers = Courier.objects.none()

    if query:
        couriers = Courier.objects.filter(
            Q(name__icontains=query) | Q(zone__icontains=query)
        ).order_by("name")

    context = {
        "couriers": couriers,
        "query": query,
    }
    return render(request, "courier/courier_search.html", context)
