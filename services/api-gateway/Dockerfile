FROM python:3.12-slim

WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el proyecto Django
COPY . .

# Copiar los archivos generados de Proto (necesario que los generes en tu host antes)
# Opcional: Puedes generarlos dentro del contenedor si instalas grpcio-tools en el Dockerfile
# Pero por ahora asumimos que los generas en el host y los copias o los montas con volumen.

# Exponer puerto
EXPOSE 8000

# Comando de arranque usando nuestro main.py
CMD ["python", "main.py"]