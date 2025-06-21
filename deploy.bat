@echo off
echo 🐳 Construyendo la aplicación multimodal...

REM Construir la imagen Docker
docker build -t multimodal-search-app .

if %errorlevel% equ 0 (
    echo ✅ Imagen construida exitosamente
    
    echo 🚀 Iniciando la aplicación...
    
    REM Ejecutar con docker-compose
    docker-compose up -d
    
    if %errorlevel% equ 0 (
        echo ✅ Aplicación iniciada exitosamente
        echo 🌐 Accede a la aplicación en: http://localhost:8000
        echo 📊 Para ver los logs: docker-compose logs -f
        echo 🛑 Para detener: docker-compose down
    ) else (
        echo ❌ Error al iniciar la aplicación
    )
) else (
    echo ❌ Error al construir la imagen Docker
)

pause