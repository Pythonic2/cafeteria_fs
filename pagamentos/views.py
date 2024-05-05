from django.shortcuts import redirect
from .models import Pagamento
from produtos.models import Produto

def processar_pagamento(request):
    carrinho = request.session.get('carrinho', {})
    valor_total = sum(item['preco_total'] for item in carrinho.values())

    # Verificar se há estoque suficiente para cada produto no carrinho
    for produto_id, item in carrinho.items():
        produto = Produto.objects.get(pk=produto_id)
        if produto.quantidade_em_estoque < item['quantidade']:
            # Se não houver estoque suficiente, redirecione de volta para o carrinho com uma mensagem de erro
            return redirect('pagina_carrinho')  # ou render com uma mensagem de erro

        # Atualizar o estoque do produto
        produto.quantidade_em_estoque -= item['quantidade']
        produto.save()

        # Subtrair a quantidade de ingredientes usados em cada produto do estoque de ingredientes
        for ingrediente in produto.ingredientes.all():
            ingrediente.quantidade_em_estoque -= item['quantidade']
            ingrediente.save()

    # Criar uma instância do model Pagamento para registrar o pagamento
    forma_pagamento = request.POST.get('forma_pagamento')  # Supondo que isso venha do formulário de pagamento
    pagamento = Pagamento.objects.create(total=valor_total, forma_pagamento=forma_pagamento)

    # Limpar o carrinho após o pagamento ser concluído
    request.session.pop('carrinho', None)

    # Redirecionar para a página do carrinho com uma mensagem de sucesso
    return redirect('pagina_carrinho')  # ou render com uma mensagem de sucesso
