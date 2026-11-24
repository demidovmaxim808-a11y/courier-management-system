from django.contrib import admin
from django.utils.html import format_html  # <-- ДОБАВЛЕНО

from .models import Courier
from order.models import Order


class OrderInline(admin.TabularInline):
    """Встроенная форма для просмотра заказов курьера."""
    model = Order
    extra = 0
    fields = ('number', 'status', 'date', 'address')
    readonly_fields = ('number', 'date')
    show_change_link = True


@admin.register(Courier)
class CourierAdmin(admin.ModelAdmin):
    """Настройка отображения курьеров в админке."""
    list_display = ('id', 'name', 'phone', 'transport', 'zone', 'status', 'photo_preview')  # <-- ДОБАВЛЕНО photo_preview
    list_display_links = ('id', 'name')
    list_filter = ('status', 'zone', 'transport')
    search_fields = ('name', 'phone', 'zone')
    ordering = ('name',)
    inlines = [OrderInline]

    # НОВОЕ: Метод для отображения фото в списке
    @admin.display(description='Фото')
    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="height: 40px; border-radius: 50%;" />', obj.photo.url)
        return "Нет фото"