from django import forms
from django.contrib.auth.forms import (
    UserChangeForm,
    UserCreationForm,
    PasswordChangeForm
)
from django.core.exceptions import ValidationError

from members.models import UserProfile, User


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=150, label='Nazwa użytkownika')
    email = forms.EmailField(label='Adres e-mail')
    first_name = forms.CharField(max_length=64, label='Imię')
    last_name = forms.CharField(max_length=64, label='Nazwisko')
    street = forms.CharField(max_length=64, label='Ulica')
    building_number = forms.CharField(max_length=8, label='Nr budynku')
    password1 = forms.CharField(required=True, label='Nowe hasło',
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control'}),
                                error_messages={
                                    'required': 'Hasło nie może być puste'})
    password2 = forms.CharField(required=True, label='Powtórz nowe hasło',
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control'}),
                                error_messages={
                                    'required': 'Hasło nie może być puste'})

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
            raise ValidationError("Konto o podanym adresie e-mail istnieje!")
        return self.cleaned_data


class UserEditForm(UserChangeForm):
    first_name = forms.CharField(max_length=64, label='Imię')
    last_name = forms.CharField(max_length=64, label='Nazwisko')
    email = forms.EmailField(label='Adres e-mail')
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
        labels = {
            'street': 'Ulica',
            'building_number': 'Numer budynku',
        }

        widgets = {
            'street': forms.TextInput(attrs={'placeholder': ''}),
            'building_number': forms.TextInput(
                attrs={'placeholder': ''}),
        }


class UserPasswordChangeForm(PasswordChangeForm):
    error_messages = {'password_incorrect': 'Stare hasło jest niepoprawne'}
    old_password = forms.CharField(required=True, label='Stare hasło',
                                   widget=forms.PasswordInput(
                                       attrs={
                                           'class': 'form-control'
                                       }),
                                   error_messages={
                                       'required': 'Hasło nie może być puste'
                                   })
    new_password1 = forms.CharField(required=True, label='Nowe hasło',
                                    widget=forms.PasswordInput(
                                        attrs={
                                            'class': 'form-control'
                                        }),
                                    error_messages={
                                        'required': 'Hasło nie może być puste'
                                    })
    new_password2 = forms.CharField(required=True, label='Powtórz nowe hasło',
                                    widget=forms.PasswordInput(
                                        attrs={
                                            'class': 'form-control'
                                        }),
                                    error_messages={
                                        'required': 'Hasło nie może być puste'
                                    })


class Meta:
    model = User
    fields = [
        'old_password',
        'new_password1',
        'new_password2'
    ]
