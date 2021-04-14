from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import UserEditForm


class UserRegisterView(SuccessMessageMixin, CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
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
