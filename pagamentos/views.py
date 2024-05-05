from produtos.models import Produto
from .models import Pagamento
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from pagamentos.models import Pagamento
from django.contrib import messages
from produtos.views import limpar_carrinho

def processar_pagamento(request):
    carrinho = request.session.get('carrinho', {})
    valor_total = sum(item.get('preco_total', 0) for item in carrinho.values())
    forma_pagamento = request.POST.get('forma_pagamento')
    
    produtos = []
    quantidade_vendida_total = 0
    for produto_id, item in carrinho.items():
        produto = Produto.objects.get(pk=produto_id)
        quantidade_vendida = item['quantidade']
        quantidade_vendida_total += quantidade_vendida
        produto.quantidade_em_estoque -= quantidade_vendida
        produto.save()
        produtos.append(produto)
    
    pagamento = Pagamento.objects.create(
        total=valor_total,
        forma_pagamento=forma_pagamento,
        quantidade=quantidade_vendida_total,
        usuario=request.user
    )
    pagamento.produtos.set(produtos)
    
    
    messages.success(request, "Pagamento realizado com sucesso!")
    limpar_carrinho(request)

    return redirect('cardapio')
