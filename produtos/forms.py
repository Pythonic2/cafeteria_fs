from django import forms
from .models import Produto, FotoProduto, Ingrediente


class ImageForm(forms.ModelForm):
    class Meta:
        model = FotoProduto
        fields = '__all__'


class IngredienteForm(forms.ModelForm):
    class Meta:
        model = Ingrediente
        fields = '__all__'

class ProdutoForm(forms.ModelForm):

    class Meta:
        model = Produto
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProdutoForm, self).__init__(*args, **kwargs)
        self.fields['ingredientes'].widget.attrs.update({'class': 'form-control form-control-user', 'placeholder': 'água, limão, açucar'})
        self.fields['nome'].widget.attrs.update({'class': 'form-control form-control-user', 'placeholder': 'Nome'})
        self.fields['descricao'].widget.attrs.update({'class': 'form-control form-control-user', 'placeholder': 'Descrição'})
        self.fields['informacoes_nutricionais'].widget.attrs.update({'class': 'form-control form-control-user', 'placeholder': '0 kcal,10 carbo'})
        self.fields['valor'].widget.attrs.update({'class': 'form-control form-control-user', 'placeholder': '5'})
        self.fields['quantidade_em_estoque'].widget.attrs.update({'class': 'form-control form-control-user', 'placeholder': 'Se necessário','required':False})
