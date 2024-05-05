from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import Produto, Ingrediente
from pagamentos.models import Pagamento
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

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

    @method_decorator(login_required)
    def get(self, request, **kwargs):
        context = super().get_context_data(**kwargs)
        context['produtos'] = Produto.objects.all()
        context['usuario'] = request.user
        context['quantidade_carrinho'] = self.obter_quantidade_carrinho(request)
        return render(request, self.template_name, context)

    def obter_quantidade_carrinho(self, request):
        carrinho = request.session.get('carrinho', {})
        quantidade_total = sum(item['quantidade'] for item in carrinho.values())
        return quantidade_total


def adicionar_ao_carrinho(request, produto_id):
    produto = Produto.objects.get(pk=produto_id)
    quantidade = int(request.POST.get('quantidade', 0))
    if quantidade >= 1:
        carrinho = request.session.get('carrinho', {})
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

    return redirect('cardapio')


def limpar_carrinho(request):
    if 'carrinho' in request.session:
        del request.session['carrinho']
        request.session.save()
    return redirect('cardapio')


def pagina_carrinho(request):
    carrinho = request.session.get('carrinho', {})
    total = sum(item.get('preco_total', 0) for item in carrinho.values())
    quantidade_total = sum(item.get('quantidade', 0) for item in carrinho.values())
    total = round(total, 2)
    
    # Obtendo os produtos do carrinho com suas fotos
    produtos_com_fotos = []
    for produto_id, item in carrinho.items():
        produto = Produto.objects.get(pk=produto_id)
        produto_com_foto = {
            'produto': produto,
            'preco': item['preco'],
            'quantidade': item['quantidade'],
            'preco_total': item['preco_total'],
            'fotos': produto.fotos.all()  # Obtém todas as fotos do produto
        }
        produtos_com_fotos.append(produto_com_foto)
    
    context = {
        'carrinho': produtos_com_fotos,  # Agora passamos os produtos com suas fotos
        'total': total,
        'usuario': request.user,
        'quantidade_carrinho': quantidade_total
    }
    
    return render(request, 'app_cardapio/cart.html', context)


def remover_do_carrinho(request, produto_id):
    carrinho = request.session.get('carrinho', {})
    if str(produto_id) in carrinho:
        del carrinho[str(produto_id)]
        request.session['carrinho'] = carrinho
        request.session.save()
    return redirect('pagina_carrinho')


