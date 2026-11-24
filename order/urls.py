"""Маршруты приложения order."""

from django.urls import path
from . import views

app_name = "order"

urlpatterns = [
    path("", views.orders_list, name="orders"),
    path("statistics/", views.order_statistics, name="order_statistics"),
    path("create/", views.order_create, name="order_create"),              # <-- НОВОЕ
    path("<int:order_id>/", views.order_detail, name="order_detail"),
    path("<int:order_id>/edit/", views.order_edit, name="order_edit"),     # <-- НОВОЕ
    path("<int:order_id>/delete/", views.order_delete, name="order_delete"), # <-- НОВОЕ
]