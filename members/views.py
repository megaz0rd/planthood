from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import UserEditForm, UserRegistrationForm


class UserRegisterView(SuccessMessageMixin, CreateView):
    template_name = 'registration/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')

    def get_success_message(self, cleaned_data):
        return "Konto pomyślnie utworzone!"


class UserEditView(SuccessMessageMixin, UpdateView):
    template_name = 'registration/edit_profile.html'
    form_class = UserEditForm
    success_url = reverse_lazy('index')

    def get_object(self):
        return self.request.user

    def get_success_message(self, cleaned_data):
        return "Twoje konto zostało zaktualizowane!"


class UserPasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'registration/change_password.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('index')

    def get_success_message(self, cleaned_data):
        return "Twoje hasło zostało zmienione!"
