"""Формы для приложения courier."""

from django import forms
from .models import Courier


class CourierForm(forms.ModelForm):
    """Форма создания и редактирования курьера."""

    class Meta:
        model = Courier
        fields = ['name', 'phone', 'transport', 'zone', 'status', 'photo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'transport': forms.TextInput(attrs={'class': 'form-control'}),
            'zone': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_phone(self):
        """Валидация телефона."""
        phone = self.cleaned_data.get('phone')
        if len(phone) < 5:
            raise forms.ValidationError("Номер телефона слишком короткий (минимум 5 символов).")
        return phone