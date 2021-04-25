from django.urls import path

from . import views

app_name = 'plantswap'

urlpatterns = [
    path('plants/', views.PlantListView.as_view(), name='plant-list'),
    path('plants/detail/<int:pk>/', views.PlantDetailView.as_view(),
         name='plant-detail'),
    path('plants/edit/<int:pk>/', views.PlantUpdateView.as_view(),
         name='plant-edit'),
    path('plants/new/', views.PlantCreateView.as_view(), name='plant-add'),
    path('transactions/', views.TransactionListView.as_view(),
         name='transaction-list'),
    path('transactions/detail/<int:pk>/', views.TransactionDetailView.as_view(),
         name='transaction-detail'),
    path('transactions/message/<int:pk>/', views.MessageSendView.as_view(),
         name='message'),
    path('reminders/', views.ReminderListView.as_view(),
         name='reminder-list'),
    path('reminders/new/', views.ReminderCreateView.as_view(),
         name='reminder-add'),
    path('reminders/edit/<int:pk>/', views.ReminderUpdateView.as_view(),
         name='reminder-edit'),
    path('add-to-transaction/<int:pk>/', views.add_to_transaction,
         name='add-to-transaction'),
]
