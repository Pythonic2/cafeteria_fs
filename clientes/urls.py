from django.urls import path, re_path
from gerenciamento.views import CriarCliente,ListaCliente,DeletarCliente,AtualizarCliente
from django.views.defaults import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('criar-cliente/', CriarCliente.as_view(), name='criar-cliente'),
    path('lista-cliente/', ListaCliente.as_view(), name='lista-cliente'),
    path('delete-cliente/<int:pk>/', DeletarCliente.as_view(), name='delete-cliente'),
    path('atualiza-cliente/<int:pk>/', AtualizarCliente.as_view(), name='atualiza-cliente'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)