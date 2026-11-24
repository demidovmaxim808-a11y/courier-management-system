"""View-функции приложения order (Django ORM)."""

from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages

from courier.models import Courier
from order.models import Order
from order.forms import OrderForm  # <-- ДОБАВЛЕНО


def orders_list(request):
    """Страница /orders/: список заказов с фильтрами и сортировкой."""
    queryset = Order.objects.select_related("courier", "user")

    status = request.GET.get("status", "").strip()
    if status:
        queryset = queryset.filter(status=status)

    search = request.GET.get("search", "").strip()
    if search:
        queryset = queryset.filter(
            Q(number__icontains=search) | Q(address__icontains=search)
        )

    courier_id = request.GET.get("courier", "").strip()
    if courier_id.isdigit():
        queryset = queryset.filter(courier_id=int(courier_id))

    sort = request.GET.get("sort", "date")
    sort_fields = {
        "date": "-date",
        "weight": "-weight",
        "cost": "-cost",
    }
    sort_field = sort_fields.get(sort, "-date")
    queryset = queryset.order_by(sort_field, "id")

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
    stats = Courier.objects.annotate(
        total_orders=Count("orders"),
        active_orders=Count(
            "orders",
            filter=Q(orders__status="в пути")
        ),
    ).order_by("-total_orders")

    context = {"stats": stats}
    return render(request, "order/order_statistics.html", context)


# НОВОЕ: Создание заказа
def order_create(request):
    """Создание нового заказа."""
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Заказ успешно создан!")
            return redirect('order:orders')
    else:
        form = OrderForm()
    
    return render(request, 'order/order_form.html', {'form': form, 'title': 'Создать заказ'})


# НОВОЕ: Редактирование заказа
def order_edit(request, order_id):
    """Редактирование заказа."""
    order = get_object_or_404(Order, pk=order_id)
    
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, "Заказ успешно обновлен!")
            return redirect('order:order_detail', order_id=order.id)
    else:
        form = OrderForm(instance=order)
    
    return render(request, 'order/order_form.html', {'form': form, 'title': 'Редактировать заказ'})


# НОВОЕ: Удаление заказа
def order_delete(request, order_id):
    """Удаление заказа (через POST)."""
    order = get_object_or_404(Order, pk=order_id)
    if request.method == 'POST':
        order.delete()
        messages.success(request, "Заказ удален.")
        return redirect('order:orders')
    
    return render(request, 'order/order_confirm_delete.html', {'order': order})