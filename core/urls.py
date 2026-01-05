from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("zap/", views.redirect_whatsapp, name="whatsapp_track"),
    path("robots.txt", views.robots_txt, name="robots_txt"),
]
