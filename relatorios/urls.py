# relatorios/urls.py
from django.urls import path
from .views import relatorio_pagamentos

urlpatterns = [
    path('pagamentos/', relatorio_pagamentos, name='relatorio_pagamentos'),
]
