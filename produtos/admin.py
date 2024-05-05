from django.contrib import admin
from produtos.models import Produto, Ingrediente,FotoProduto,ItemCarrinho,Carrinho
# Register your models here.
admin.site.register([Produto,Ingrediente,FotoProduto,ItemCarrinho,Carrinho])