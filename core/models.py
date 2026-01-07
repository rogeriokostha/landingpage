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


class Configuracao(models.Model):
    # --- Configurações Básicas ---
    titulo_site = models.CharField(
        "Título do Site (Browser)",
        max_length=70,
        default="Meu Site Incrível",
        help_text="Aparece na aba do navegador e no Google (Max 60-70 caracteres)",
    )
    descricao_site = models.TextField(
        "Descrição SEO",
        max_length=160,
        blank=True,
        null=True,
        help_text="Resumo que aparece no Google (Max 160 caracteres)",
    )
    url_canonica = models.URLField(
        "URL Canônica",
        blank=True,
        null=True,
        help_text="Ex: https://digitalizadordeideias.com.br (Importante para evitar conteúdo duplicado)",
    )
    autor = models.CharField(
        "Autor/Publisher",
        max_length=100,
        blank=True,
        null=True,
        help_text="Nome da empresa ou pessoa",
    )

    # --- Tags de Rastreamento ---
    facebook_pixel_id = models.CharField(
        "Facebook Pixel ID", max_length=50, blank=True, null=True
    )
    gtm_id = models.CharField(
        "Google Tag Manager ID", max_length=50, blank=True, null=True
    )

    def __str__(self):
        return "Configuração Geral do Site"

    class Meta:
        verbose_name = "Configuração Geral"
        verbose_name_plural = "Configurações Gerais"
