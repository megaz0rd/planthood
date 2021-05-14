from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import UserEditForm, UserRegistrationForm, UserProfileEditForm, \
    UserPasswordChangeForm
from .models import UserProfile


class UserRegisterView(SuccessMessageMixin, CreateView):
    """Powers a form to register a user and create a user profile."""

    template_name = 'registration/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form, *args, **kwargs):
        """Waits for saving user model to creates user profile. Then
        authenticates user and logs in."""

        user = form.save(commit=False)
        street = form.cleaned_data['street']
        building_number = form.cleaned_data['building_number']
        user.save()
        UserProfile.objects.create(user=user, street=street,
                                   building_number=building_number)
        username, password = form.cleaned_data.get(
            'username'), form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super(UserRegisterView, self).form_valid(form)

    def get_success_message(self, cleaned_data):
        return "Konto pomyślnie utworzone!"


class UserEditView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Powers a form to edit a user model"""

    template_name = 'registration/edit_profile.html'
    form_class = UserEditForm
    success_url = reverse_lazy('index')

    def get_object(self):
        return self.request.user

    def get_success_message(self, cleaned_data):
        return "Twoje konto zostało zaktualizowane!"


class UserPasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    """Powers a form to edit a user's password"""

    template_name = 'registration/change_password.html'
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('index')

    def get_success_message(self, cleaned_data):
        return "Twoje hasło zostało zmienione!"


class UserProfileEditView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Powers a form to edit a user profile"""

    template_name = 'registration/edit_profile.html'
    form_class = UserProfileEditForm
    success_url = reverse_lazy('index')

    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)

    def get_success_message(self, cleaned_data):
        return "Twój adres został zaktualizowany"
