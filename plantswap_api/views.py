from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView

from plantswap.models import Plant, Transaction
from plantswap.serializers import PlantSerializer, TransactionSerializer
from plantswap_api.utils import week_earlier, this_month, today


class PlantViewSet(viewsets.ModelViewSet):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class StatsView(APIView):

    def get(self, request, *args, **kwargs):
        stats_data = {
            "transactions": {
                "total": Transaction.objects.count(),
                "sell": Transaction.objects.filter(status=1).count(),
                "exchange": Transaction.objects.filter(status=2).count(),
                "free": Transaction.objects.filter(status=3).count(),
            },
            "plants": {
                'total': Plant.objects.count(),
                'last week': Plant.objects.filter(
                    created_at__gte=week_earlier).count(),
                'this month': Plant.objects.filter(
                    created_at__gte=this_month).count(),
            },
            "generation_date": today
        }
        return Response(data=stats_data)
