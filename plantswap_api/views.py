from django.contrib.auth.models import User, Group
from rest_framework.response import Response
from rest_framework import viewsets, permissions
from rest_framework.views import APIView

from plantswap.models import (
    Plant,
    Transaction, Reminder
)
from plantswap.serializers import (
    PlantSerializer,
    TransactionSerializer, ReminderSerializer, UserSerializer, GroupSerializer
)
from plantswap_api.utils import week_earlier, this_month, today


class PlantViewSet(viewsets.ModelViewSet):
    """ API endpoint that allows plants to be viewed or edited. """

    queryset = Plant.objects.all()
    serializer_class = PlantSerializer
    permission_classes = [permissions.IsAuthenticated]


class TransactionViewSet(viewsets.ModelViewSet):
    """ API endpoint that allows transactions to be viewed or edited. """

    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]


class ReminderViewSet(viewsets.ModelViewSet):
    """ API endpoint that allows reminders to be viewed or edited. """

    queryset = Reminder.objects.all()
    serializer_class = ReminderSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    """ API endpoint that allows users to be viewed or edited. """

    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """ API endpoint that allows groups to be viewed or edited. """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class StatsView(APIView):
    """ API endpoint that allows statistics to be viewed. """

    def get(self, request, *args, **kwargs):
        stats_data = {
            "transactions": {
                "total": Transaction.objects.count(),
                "finished": Transaction.objects.filter(
                    is_finished=True).count(),
            },
            "plants": {
                'total': Plant.objects.count(),
                'added last week': Plant.objects.filter(
                    added__gte=week_earlier).count(),
                'added this month': Plant.objects.filter(
                    added__gte=this_month).count(),
            },
            "generation_date": today
        }
        return Response(data=stats_data)
