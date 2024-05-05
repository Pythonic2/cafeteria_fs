from django.urls import path, re_path
from .views import *
from django.views.defaults import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('gerenciamento/', GerenciamentoView.as_view(), name='gerenciamento'),

    path('adicionar-produto/', NewProduto.as_view(), name='adicionar-produto'),
    path('lista-produtos/', ListProdutos.as_view(), name='lista-produtos'),
    path('editar-produtos/<int:pk>/', UpdateProduto.as_view(), name='editar-produtos'),
    path('detail-produtos/<int:pk>/', DetailProduto.as_view(), name='detail-produtos'),
    path('delete-produtos/<int:pk>/', DeleteProduto.as_view(), name='delete-produtos'),

    path('adicionar-fotos/', AdicionarFotos.as_view(), name='adicionar-fotos'),
    path('lista-fotos/', ListaFotos.as_view(), name='lista-fotos'),
    path('editar-fotos/<int:pk>/', alterar_status_foto, name='editar-fotos'),
    path('deletar-fotos/<int:pk>/', excluir_foto, name='deletar-fotos'),

    path('adicionar-ingredientes/', AdicionarIngredientes.as_view(), name='adicionar-ingredientes'),
    path('salvar-ingredientes/', AdicionarIngredientes.as_view(), name='salvar-ingredientes'),
    path('lista-ingredientes/', htmx_lista_ingredientes, name='lista-ingredientes'),
    path('editar-ingrediente/<int:pk>/', EditarIngrediente.as_view(), name='editar-ingrediente'),
    path('deletar-ingrediente/<int:id>/', deletar_ingrediente, name='deletar-ingrediente'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)