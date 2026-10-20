"""Маршруты приложения order."""

from django.urls import path

from . import views

app_name = "order"

urlpatterns = [
    path("", views.orders_list, name="orders"),
    path("<int:order_id>/", views.order_detail, name="order_detail"),
    path("statistics/", views.order_statistics, name="order_statistics"),
]
