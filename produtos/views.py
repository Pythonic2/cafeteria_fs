from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import Produto,Ingrediente
from pagamentos.models import Pagamento
from django.contrib import messages

def monitorar_quantidade():
    produtos_acabando = Produto.objects.filter(quantidade_em_estoque__lt=10)
    ingredientes_acabando = Ingrediente.objects.filter(quantidade_em_estoque__lt=10)
    
    if produtos_acabando.exists():
        print("Produtos com quantidade abaixo de 10:")
        for produto in produtos_acabando:
            print(f"- {produto.nome}: {produto.quantidade_em_estoque}")
    
    if ingredientes_acabando.exists():
        print("\nIngredientes com quantidade abaixo de 10:")
        for ingrediente in ingredientes_acabando:
            print(f"- {ingrediente.nome}: {ingrediente.quantidade_em_estoque}")
            
class CardapioView(TemplateView):
    template_name = 'app_cardapio/shop.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['produtos'] = Produto.objects.all()
        return context


def adicionar_ao_carrinho(request, produto_id):
    produto = Produto.objects.get(pk=produto_id)
    quantidade = int(request.POST.get('quantidade', 0))
    
    if quantidade >= 1:
        carrinho = request.session.get('carrinho', {})
        print(carrinho)
        if produto_id in carrinho:
            carrinho[produto_id]['quantidade'] += quantidade
            carrinho[produto_id]['preco_total'] += quantidade * float(produto.valor)
        else:
            carrinho[produto_id] = {
                'produto': produto.nome,
                'preco': float(produto.valor),
                'quantidade': quantidade,
                'preco_total': quantidade * float(produto.valor)
            }

        request.session['carrinho'] = carrinho
    return redirect('pagina_carrinho')


def limpar_carrinho(request):
    request.session.flush() 
    return redirect('cardapio')

def pagina_carrinho(request):
    carrinho = request.session.get('carrinho', {})
    total = sum(item.get('preco_total', 0) for item in carrinho.values())
    total = round(total, 2)  
    print(carrinho)
    return render(request, 'app_cardapio/cart.html', {'carrinho': carrinho, 'total': total})

def remover_do_carrinho(request, produto_id):
    carrinho = request.session.get('carrinho', {})
    if produto_id in carrinho:
        del carrinho[produto_id]
        request.session['carrinho'] = carrinho
    return redirect('pagina_carrinho')


def processar_pagamento(request):
    carrinho = request.session.get('carrinho', {})
    valor_total = sum(item.get('preco_total', 0) for item in carrinho.values())
    forma_pagamento = request.POST.get('forma_pagamento')

    quantidade = request.POST.get('quantidade')
    print(quantidade)

    for produto_id, item in carrinho.items():
        produto = Produto.objects.get(pk=produto_id)
        quantidade_vendida = item['quantidade']  # Obter a quantidade vendida do item do carrinho
        pagamento = Pagamento.objects.create(total=valor_total, forma_pagamento=forma_pagamento,quantidade=quantidade_vendida)
        produto.quantidade_em_estoque -= quantidade_vendida
        produto.save()
        pagamento.produtos.add(produto)
    request.session.flush()

    messages.success(request, "Pagamento realizado com sucesso!")
    return redirect('cardapio')
