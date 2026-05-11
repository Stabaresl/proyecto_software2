# IMPORTANTE: la carpeta en el repo se llama ms_usuarios (guión bajo)
FROM python:3.13-slim

RUN apt-get update && apt-get install -y \
    gcc libpq-dev curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Dependencias primero (cache de capas)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Código fuente
COPY . .

COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

EXPOSE 8001

ENTRYPOINT ["docker-entrypoint.sh"]
