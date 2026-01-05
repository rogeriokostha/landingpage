from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from .models import Rastreamento
from ipware import get_client_ip  # Biblioteca que pega o IP real mesmo no Docker
import requests  # Para consultar a API de localização (GeoIP)


def obter_localizacao(ip):
    """
    Função auxiliar que consulta onde o IP está (Cidade/Estado).
    Usa uma API pública gratuita para começar.
    """
    try:
        if ip and ip != "127.0.0.1":  # Só consulta se for IP real
            response = requests.get(f"http://ip-api.com/json/{ip}")
            data = response.json()
            if data["status"] == "success":
                return data["city"], data["regionName"]
    except:
        pass
    return None, None


def home(request):
    # Lógica de salvar a visita (IP) continua aqui...
    ip, is_routable = get_client_ip(request)

    # Se for apenas uma visita (GET), salvamos o rastro (código que já existia...)
    if request.method == "GET" and ip:
        cidade, estado = obter_localizacao(ip)
        # Verificamos se já não salvou visita recente para não duplicar (opcional)
        # Rastreamento.objects.create(...) <--- Mantenha seu código de visita aqui

    # NOVA LÓGICA: Se o usuário preencheu o formulário (POST)
    if request.method == "POST":
        nome = request.POST.get("nome")
        email = request.POST.get("email")

        # 1. Salva o Lead no Banco (marcando como EMAIL)
        cidade, estado = obter_localizacao(ip)
        Rastreamento.objects.create(
            ip=ip,
            cidade=cidade,
            estado=estado,
            dispositivo=request.META.get("HTTP_USER_AGENT", ""),
            acao="EMAIL",
            nome_lead=nome,  # Salvamos o nome
            email_lead=email,  # Salvamos o email
        )

        # 2. Envia o E-mail (Simulado no Terminal)
        assunto = f"Novo Lead Capturado: {nome}"
        mensagem = f"O cliente {nome} ({email}) acabou de se cadastrar na Landing Page."

        send_mail(
            assunto,
            mensagem,
            "sistema@seusite.com.br",  # Remetente
            ["seuemail@exemplo.com"],  # Destinatário (Você)
            fail_silently=False,
        )

        # Retorna para a mesma página com uma mensagem de sucesso (contexto)
        return render(request, "index.html", {"sucesso": True})

    return render(request, "index.html")


def redirect_whatsapp(request):
    """
    Rota Oculta.
    O botão do site aponta pra cá, a gente grava o clique e joga pro Zap.
    """
    ip, is_routable = get_client_ip(request)

    # Grava que clicou no WhatsApp
    if ip:
        cidade, estado = obter_localizacao(ip)
        Rastreamento.objects.create(
            ip=ip,
            cidade=cidade,
            estado=estado,
            dispositivo=request.META.get("HTTP_USER_AGENT", ""),
            acao="WHATSAPP",
        )

    # Seu número (depois colocamos no .env para ficar dinâmico)
    numero_whatsapp = "5517997747442"
    mensagem = "Olá, vi sua Landing Page e gostaria de saber mais."

    link_zap = f"https://api.whatsapp.com/send?phone={numero_whatsapp}&text={mensagem}"

    return redirect(link_zap)


from django.http import HttpResponse


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /admin/",  # Não deixa o Google indexar seu painel admin
        "Allow: /",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
