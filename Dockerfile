# Imagem base do Python
FROM python:3.11-slim

# Evita arquivos temporários e logs presos
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Define diretório de trabalho
WORKDIR /app

# Instala dependências do sistema (necessárias para o PostgreSQL)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instala as dependências do Python
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copia o resto do código
COPY . /app/

# Expõe a porta
EXPOSE 8000