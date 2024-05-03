from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import TemplateView
from produtos.models import FotoProduto,Ingrediente,Produto

def htmx_produtos(request):
    produtos = Produto.objects.all().order_by('-id')
    imagens = FotoProduto.objects.all()
    context = {'produtos': produtos}
    context['fotos'] = imagens
    return render(request, 'app_gerenciamento/produtos/lista_produtos.html', context)


class GerenciamentoView(TemplateView):
    
    template_name = 'app_gerenciamento/admin.html'

    def get(self, request, *args, **kwargs):
        
        return render(request, self.template_name)