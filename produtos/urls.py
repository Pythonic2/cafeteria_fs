from django.urls import path
from .views import CardapioView, adicionar_ao_carrinho, pagina_carrinho, remover_do_carrinho, limpar_carrinho
from pagamentos.views import processar_pagamento

urlpatterns = [
    path('cardapio/', CardapioView.as_view(), name='cardapio'),
    path('adicionar/<int:produto_id>/', adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('carrinho/', pagina_carrinho, name='pagina_carrinho'),
    path('remover/<int:produto_id>/', remover_do_carrinho, name='remover_do_carrinho'),
    path('limpar-carrinho/', limpar_carrinho, name='limpar-carrinho'),
    path('processar-pagamento/', processar_pagamento, name='processar_pagamento'),
]
