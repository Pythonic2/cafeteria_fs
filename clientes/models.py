from django.db import models
from phonenumber_field.modelfields import PhoneNumberField# Create your models here.

class Cliente(models.Model):
    nome = models.CharField(max_length=80)
    email = models.EmailField(blank=True)
    telefone = PhoneNumberField(blank=True)

    def __str__(self) -> str:
        return self.nome