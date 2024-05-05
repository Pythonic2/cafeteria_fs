from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.generic import TemplateView
from produtos.models import FotoProduto,Ingrediente,Produto
from django.urls import reverse_lazy
from produtos.forms import ProdutoForm,ImageForm,IngredienteForm
from django.contrib import messages
from django.views.generic import DetailView,ListView,CreateView,UpdateView,DeleteView
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from clientes.models import Cliente
from clientes.forms import ClienteForm

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


class GerenciamentoView(TemplateView):
    template_name = 'app_gerenciamento/admin.html'
    def get(self, request, *args, **kwargs):
        monitorar_quantidade()

        return render(request, self.template_name)
    
# gerenciamento de Produto
class NewProduto(CreateView):
    model = Produto
    form_class = ProdutoForm
    template_name = 'app_gerenciamento/produtos/create_produtos.html'
    success_url = reverse_lazy('adicionar-fotos')
    
    def form_valid(self, form):
        produto = form.save(commit=False)
        produto.save()
        messages.success(self.request, 'Produto Cadastrado com Sucesso')
        return super().form_valid(form)


class ListProdutos(ListView):
    model = Produto
    template_name = 'app_gerenciamento/produtos/lista_produtos.html'
    context_object_name = 'produtos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for produto in context['produtos']:
            produto.foto_principal = FotoProduto.objects.filter(produto=produto, principal=True).first()
        return context


class UpdateProduto(UpdateView):
    model = Produto
    template_name = 'app_gerenciamento/produtos/create_produtos.html'
    fields = '__all__'
    success_url = reverse_lazy('adicionar-fotos')


class DetailProduto(DetailView):
    queryset = Produto.objects.all()
    template_name = 'app_gerenciamento/produtos/detail_produto.html'


class DeleteProduto(DeleteView):
    template_name = 'app_gerenciamento/produtos/produto_confirm_delete.html'
    queryset = Produto.objects.all()
    success_url = reverse_lazy('lista-produtos')


# gerenciamneto de ingredientes
class AdicionarIngredientes(CreateView):
    model = Ingrediente
    form_class = IngredienteForm
    template_name = "app_gerenciamento/ingredientes/create_ingredientes.html"
    success_url = reverse_lazy('adicionar-ingredientes')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ingredientes'] = Ingrediente.objects.all().order_by('-id')  # Adiciona a lista de ingredientes ao contexto
        return context
    
    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)
       

def htmx_lista_ingredientes(request):
    context = {}
    ingredientes =  Ingrediente.objects.all().order_by('-id')
    context['ingredientes'] = ingredientes
    return render(request,'app_gerenciamento/ingredientes/lista_all_ingredientes.html',context)


def deletar_ingrediente(id):
    ingrediente = Ingrediente.objects.get(id=id)
    ingrediente.delete()
    return HttpResponseRedirect(reverse('adicionar-ingredientes'))


class DetalhesIngrediente(DetailView):
    model = Ingrediente
    template_name = 'app_gerenciamento/ingredientes/detail_ingrediente.html'  # Template para editar o ingrediente
    context_object_name = 'ingrediente' 


class EditarIngrediente(UpdateView):
    model = Ingrediente
    template_name = 'app_gerenciamento/ingredientes/create_ingredientes.html'
    fields = '__all__'
    success_url = reverse_lazy('adicionar-ingredientes')


# gerenciamento de fotos
class AdicionarFotos(CreateView):
    template_name = "app_gerenciamento/produtos/adicionar_fotos.html"
    form_class = ImageForm
    model = FotoProduto
    success_url = reverse_lazy('criar_produto')

    def get_initial(self):
        initial = super().get_initial()
        ultimo_produto = Produto.objects.last()
        initial['produto'] = ultimo_produto
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mostrar'] = False 
        return context

    def form_valid(self, form):
        fotos = form.save(commit=False)
        fotos.save()
        messages.success(self.request, 'Produto cadastrado com sucesso')
        self.object = form.instance
        self.object.mostrar = True
        context = self.get_context_data()
        context['mostrar'] = True
        return self.render_to_response(context)


class ListaFotos(ListView):
    model = FotoProduto
    template_name = 'app_gerenciamento/produtos/lista_fotos_produtos.html'
    context_object_name = 'fotos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for foto in context['fotos']:
            foto.produto.foto_principal = foto
        return context


def excluir_foto(request,pk):
    foto = get_object_or_404(FotoProduto, pk=pk)
    foto.delete()
    return redirect('lista-fotos')


def alterar_status_foto(request,pk):
    foto = get_object_or_404(FotoProduto, pk=pk)
    foto.principal = not foto.principal
    foto.save()
    return redirect('lista-fotos')


# gerenciamneto clientes
class CriarCliente(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'app_gerenciamento/clientes/create_cliente.html'
    success_url = reverse_lazy('criar-cliente')


class ListaCliente(ListView):
    model = Cliente
    template_name = 'app_gerenciamento/clientes/cliente_list.html'
    queryset = Cliente.objects.all().order_by('-id')


class DetalharCliente(DetailView):
    queryset = Cliente.objects.all()
    template_name = 'app_gerenciamento/clientes/cliente_detail.html'


class DeletarCliente(DeleteView):
    queryset = Cliente.objects.all()
    template_name = 'app_gerenciamento/clientes/cliente_confirm_delete.html'
    success_url = reverse_lazy('lista-cliente')


class AtualizarCliente(UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'app_gerenciamento/clientes/create_cliente.html'
    success_url = reverse_lazy('lista-cliente')