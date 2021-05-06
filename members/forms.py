from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.core.exceptions import ValidationError

from members.models import UserProfile, User


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=64)
    last_name = forms.CharField(max_length=64)
    street = forms.CharField(max_length=64)
    building_number = forms.CharField(max_length=8)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        ]

    def clean(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already registered.")
        return self.cleaned_data


class UserEditForm(UserChangeForm):
    first_name = forms.CharField(max_length=64)
    last_name = forms.CharField(max_length=64)
    email = forms.EmailField()
    password = None

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
        ]


class UserProfileEditForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = [
            'street',
            'building_number',
        ]
