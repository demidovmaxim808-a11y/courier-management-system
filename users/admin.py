from django.contrib import admin

from .models import User
from order.models import Order


class UserOrderInline(admin.TabularInline):
    """Встроенная форма для просмотра заказов пользователя."""
    model = Order
    extra = 0
    fields = ('number', 'status', 'date', 'courier')
    readonly_fields = ('number', 'date')
    show_change_link = True


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Настройка отображения пользователей в админке."""
    list_display = ('id', 'name', 'email', 'role')
    list_display_links = ('id', 'name')
    list_filter = ('role',)
    search_fields = ('name', 'email')
    ordering = ('name',)
    inlines = [UserOrderInline]