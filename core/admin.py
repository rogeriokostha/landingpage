from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Rastreamento, Configuracao

# 1. Configura o Admin do Usuário (já que personalizamos ele)
admin.site.register(Usuario, UserAdmin)


# 2. Configura o Admin do Rastreamento (O Espião)
@admin.register(Rastreamento)
class RastreamentoAdmin(admin.ModelAdmin):
    # Colunas que vão aparecer na lista
    list_display = ("ip", "acao", "cidade", "estado", "data_criacao")

    # Filtros laterais (para você filtrar só quem clicou no Whatsapp, por exemplo)
    list_filter = ("acao", "data_criacao", "estado")

    # Barra de pesquisa (procurar por IP ou Cidade)
    search_fields = ("ip", "cidade", "nome_lead")

    # Deixa os campos apenas como leitura (para ninguém adulterar o histórico)
    readonly_fields = ("ip", "cidade", "estado", "dispositivo", "acao", "data_criacao")

    # Remove o botão de "Adicionar" (já que os dados entram sozinhos pelo site)
    def has_add_permission(self, request):
        return False


@admin.register(Configuracao)
class ConfiguracaoAdmin(admin.ModelAdmin):
    # Organiza os campos em grupos (SEO vs Analytics)
    fieldsets = (
        (
            "Informações Básicas (SEO)",
            {
                "fields": ("titulo_site", "descricao_site", "autor", "url_canonica"),
                "description": "Estes dados aparecem no Google e na aba do navegador.",
            },
        ),
        (
            "Rastreamento & Marketing",
            {
                "fields": ("facebook_pixel_id", "gtm_id"),
                "description": "IDs para integração com Facebook Ads e Google Analytics.",
            },
        ),
    )

    # Impede de criar mais de uma configuração (Singleton)
    def has_add_permission(self, request):
        # Se já existe 1 registro, bloqueia o botão de adicionar
        if self.model.objects.exists():
            return False
        return True
