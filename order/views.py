"""View-функции приложения order."""

from django.http import HttpResponse

from homepage.views import page
from models.orders import find_order_by_id
from storage import load_couriers, load_orders, load_users


def orders_list(request):
    """Страница /orders/: список заказов."""
    couriers = load_couriers()
    users = load_users()
    orders = load_orders(couriers, users)

    items = ""
    for order in orders:
        courier_name = "не назначен"
        if order.courier is not None:
            courier_name = order.courier.name

        if order.status == "доставлен":
            badge = "bg-success"
        elif order.status == "отменен":
            badge = "bg-secondary"
        elif order.status == "в пути":
            badge = "bg-warning"
        else:
            badge = "bg-primary"

        text = f"{order.number} - {order.address} ({courier_name})"
        items += f"""
        <li class="list-group-item d-flex justify-content-between">
            <a href="/orders/{order.id}/">{text}</a>
            <span class="badge {badge}">{order.status}</span>
        </li>
        """
    content = f"""
    <h1>Заказы</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Заказы", content))


def order_detail(request, order_id):
    """Страница /orders/<int:order_id>/."""
    couriers = load_couriers()
    users = load_users()
    orders = load_orders(couriers, users)

    order = find_order_by_id(orders, order_id)

    if order is None:
        content = """
        <h1 class="text-danger">Заказ не найден</h1>
        <a href="/orders/" class="btn btn-outline-secondary">
            &larr; к списку заказов
        </a>
        """
        return HttpResponse(
            page("Заказ не найден", content),
            status=404,
        )

    if order.status == "доставлен":
        badge = "bg-success"
    elif order.status == "отменен":
        badge = "bg-secondary"
    elif order.status == "в пути":
        badge = "bg-warning"
    else:
        badge = "bg-primary"

    courier_name = "не назначен"
    if order.courier is not None:
        courier_name = order.courier.name

    user_name = "не указан"
    if order.user is not None:
        user_name = order.user.name

    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">Заказ {order.number}</h5>
            <p class="card-text"><strong>ID:</strong> {order.id}</p>
            <p class="card-text">
                <strong>Адрес:</strong> {order.address}
            </p>
            <p class="card-text">
                <strong>Получатель:</strong> {order.recipient}
            </p>
            <p class="card-text">
                <strong>Телефон:</strong> {order.phone}
            </p>
            <p class="card-text">
                <strong>Вес:</strong> {order.weight} кг
            </p>
            <p class="card-text">
                <strong>Стоимость:</strong> {order.cost} руб.
            </p>
            <p class="card-text">
                <strong>Дата:</strong> {order.date}
            </p>
            <p class="card-text">
                <strong>Курьер:</strong> {courier_name}
            </p>
            <p class="card-text">
                <strong>Пользователь:</strong> {user_name}
            </p>
            <p class="card-text">
                Статус:
                <span class="badge {badge}">{order.status}</span>
            </p>
            <a href="/orders/" class="btn btn-outline-secondary">
                &larr; к списку заказов
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(f"Заказ {order.number}", content))
