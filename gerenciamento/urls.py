from django.urls import path, re_path
from .views import GerenciamentoView, htmx_produtos
from django.views.defaults import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('gerenciamento/', GerenciamentoView.as_view(), name='gerenciamento'),
    path('gerenciamento_produtos/', htmx_produtos, name='gerenciamento_produtos'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)