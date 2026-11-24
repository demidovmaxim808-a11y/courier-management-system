"""Формы для приложения order."""

from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    """Форма создания и редактирования заказа."""

    # Явно задаем варианты для поля статуса, чтобы выпадающий список работал
    status = forms.ChoiceField(
        choices=[
            ('новый', 'Новый'),
            ('в пути', 'В пути'),
            ('доставлен', 'Доставлен'),
            ('отменен', 'Отменен'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Статус"
    )

    class Meta:
        model = Order
        fields = ['number', 'address', 'recipient', 'phone', 'weight', 'cost', 'date', 'status', 'courier', 'user']
        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'recipient': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            # 'status' мы убрали отсюда, так как описали его выше через ChoiceField
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

    def clean(self):
        cleaned_data = super().clean()
        courier = cleaned_data.get('courier')
        date = cleaned_data.get('date')
        status = cleaned_data.get('status')

        if courier and date and status in ['новый', 'в пути']:
            conflicts = Order.objects.filter(
                courier=courier,
                date=date,
                status__in=['новый', 'в пути']
            )
            if self.instance and self.instance.pk:
                conflicts = conflicts.exclude(pk=self.instance.pk)

            if conflicts.exists():
                raise forms.ValidationError(
                    "У этого курьера уже есть активный заказ на эту дату. "
                    "Выберите другого курьера или измените дату."
                )
        
        return cleaned_data