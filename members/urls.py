from django.urls import path

from members import views

app_name = 'members'

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(),
         name='register'),
    path('edit_profile/', views.UserEditView.as_view(),
         name='edit-profile'),
    path('password/', views.UserPasswordChangeView.as_view(),
         name='change-password'),
    path('address/', views.UserProfileEditView.as_view(),
         name='edit-address')
]
