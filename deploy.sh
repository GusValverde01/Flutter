#!/bin/bash

# Script para construir y ejecutar la aplicación Docker

echo "🐳 Construyendo la aplicación multimodal..."

# Construir la imagen Docker
docker build -t multimodal-search-app .

if [ $? -eq 0 ]; then
    echo "✅ Imagen construida exitosamente"
    
    echo "🚀 Iniciando la aplicación..."
    
    # Ejecutar con docker-compose
    docker-compose up -d
    
    if [ $? -eq 0 ]; then
        echo "✅ Aplicación iniciada exitosamente"
        echo "🌐 Accede a la aplicación en: http://localhost:8000"
        echo "📊 Para ver los logs: docker-compose logs -f"
        echo "🛑 Para detener: docker-compose down"
    else
        echo "❌ Error al iniciar la aplicación"
    fi
else
    echo "❌ Error al construir la imagen Docker"
fi