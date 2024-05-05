from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission


class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    telefone = PhoneNumberField()
    end = models.CharField(max_length=200)



class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    telefone = PhoneNumberField(blank=True)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # Verifica se o usuário é novo
            self.is_superuser = True  # Define o novo usuário como superusuário
        
        super().save(*args, **kwargs)
