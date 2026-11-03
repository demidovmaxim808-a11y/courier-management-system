"""Модель пользователя (диспетчера)."""

from django.db import models


class User(models.Model):
    """Пользователь системы."""

    name = models.CharField(
        max_length=200,
        verbose_name="Имя пользователя",
    )
    email = models.EmailField(
        verbose_name="Электронная почта",
    )
    role = models.CharField(
        max_length=50,
        default="диспетчер",
        verbose_name="Роль",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["name"]