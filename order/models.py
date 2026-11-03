"""Модель заказа."""

from django.db import models

from courier.models import Courier
from users.models import User


class Order(models.Model):
    """Заказ на доставку."""

    number = models.CharField(
        max_length=50,
        verbose_name="Номер заказа",
    )
    address = models.CharField(
        max_length=300,
        verbose_name="Адрес доставки",
    )
    recipient = models.CharField(
        max_length=200,
        verbose_name="Получатель",
    )
    phone = models.CharField(
        max_length=20,
        verbose_name="Телефон получателя",
    )
    weight = models.FloatField(
        verbose_name="Вес (кг)",
    )
    cost = models.FloatField(
        verbose_name="Стоимость (руб.)",
    )
    date = models.DateField(
        verbose_name="Дата создания",
    )
    status = models.CharField(
        max_length=50,
        default="новый",
        verbose_name="Статус",
    )
    courier = models.ForeignKey(
        Courier,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
        verbose_name="Курьер",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
        verbose_name="Пользователь",
    )

    def __str__(self):
        return self.number

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["-date", "id"]