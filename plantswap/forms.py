from django import forms

from .models import Plant, Transaction


class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = [
            'name',
            'description',
            'photo',
            'amount'
        ]
        labels = {
            'name': 'Nazwa',
            'description': 'Opis',
            'photo': 'Wybierz zdjęcie',
            'amount': 'Liczba sztuk'
        }


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            'name',
            'description',
            'plant',
            'status'
        ]
        labels = {
            'name': 'Nazwa',
            'description': 'Opis',
            'plant': 'Roślina',
        }
