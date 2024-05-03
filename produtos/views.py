from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import TemplateView
from .models import Produto,FotoProduto,Ingrediente
# Create your views here.

class CardapioView(TemplateView):
    
    template_name = 'app_cardapio/shop.html'

    def get(self, request, *args, **kwargs):
        produtos = Produto.objects.all()
        
        return render(request, self.template_name)