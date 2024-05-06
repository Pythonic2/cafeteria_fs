# relatorios/urls.py
from django.urls import path
from .views import relatorio_pagamentos,relatorio_ingredientes

urlpatterns = [
    path('relatorio-pagamento/', relatorio_pagamentos, name='relatorio_pagamento'),
    path('relatorio-ingrediente/', relatorio_ingredientes, name='relatorio_ingrediente'),
]
