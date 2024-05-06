from produtos.models import Produto
from .models import Pagamento
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from pagamentos.models import Pagamento
from django.contrib import messages
from produtos.views import limpar_carrinho

def subtrair_quantidade_em_estoque(produto, quantidade):
    """ verifica se há ingrediente associado ao produto para subtrair na compra"""
    produto.quantidade_em_estoque -= quantidade
    produto.save()
    for ingrediente in produto.ingredientes.all():
        ingrediente.quantidade_em_estoque -= quantidade
        ingrediente.save()

def processar_pagamento(request):
    """ 
        faz a soma dos produtos no carrinho, quantidade, e cria um objeto pagamento com os items:
        `Total` : `valor da compra`,
        `Forma de Pagamento` : `Credito,Debito,Pix, Dinheiro`,
        `Produtos` : `Todos os produtos do carrinhos q foram pagos`,
        `Quantidade` : `Soma de todos os itens`,
        `Usuario` : `Cliente Logado`,
    
    """

    carrinho = request.session.get('carrinho', {})
    valor_total = sum(item.get('preco_total', 0) for item in carrinho.values())
    forma_pagamento = request.POST.get('forma_pagamento')
    
    produtos = []
    quantidade_vendida_total = 0
    
    for produto_id, item in carrinho.items():
        produto = Produto.objects.get(pk=produto_id)
        quantidade_vendida = item['quantidade']
        if quantidade_vendida > 0: 
            quantidade_vendida_total += quantidade_vendida
            subtrair_quantidade_em_estoque(produto, quantidade_vendida)
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
