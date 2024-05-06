import django_tables2 as tables
from pagamentos.models import Pagamento
from produtos.models import Ingrediente


class PagamentoTable(tables.Table):
    produtos = tables.Column(accessor='produtos.all', verbose_name='Produtos')

    class Meta:
        model = Pagamento
        template_name = "django_tables2/bootstrap4.html"
        attrs = {'class': 'table table-bordered', 'th': {'class': 'text-center'}, 'td': {'class': 'text-center', 'style': 'padding: 20px;'}}

    def render_produtos(self, value):
        return ', '.join([produto.nome for produto in value])
    


class IngredienteTable(tables.Table):
    id = tables.Column(verbose_name='ID')
    nome = tables.Column(verbose_name='Nome')
    quantidade_em_estoque = tables.Column(verbose_name='Quantidade em estoque')

    class Meta:
        model = Ingrediente
        template_name = "django_tables2/bootstrap4.html"
        attrs = {'class': 'table table-bordered', 'th': {'class': 'text-center'}, 'td': {'class': 'text-center', 'style': 'padding: 20px;'}}