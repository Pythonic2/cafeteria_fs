from django.conf import settings
from django.db import models
from produtos.models import Produto
from clientes.models import User

class Pagamento(models.Model):
    FORMAS_PAGAMENTO = [
        ('cartao_credito', 'Cartão de Crédito'),
        ('cartao_debito', 'Cartão de Débito'),
        ('dinheiro', 'Dinheiro'),
        ('pix', 'PIX'),
    ]

    data_venda = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    forma_pagamento = models.CharField(max_length=100, choices=FORMAS_PAGAMENTO)
    produtos = models.ManyToManyField(Produto)
    quantidade = models.FloatField(default=1)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Venda em {self.data_venda}"
