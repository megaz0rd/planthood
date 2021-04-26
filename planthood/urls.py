from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from plantswap import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('members.urls')),
    path('api/', include('plantswap_api.urls')),
    path('', include('plantswap.urls')),
    path('', views.MainView.as_view(), name='index'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
