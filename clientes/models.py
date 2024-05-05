from phonenumber_field.modelfields import PhoneNumberField
from django.db import models


class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    telefone = PhoneNumberField()
    end = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.nome
