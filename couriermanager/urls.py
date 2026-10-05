"""Корневая маршрутизация проекта."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("couriers/", include("courier.urls")),
    path("orders/", include("order.urls")),
]

handler404 = "homepage.views.page_not_found"
