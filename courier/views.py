"""View-функции приложения courier."""

from django.http import HttpResponse

from homepage.views import page
from models.couriers import find_courier_by_id
from storage import load_couriers


def couriers_list(request):
    """Страница /couriers/: список курьеров."""
    items = ""
    for courier in load_couriers():
        text = (
            f"{courier.name} - {courier.transport}, "
            f"зона: {courier.zone}, статус: {courier.status}"
        )
        items += (
            f'<li class="list-group-item">'
            f'<a href="/couriers/{courier.id}/">{text}</a>'
            f'</li>'
        )
    content = f"""
    <h1>Курьеры</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Курьеры", content))


def courier_detail(request, courier_id):
    """Страница /couriers/<int:courier_id>/."""
    couriers = load_couriers()
    courier = find_courier_by_id(couriers, courier_id)

    if courier is None:
        content = """
        <h1 class="text-danger">Курьер не найден</h1>
        <a href="/couriers/" class="btn btn-outline-secondary">
            &larr; к списку курьеров
        </a>
        """
        return HttpResponse(
            page("Курьер не найден", content),
            status=404,
        )

    badge = "bg-success" if courier.status == "свободен" else "bg-warning"
    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{courier.name}</h5>
            <p class="card-text"><strong>ID:</strong> {courier.id}</p>
            <p class="card-text">
                <strong>Телефон:</strong> {courier.phone}
            </p>
            <p class="card-text">
                <strong>Транспорт:</strong> {courier.transport}
            </p>
            <p class="card-text">
                <strong>Зона:</strong> {courier.zone}
            </p>
            <p class="card-text">
                Статус:
                <span class="badge {badge}">{courier.status}</span>
            </p>
            <p class="card-text">
                <strong>Выполнено заказов:</strong>
                {courier.orders_done}
            </p>
            <a href="/couriers/" class="btn btn-outline-secondary">
                &larr; к списку курьеров
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(courier.name, content))
