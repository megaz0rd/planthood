from django import forms
from django.core.mail import send_mail
from django.utils import timezone

from .constant import STATUS_CHOICE
from .models import Plant, Reminder, Message


class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = [
            'name',
            'description',
            'photo',
            'status'
        ]
        labels = {
            'name': '',
            'description': '',
            'photo': 'Dodaj zdjęcie',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Nazwa rośliny'}),
            'description': forms.Textarea(attrs={'placeholder': 'Opis rośliny'})
        }

    def __init__(self, *args, **kwargs):
        """Limits available choices option for choice field"""
        super(PlantForm, self).__init__(*args, **kwargs)
        limited_choices = [(choice[0], choice[1]) for choice in
                           STATUS_CHOICE if choice[0] == 1 or choice[0] == 2
                           or choice[0] == 3]
        self.fields['status'] = forms.ChoiceField(choices=limited_choices,
                                                  label='')


class ReminderForm(forms.ModelForm):
    previous_care_day = forms.DateField(widget=forms.SelectDateWidget(),
                                        initial=timezone.now,
                                        label='Data ostatniej pielęgnacji')

    class Meta:
        model = Reminder
        fields = [
            'name',
            'plant',
            'previous_care_day',
            'cycle',
            'creator'
        ]
        labels = {
            'name': 'Wybierz typ pielęgnacji',
            'plant': 'Wybierz roślinę',
            'cycle': 'Cykl',
        }
        widgets = {
            'creator': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        """Grants access to the request object so that only plants of the
        current user are given as options"""

        self.request = kwargs.pop('request')
        super(ReminderForm, self).__init__(*args, **kwargs)
        self.fields['plant'].queryset = Plant.objects.filter(
            owner=self.request.user, status__in=[1, 3])
        self.fields['creator'].initial = self.request.user


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = [
            'plant',
            'from_user',
            'to_user',
            'content',
        ]
        widgets = {
            'plant': forms.HiddenInput(),
            'from_user': forms.HiddenInput(),
            'to_user': forms.HiddenInput(),
            'content': forms.Textarea(attrs={'placeholder': ''})
        }
        labels = {'content': ''}

    def send_email(self):
        send_mail(
            f'Zainteresowanie rośliną: '
            f'{self.cleaned_data["plant"].name}',
            f'Użytkownik {self.cleaned_data["from_user"]}'
            f' pisze: {self.cleaned_data["content"]}',
            self.cleaned_data['from_user'].email,
            [f'{self.cleaned_data["to_user"].email}'],
            fail_silently=False
        )
