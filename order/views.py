"""View-функции приложения order (Django ORM)."""

from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render

from courier.models import Courier
from order.models import Order


def orders_list(request):
    """Страница /orders/: список заказов с фильтрами и сортировкой."""
    # Базовый запрос: сразу подгружаем связанных курьеров и юзеров
    queryset = Order.objects.select_related("courier", "user")

    # Фильтрация по статусу
    status = request.GET.get("status", "").strip()
    if status:
        queryset = queryset.filter(status=status)

    # Поиск по номеру или адресу
    search = request.GET.get("search", "").strip()
    if search:
        queryset = queryset.filter(
            Q(number__icontains=search) | Q(address__icontains=search)
        )

    # Фильтрация по курьеру (связанное поле)
    courier_id = request.GET.get("courier", "").strip()
    if courier_id.isdigit():
        queryset = queryset.filter(courier_id=int(courier_id))

    # Сортировка
    sort = request.GET.get("sort", "date")
    sort_fields = {
        "date": "-date",
        "weight": "-weight",
        "cost": "-cost",
    }
    sort_field = sort_fields.get(sort, "-date")
    queryset = queryset.order_by(sort_field, "id")

    # Пагинация
    paginator = Paginator(queryset, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "orders": page_obj,
        "page_obj": page_obj,
        "status": status,
        "search": search,
        "courier_id": courier_id,
        "sort": sort,
        "couriers": Courier.objects.all(),
    }
    return render(request, "order/order_list.html", context)


def order_detail(request, order_id):
    """Страница /orders/<int:order_id>/."""
    order = get_object_or_404(
        Order.objects.select_related("courier", "user"),
        pk=order_id,
    )
    context = {"order": order}
    return render(request, "order/order_detail.html", context)


def order_statistics(request):
    """Страница статистики заказов по курьерам."""
    # Аннотация: считаем общее кол-во заказов и кол-во заказов в пути
    stats = Courier.objects.annotate(
        total_orders=Count("orders"),
        active_orders=Count(
            "orders",
            filter=Q(orders__status="в пути")
        ),
    ).order_by("-total_orders")

    context = {"stats": stats}
    return render(request, "order/order_statistics.html", context)
