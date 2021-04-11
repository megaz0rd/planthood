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
    TransactionForm, ReminderForm,
)
from .models import (
    Plant,
    Transaction, Reminder,
)


class MainView(TemplateView):
    template_name = 'index.html'


class PlantCreateView(CreateView):
    model = Plant
    form_class = PlantForm
    success_url = reverse_lazy('plant-list')


class PlantDetailView(DetailView):
    model = Plant
    pk_url_kwarg = 'pk'


class PlantListView(ListView):
    model = Plant
    context_object_name = 'plants'


class PlantUpdateView(UpdateView):
    model = Plant
    pk_url_kwarg = 'pk'
    form_class = PlantForm
    success_url = reverse_lazy('plant-list')


class TransactionCreateView(CreateView):
    model = Transaction
    form_class = TransactionForm
    success_url = reverse_lazy('transaction-list')


class TransactionListView(ListView):
    model = Transaction
    context_object_name = 'transactions'


class TransactionUpdateView(UpdateView):
    model = Transaction
    form_class = TransactionForm
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('transaction-list')


class ReminderCreateView(CreateView):
    model = Reminder
    form_class = ReminderForm
    success_url = reverse_lazy('reminder-list')


class ReminderListView(ListView):
    model = Reminder
    context_object_name = 'reminders'
