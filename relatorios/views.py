from django.shortcuts import render
from pagamentos.models import Pagamento
from .tables import PagamentoTable,IngredienteTable
from pagamentos.models import Pagamento
from produtos.models import Ingrediente



def relatorio_pagamentos(request):
    queryset = Pagamento.objects.prefetch_related('produtos').all()
    table = PagamentoTable(queryset)
    return render(request, 'relatorios/relatorio_pagamentos.html', {'table': table})

def relatorio_ingredientes(request):
    queryset = Ingrediente.objects.all()
    table = IngredienteTable(queryset)
    return render(request, 'relatorios/relatorio_pagamentos.html', {'table': table})