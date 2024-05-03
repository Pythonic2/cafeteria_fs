from django.db import models
from django.core.validators import MinValueValidator

class Ingrediente(models.Model):
    nome = models.CharField(max_length=70)
    quantidade_em_estoque = models.FloatField(validators=[MinValueValidator(0)])

    def __str__(self):
        return self.nome

class Produto(models.Model):
    nome = models.CharField(max_length=60)
    descricao = models.TextField(max_length=200)
    ingredientes = models.ManyToManyField(Ingrediente, blank=True)
    informacoes_nutricionais = models.TextField(max_length=150)
    valor = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    quantidade_em_estoque = models.FloatField(validators=[MinValueValidator(0)])

    def __str__(self):
        return self.nome

class FotoProduto(models.Model):
    produto = models.ForeignKey(Produto, related_name='fotos', on_delete=models.CASCADE)
    imagem = models.FileField()
    principal = models.BooleanField(default=False)

    def __str__(self):
        return f'Foto de {self.produto.nome}'



