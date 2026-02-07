from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from unfold.admin import ModelAdmin
from unfold.forms import UserChangeForm, UserCreationForm
from .models import Usuario, Rastreamento, Configuracao, Portfolio

# 1. Configura o Admin do Usuário (Versão Unfold)
@admin.register(Usuario)
class UsuarioAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = UserChangeForm


# 2. Configura o Admin do Rastreamento (O Espião)
@admin.register(Rastreamento)
class RastreamentoAdmin(ModelAdmin):
    # Colunas que vão aparecer na lista
    list_display = ("ip", "acao", "cidade", "estado", "data_criacao")

    # Filtros laterais com estilo Unfold
    list_filter = ("acao", "data_criacao", "estado")

    # Barra de pesquisa
    search_fields = ("ip", "cidade", "nome_lead")

    # Deixa os campos apenas como leitura
    readonly_fields = ("ip", "cidade", "estado", "dispositivo", "acao", "data_criacao")

    # Estilização: Remove o botão de "Adicionar"
    def has_add_permission(self, request):
        return False


# 3. Configurações da Landing Page
@admin.register(Configuracao)
class ConfiguracaoAdmin(ModelAdmin):
    # Organiza os campos em grupos (fieldsets no Unfold ficam muito elegantes)
    fieldsets = (
        (
            "Informações Básicas (SEO)",
            {
                "fields": ("titulo_site", "descricao_site", "autor", "url_canonica"),
                "classes": ["tab"], # Opcional: organiza em abas no Unfold
            },
        ),
        (
            "Rastreamento & Marketing",
            {
                "fields": ("facebook_pixel_id", "gtm_id"),
            },
        ),
    )

    # Singleton: Impede de criar mais de uma configuração
    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return True


# 4. Portfólio
@admin.register(Portfolio)
class PortfolioAdmin(ModelAdmin):
    list_display = ("titulo", "slug", "ativo")
    
    # No Unfold, campos ativos (booleano) ganham um visual de toggle/badge automático
    list_editable = ["ativo"] 
    
    prepopulated_fields = {
        "slug": ("titulo",)
    }