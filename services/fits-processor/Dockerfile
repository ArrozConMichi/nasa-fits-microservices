FROM python:3.12-slim

WORKDIR /app

# Instalar dependencias del sistema para gráficos
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libagg-dev \
    libfreetype6-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el código y los protos generados (los vamos a copiar a mano a esta carpeta como hicimos con metadata)
COPY . .
#usamos otro puerto para no chocar con los metadatos
EXPOSE 50052 

CMD ["python", "main.py"]