"""
Django settings for backend project - PRODUCTION READY
"""

from pathlib import Path
from decouple import config, Csv  # Importante: Csv serve para ler listas do .env
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================================================================
# SEGURANÇA E CONFIGURAÇÃO DE AMBIENTE
# ==============================================================================

# Nunca deixe a chave exposta no código. O Portainer vai injetar isso.
SECRET_KEY = config("SECRET_KEY", default="chave-insegura-apenas-para-teste-local")

# Em produção, isso TEM que ser False.
DEBUG = config("DEBUG", default=False, cast=bool)

# Lista de domínios permitidos (Ex: digitalizadordeideias.com.br)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="127.0.0.1,localhost", cast=Csv())

# Confiança no HTTPS do Traefik (Obrigatório para o formulário funcionar)
CSRF_TRUSTED_ORIGINS = ["https://digitalizadordeideias.com.br"]
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# ==============================================================================
# APLICAÇÃO
# ==============================================================================

INSTALLED_APPS = [
    "unfold",  # Deve vir primeiro!
    "unfold.contrib.filters",  # Opcional: filtros melhores
    "unfold.contrib.forms",
    "core",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Otimização de estáticos
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.site_config",
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"


# ==============================================================================
# BANCO DE DADOS
# ==============================================================================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOST"),
        "PORT": config("DB_PORT"),
    }
}


# ==============================================================================
# VALIDAÇÃO DE SENHA E AUTH
# ==============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

AUTH_USER_MODEL = "core.Usuario"


# ==============================================================================
# INTERNACIONALIZAÇÃO
# ==============================================================================

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True


# ==============================================================================
# ARQUIVOS ESTÁTICOS (CSS, JS, IMAGES) - WHITENOISE
# ==============================================================================

STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "core/static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Ativa compressão e cache (Site muito mais rápido)
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Configuração de Mídia (Imagens que você sobe no Admin)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# ==============================================================================
# CONFIGURAÇÃO DE E-MAIL (SMTP)
# ==============================================================================

# Se as variáveis de email não existirem no Portainer, ele usa o Console (para não quebrar)
EMAIL_BACKEND = config(
    "EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend"
)
EMAIL_HOST = config("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")


UNFOLD = {
    "SITE_TITLE": "Gerenciador Landing Page",
    "SITE_HEADER": "Admin Digitalizador",
    "SITE_SYMBOL": "rocket",  # Ícone do Heroicons
    "COLORS": {
        "primary": {
            "50": "250 245 255",
            "100": "243 232 255",
            "200": "233 213 255",
            "300": "216 180 254",
            "400": "192 132 252",
            "500": "168 85 247",  # Cor principal (roxo)
            "600": "147 51 234",
            "700": "126 34 206",
            "800": "107 33 168",
            "900": "88 28 135",
            "950": "59 7 100",
        },
    },
}