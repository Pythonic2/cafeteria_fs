from django.urls import path, re_path
from .views import HomeView
from django.views.defaults import *
from django.conf import settings
from django.conf.urls.static import static
from produtos.views import CardapioView
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)