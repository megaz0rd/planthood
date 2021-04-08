from django.urls import path

from . import views

app_name = 'plantswap'

urlpatterns = [
    path('plants/', views.PlantListView.as_view(), name='plant-list'),
    path('plants/edit/<int:pk>/', views.PlantUpdateView.as_view(),
         name='plant-edit'),
    path('plants/new/', views.PlantCreateView.as_view(), name='plant-add'),
    path('transactions/', views.TransactionListView.as_view(),
         name='transaction-list'),
    path('transactions/edit/<int:pk>/', views.TransactionUpdateView.as_view(),
         name='transaction-edit'),
    path('transactions/new/', views.TransactionCreateView.as_view(),
         name='transaction-add'),
]
