from .models import Configuracao


def site_config(request):
    # Pega a primeira configuração que encontrar, ou retorna vazio
    config = Configuracao.objects.first()
    return {"site_config": config}
