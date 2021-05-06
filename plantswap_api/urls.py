from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import (
    PlantViewSet,
    ReminderViewSet,
    TransactionViewSet,
    StatsView, UserViewSet
)

router = SimpleRouter()

router.register("plants", PlantViewSet,
                basename='plants')
router.register("transactions", TransactionViewSet,
                basename='transactions'),
router.register("reminders", ReminderViewSet,
                basename='reminders'),
router.register("users", UserViewSet,
                basename='users'),

urlpatterns = router.urls
urlpatterns += [
    path('stats/', StatsView.as_view())
]
