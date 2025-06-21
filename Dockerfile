# Usar Python 3.11 como base
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias para Flet
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos de requisitos
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Crear directorios necesarios para datos persistentes
RUN mkdir -p /app/data

# Exponer el puerto que usará Flet
EXPOSE 8000

# Variables de entorno
ENV FLET_WEB=true
ENV FLET_PORT=8000
ENV FLET_HOST=0.0.0.0

# Comando para ejecutar la aplicación
CMD ["python", "main.py", "--web", "--port", "8000", "--host", "0.0.0.0"]