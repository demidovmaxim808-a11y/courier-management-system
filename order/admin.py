from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Настройка отображения заказов в админке."""
    list_display = (
        'id', 'number', 'address', 'recipient',
        'courier', 'status', 'weight', 'cost', 'date'
    )
    list_display_links = ('id', 'number')
    list_filter = ('status', 'date', 'courier', 'user')
    search_fields = ('number', 'address', 'recipient', 'phone')
    ordering = ('-date', 'id')
    list_select_related = ('courier', 'user')
    date_hierarchy = 'date'