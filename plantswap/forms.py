from django import forms

from django.utils import timezone

from .models import Plant, Transaction, Reminder


class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = [
            'name',
            'description',
            'photo',
        ]


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            'name',
            'description',
            'plant',
            'status',
            'amount'
        ]


class ReminderForm(forms.ModelForm):
    previous_care_day = forms.DateField(
        widget=forms.SelectDateWidget(),
        initial=timezone.now
    )

    class Meta:
        model = Reminder
        fields = [
            'name',
            'plant',
            'previous_care_day',
            'cycle'
        ]
