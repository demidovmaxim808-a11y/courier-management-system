"""Модель курьера."""

from django.db import models


class Courier(models.Model):
    """Курьер службы доставки."""

    name = models.CharField(max_length=200, verbose_name="Имя курьера")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    transport = models.CharField(max_length=100, verbose_name="Транспорт")
    zone = models.CharField(max_length=200, verbose_name="Зона обслуживания")
    status = models.CharField(max_length=50, default="свободен", verbose_name="Статус")
    orders_done = models.PositiveIntegerField(default=0, verbose_name="Выполнено заказов")
    
    # НОВОЕ: Поле для загрузки фото
    photo = models.ImageField(
        upload_to='couriers/', 
        blank=True, 
        null=True, 
        verbose_name="Фото курьера"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Курьер"
        verbose_name_plural = "Курьеры"
        ordering = ["name"]