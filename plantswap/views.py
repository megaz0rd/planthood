from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from .forms import (
    PlantForm,
    TransactionForm,
    ReminderForm,
    UserRegisterForm,
)
from .models import (
    Plant,
    Transaction,
    Reminder,
)


class MainView(TemplateView):
    """Shows landing page"""

    template_name = 'index.html'


class PlantCreateView(SuccessMessageMixin, CreateView):
    """Powers a form to create a new plant"""

    model = Plant
    form_class = PlantForm
    success_url = reverse_lazy('plantswap:plant-list')

    def get_success_message(self, cleaned_data):
        return "Roślina dodana!"


class PlantDetailView(DetailView):
    """Shows users a single plant"""

    model = Plant
    pk_url_kwarg = 'pk'


class PlantListView(ListView):
    """Shows users a single plant"""

    model = Plant
    context_object_name = 'plants'
    ordering = 'id'


class PlantUpdateView(SuccessMessageMixin, UpdateView):
    """Powers a form to update an existing plant"""

    model = Plant
    pk_url_kwarg = 'pk'
    form_class = PlantForm
    success_url = reverse_lazy('plantswap:plant-list')

    def get_success_message(self, cleaned_data):
        return "Roślina pomyślnie zaktualizowana!"


class TransactionCreateView(SuccessMessageMixin, CreateView):
    """Powers a form to create a new transaction"""

    model = Transaction
    form_class = TransactionForm
    success_url = reverse_lazy('plantswap:transaction-list')

    def get_success_message(self, cleaned_data):
        return "Wymiana dodana!"


class TransactionListView(ListView):
    """Shows users a list of transactions"""

    model = Transaction
    context_object_name = 'transactions'


class TransactionUpdateView(SuccessMessageMixin, UpdateView):
    """Powers a form to update an existing transaction"""

    model = Transaction
    form_class = TransactionForm
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('plantswap:transaction-list')

    def get_success_message(self, cleaned_data):
        return "Wymiana pomyślnie zaktualizowana!"


class ReminderCreateView(SuccessMessageMixin, CreateView):
    """Powers a form to create a new reminder"""

    model = Reminder
    form_class = ReminderForm
    success_url = reverse_lazy('plantswap:reminder-list')

    def get_success_message(self, cleaned_data):
        return "Przypomnienie dodane!"


class ReminderListView(ListView):
    """Shows users a list of reminders"""

    model = Reminder
    context_object_name = 'reminders'


class SignUpView(SuccessMessageMixin, CreateView):

    template_name = 'registration/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('login')

    def get_success_message(self, cleaned_data):
        return "Konto pomyślnie utworzone!"
