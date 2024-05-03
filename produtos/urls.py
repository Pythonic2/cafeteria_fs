from django.urls import path, re_path
from .views import CardapioView
from django.views.defaults import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('cardapio/', CardapioView.as_view(), name='cardapio'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)