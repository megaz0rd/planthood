from django import forms
from django.contrib.auth.forms import UserChangeForm

from members.models import UserProfile


class UserEditForm(UserChangeForm):
    first_name = forms.CharField(max_length=64)
    last_name = forms.CharField(max_length=64)
    email = forms.EmailField()
    street = forms.CharField(max_length=64)
    building_number = forms.CharField(max_length=8)

    class Meta:
        model = UserProfile
        fields = [
            'first_name',
            'last_name',
            'email',
            'street',
            'building_number',
            'password'
        ]
