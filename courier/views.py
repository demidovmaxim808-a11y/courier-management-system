"""View-функции приложения courier (Django ORM)."""

from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages

from courier.models import Courier
from courier.forms import CourierForm  # <-- ДОБАВЛЕНО


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


# НОВОЕ: Создание курьера
def courier_create(request):
    """Создание нового курьера."""
    if request.method == 'POST':
        form = CourierForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Курьер успешно добавлен!")
            return redirect('courier:couriers')
    else:
        form = CourierForm()
    
    return render(request, 'courier/courier_form.html', {'form': form, 'title': 'Добавить курьера'})


# НОВОЕ: Редактирование курьера
def courier_edit(request, courier_id):
    """Редактирование курьера."""
    courier = get_object_or_404(Courier, pk=courier_id)
    
    if request.method == 'POST':
        form = CourierForm(request.POST, request.FILES, instance=courier)
        if form.is_valid():
            form.save()
            messages.success(request, "Данные курьера обновлены!")
            return redirect('courier:courier_detail', courier_id=courier.id)
    else:
        form = CourierForm(instance=courier)
    
    return render(request, 'courier/courier_form.html', {'form': form, 'title': 'Редактировать курьера'})