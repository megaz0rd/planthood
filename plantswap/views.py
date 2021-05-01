from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView, DeleteView,
)

from .forms import (
    PlantForm,
    ReminderForm,
    MessageForm,
)
from .models import (
    Plant,
    Match,
    Transaction,
    Reminder,
    Message,
)


class MainView(ListView):
    """Shows landing page if user is not authenticated else page with the
    plants available to take, exclude those items owned by user."""

    model = Plant
    context_object_name = 'plants'
    template_name = 'index.html'
    paginate_by = 18

    def get_queryset(self):
        """If user is not authenticated shows landing page with a create
        account button."""

        if not self.request.user.is_authenticated:
            return super().get_queryset()
        else:
            search_query = self.request.GET.get('q')
            if search_query:
                """Returns query results if none returns all objects."""
                return self.model.objects.filter(
                    name__icontains=search_query
                ).filter(status__in=[1, 2]
                         ).exclude(
                    owner=self.request.user)
            else:
                return self.model.objects.filter(
                    status__in=[1, 2]
                ).exclude(owner=self.request.user)


class PlantCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Powers a form to create a new plant."""

    model = Plant
    form_class = PlantForm

    def form_valid(self, form, *args, **kwargs):
        """Fills owner field in the model's form instance."""

        form.instance.owner = self.request.user
        return super(PlantCreateView, self).form_valid(form)

    def get_success_message(self, cleaned_data):
        return "Roślina dodana!"


class PlantDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """Shows user a single plant."""

    model = Plant
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        """Add an extra key to an object context data"""

        context = super(PlantDetailView, self).get_context_data(**kwargs)
        reminders = self.get_object().reminder_set.all()
        context['reminders'] = reminders
        return context

    def test_func(self):
        """Prevent user from access to an adopted plant which user is no
        longer an owner or never was"""

        if self.get_object().status == 4:
            raise ValidationError('Nie posiadasz już tej rośliny')
        elif self.get_object().status != 3:
            return self.request.user == self.get_object().owner or \
                   self.request.user != self.get_object().owner
        else:
            return self.request.user == self.get_object().owner


class PlantListView(LoginRequiredMixin, ListView):
    """Shows user plants that user owns."""

    model = Plant
    context_object_name = 'plants'

    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user,
                                         status__in=[1, 2, 3])


class PlantUpdateView(LoginRequiredMixin, UserPassesTestMixin,
                      SuccessMessageMixin, UpdateView):
    """Powers a form to update an existing plant."""

    model = Plant
    pk_url_kwarg = 'pk'
    form_class = PlantForm

    def test_func(self):
        """Prevent user from access to edit plant which user does not own"""
        if self.get_object().status != 4:
            return self.request.user == self.get_object().owner
        else:
            raise ValidationError('Nie posiadasz już tej rośliny')

    def get_success_message(self, cleaned_data):
        return "Roślina pomyślnie zaktualizowana!"


class AddToTransactionView(View):

    def get(self, request, *args, **kwargs):
        plant = get_object_or_404(Plant, pk=self.kwargs['pk'])
        match_query = Match.objects.filter(
            user=request.user).filter(plant=plant)
        if match_query.exists():
            return redirect('plantswap:message', pk=match_query[0].pk)
        else:
            match = Match.objects.create(
                user=request.user,
                plant=plant
            )
            if plant.status == 1:
                Transaction.objects.create(from_user=plant.owner,
                                           to_user=request.user,
                                           match=match)
                return redirect('plantswap:message', pk=match.id)
            elif plant.status == 2:
                Transaction.objects.create(to_user=plant.owner,
                                           from_user=request.user,
                                           match=match)
                return redirect('plantswap:message', pk=match.id)


class MessageSendView(LoginRequiredMixin, UserPassesTestMixin,
                      SuccessMessageMixin, CreateView):
    """Powers a form to create a message"""

    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('index')

    def get_match(self):
        """Get a match that is an object of a transaction"""

        match = get_object_or_404(Match, pk=self.kwargs['pk'])
        return match

    def get_transaction(self):
        transaction = get_object_or_404(Transaction, match=self.get_match())
        return transaction

    def get_initial(self, **kwargs):
        """Initialize message form with populated fields which are hidden
        from user."""

        if self.request.user == self.get_match().plant.owner:
            initial = {
                'match': self.get_match(),
                'from_user': self.get_match().plant.owner,
                'to_user': self.get_match().user
            }
        else:
            initial = {
                'match': self.get_match(),
                'from_user': self.get_match().user,
                'to_user': self.get_match().plant.owner
            }
        return initial

    def test_func(self):
        """Prevent user from sending message to user with whom user does not
        have a particular transaction or if the transaction is finished."""

        if not self.get_transaction().finished:
            return self.request.user == self.get_match().plant.owner or \
                   self.request.user == self.get_match().user
        else:
            return False

    def form_valid(self, form):
        """Valid form message, add message object to a particular transaction,
        save form and send email."""

        message = form.save()
        self.get_transaction().message.add(message)
        form.send_email()
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return "Wiadomość została wysłana!"


class TransactionDetailView(LoginRequiredMixin, UserPassesTestMixin,
                            DetailView):
    """Shows user a single transaction."""

    model = Transaction
    pk_url_kwarg = 'pk'

    def test_func(self):
        """Prevent user from access to a transaction which user
        is not a part of"""

        return self.request.user == self.get_object().to_user or \
               self.request.user == self.get_object().from_user


class TransactionListView(LoginRequiredMixin, ListView):
    """Shows user a list of transactions which user is a part of"""

    model = Transaction
    context_object_name = 'transactions'

    def get_queryset(self):
        return self.model.objects.filter(
            Q(to_user=self.request.user) |
            Q(from_user=self.request.user)
        )


class TransactionDeleteView(LoginRequiredMixin, UserPassesTestMixin,
                            DeleteView):
    """Allows user to delete an unfinished transaction"""
    model = Transaction
    success_url = reverse_lazy('plantswap:transaction-list')

    def test_func(self):
        """Prevent user from delete a transaction which user
        is not a part of"""

        return self.request.user == self.get_object().to_user or \
               self.request.user == self.get_object().from_user


class TransactionEndView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Powers a form to finish an existing transaction."""

    model = Transaction
    pk_url_kwarg = 'pk'
    fields = ['finished']
    success_url = reverse_lazy('plantswap:transaction-list')

    def form_valid(self, form):
        """If transaction ends change, change plant owner"""
        form.save(commit=False)
        plant = get_object_or_404(Plant, pk=self.get_object().match.plant.pk)
        if plant.status == 1:
            Plant.objects.create(name=plant.name,
                                 owner=self.get_object().to_user,
                                 photo=plant.photo,
                                 status=3)
        elif plant.status == 2:
            Plant.objects.create(name=plant.name,
                                 owner=self.get_object().from_user,
                                 photo=plant.photo,
                                 status=3)
        plant.status = 4
        form.save()
        self.get_object().match.delete()
        plant.save()
        return super(TransactionEndView, self).form_valid(form)

    def test_func(self):
        """Prevent user from end a transaction which user is not a part
        of"""

        return self.request.user == self.get_object().match.plant.owner or \
               self.request.user == self.get_object().match.user


class ReminderCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Powers a form to create a new reminder"""

    model = Reminder
    form_class = ReminderForm
    success_url = reverse_lazy('plantswap:reminder-list')

    def get_form_kwargs(self):
        """Passes the request object to the form class. This is necessary to
        only display in select field plants that belong to a given user."""

        kwargs = super(ReminderCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_success_message(self, cleaned_data):
        return "Przypomnienie dodane!"


class ReminderListView(LoginRequiredMixin, ListView):
    """Shows user a list of reminders which user created."""

    model = Reminder
    context_object_name = 'reminders'

    def get_queryset(self):
        return self.model.objects.filter(creator=self.request.user)


class ReminderUpdateView(LoginRequiredMixin, UserPassesTestMixin,
                         SuccessMessageMixin, UpdateView):
    """Powers a form to update an existing reminder."""

    model = Reminder
    form_class = ReminderForm
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('plantswap:reminder-list')

    def test_func(self):
        """Prevent user from access to edit a reminder which user did not
        create"""

        return self.request.user == self.get_object().creator

    def get_form_kwargs(self):
        """Passes the request object to the form class. This is necessary to
        only display in select field plants that belong to a given user."""

        kwargs = super(ReminderUpdateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_success_message(self, cleaned_data):
        return "Przypomnienie pomyślnie zaktualizowane!"
