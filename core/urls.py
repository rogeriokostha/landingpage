from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("zap/", views.redirect_whatsapp, name="whatsapp_track"),
    path("robots.txt", views.robots_txt, name="robots_txt"),
    # Galeria de Exemplos
    path("exemplos/", views.lista_exemplos, name="lista_exemplos"),
    # Rota da Página de Exemplo de Medicina
    path("exemplos/medicina/", views.exemplo_medicina, name="medicina"),
]
