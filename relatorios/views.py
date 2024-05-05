from django.shortcuts import render
from pagamentos.models import Pagamento
from .tables import PagamentoTable

def relatorio_pagamentos(request):
    queryset = Pagamento.objects.prefetch_related('produtos').all()
    table = PagamentoTable(queryset)
    return render(request, 'relatorios/relatorio_pagamentos.html', {'table': table})
