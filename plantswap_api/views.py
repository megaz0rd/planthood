from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView

from plantswap.models import (
    Plant,
    Match,
    Transaction
)
from plantswap.serializers import (
    PlantSerializer,
    MatchSerializer,
    TransactionSerializer
)
from plantswap_api.utils import week_earlier, this_month, today


class PlantViewSet(viewsets.ModelViewSet):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer


class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class StatsView(APIView):

    def get(self, request, *args, **kwargs):
        stats_data = {
            "transactions": {
                "total": Transaction.objects.count(),
                "finished": Transaction.objects.filter(finished=True).count(),
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
