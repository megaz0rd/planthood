from django import forms
from django.core.mail import send_mail
from django.utils import timezone

from .models import Plant, Reminder, Message, Match


class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = [
            'name',
            'description',
            'photo',
            'status'
        ]


class ReminderForm(forms.ModelForm):
    previous_care_day = forms.DateField(
        widget=forms.SelectDateWidget(),
        initial=timezone.now
    )

    def __init__(self, *args, **kwargs):
        """ Grants access to the request object so that only plants of the
        current user are given as options"""

        self.request = kwargs.pop('request')
        super(ReminderForm, self).__init__(*args, **kwargs)
        self.fields['plant'].queryset = Plant.objects.filter(
            owner=self.request.user)

    class Meta:
        model = Reminder
        fields = [
            'name',
            'plant',
            'previous_care_day',
            'cycle'
        ]


class MessageForm(forms.ModelForm):

    def send_email(self):
        send_mail(
            f'Zainteresowanie rośliną: '
            f'{self.cleaned_data["match"].plant.name}',
            f'Użytkownik {self.cleaned_data["from_user"]}'
            f' pisze: {self.cleaned_data["content"]}',
            self.cleaned_data['from_user'].email,
            [f'{self.cleaned_data["to_user"].email}'],
            fail_silently=False
        )

    class Meta:
        model = Message
        fields = [
            'match',
            'from_user',
            'to_user',
            'content',
        ]
        # widgets = {
        #     'match': forms.HiddenInput(),
        #     'from_user': forms.HiddenInput(),
        #     'to_user': forms.HiddenInput()
        # }
        labels = {'content': ''}
