from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import PlantViewSet, TransactionViewSet, StatsView

router = SimpleRouter()

router.register("plants", PlantViewSet,
                basename='plants')
router.register("transactions", TransactionViewSet,
                basename='transactions')

urlpatterns = router.urls
urlpatterns += [
    path('stats/', StatsView.as_view())
]
