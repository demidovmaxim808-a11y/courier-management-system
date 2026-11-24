"""Маршруты приложения courier."""

from django.urls import path
from . import views

app_name = "courier"

urlpatterns = [
    path("", views.couriers_list, name="couriers"),
    path("search/", views.courier_search, name="courier_search"),
    path("create/", views.courier_create, name="courier_create"),         # <-- НОВОЕ
    path("<int:courier_id>/", views.courier_detail, name="courier_detail"),
    path("<int:courier_id>/edit/", views.courier_edit, name="courier_edit"),  # <-- НОВОЕ
]