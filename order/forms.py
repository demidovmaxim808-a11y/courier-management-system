"""Формы для приложения order."""

from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    """Форма создания и редактирования заказа."""

    class Meta:
        model = Order
        fields = ['number', 'address', 'recipient', 'phone', 'weight', 'cost', 'status', 'courier', 'user']
        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'recipient': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'courier': forms.Select(attrs={'class': 'form-select'}),
            'user': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_weight(self):
        weight = self.cleaned_data.get('weight')
        if weight and weight <= 0:
            raise forms.ValidationError("Вес должен быть больше нуля.")
        return weight

    def clean_cost(self):
        cost = self.cleaned_data.get('cost')
        if cost and cost < 0:
            raise forms.ValidationError("Стоимость не может быть отрицательной.")
        return cost