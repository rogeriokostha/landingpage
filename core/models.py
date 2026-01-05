from django.db import models
from django.contrib.auth.models import AbstractUser


# 1. Tabela de Usuário (Login por E-mail)
class Usuario(AbstractUser):
    email = models.EmailField("Endereço de E-mail", unique=True)
    # Aqui removemos a obrigatoriedade do username antigo
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email


# 2. Tabela de Rastreamento (Oculta)
class Rastreamento(models.Model):
    ACOES = [
        ("VISITA", "Acessou a Página"),
        ("WHATSAPP", "Clicou no WhatsApp"),
        ("EMAIL", "Enviou Contato"),
    ]

    ip = models.GenericIPAddressField(null=True, blank=True)
    cidade = models.CharField(max_length=100, null=True, blank=True)
    estado = models.CharField(max_length=100, null=True, blank=True)
    dispositivo = models.TextField(null=True, blank=True)
    acao = models.CharField(max_length=20, choices=ACOES, default="VISITA")
    data_criacao = models.DateTimeField(auto_now_add=True)

    # Campos opcionais para capturar dados se o usuário preencher algo
    nome_lead = models.CharField(max_length=100, null=True, blank=True)
    email_lead = models.EmailField(null=True, blank=True)

    class Meta:
        verbose_name = "Rastro de Lead"
        verbose_name_plural = "Rastros de Leads"
        ordering = ["-data_criacao"]

    def __str__(self):
        return f"{self.acao} - {self.ip}"
