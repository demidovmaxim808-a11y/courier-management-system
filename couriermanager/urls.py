"""Корневая маршрутизация проекта."""

from django.conf import settings
from django.conf.urls.static import static  # <-- ДОБАВЛЕНО
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("couriers/", include("courier.urls")),
    path("orders/", include("order.urls")),
]

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
    # НОВОЕ: Раздача медиафайлов (фото)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "homepage.views.page_not_found"