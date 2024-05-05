from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('', include('produtos.urls')),
    path('', include('gerenciamento.urls')),
    path('', include('clientes.urls')),
    path('', include('authencications.urls')),
    path('', include('relatorios.urls')),
]
