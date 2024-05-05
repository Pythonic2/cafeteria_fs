from django.db import models
from django.core.validators import MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

User = get_user_model()

class Carrinho(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Carrinho de {self.usuario.username}"

class ItemCarrinho(models.Model):
    carrinho = models.ForeignKey(Carrinho, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey('Produto', on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    def preco_total(self):
        return self.preco_unitario * self.quantidade

    def __str__(self):
        return f"Item do carrinho de {self.carrinho.usuario.username}: {self.produto.nome}"
    
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
    quantidade_em_estoque = models.FloatField(validators=[MinValueValidator(0)], blank=True)

    def __str__(self):
        return self.nome


class FotoProduto(models.Model):
    produto = models.ForeignKey(Produto, related_name='fotos', on_delete=models.CASCADE)
    imagem = models.FileField()
    principal = models.BooleanField(default=False)

    def __str__(self):
        return f'Foto de {self.produto.nome}'



@receiver(post_save, sender=Produto)
@receiver(post_save, sender=Ingrediente)
def verificar_quantidade_estoque(sender, instance, **kwargs):
    if instance.quantidade_em_estoque < 10:
        print(f"A quantidade de {instance.nome} está abaixo de 10!")