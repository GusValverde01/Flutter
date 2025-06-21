# 📚 App Multimodal - Sistema de Búsqueda y Favoritos

Una aplicación completa desarrollada con **Flet** que permite buscar y gestionar contenido multimedia: libros, películas, anime y videojuegos.

## 🚀 Características

- ✅ **Búsqueda multimodal**: Libros, películas, anime, videojuegos
- ✅ **Sistema de favoritos**: Guarda tu contenido preferido
- ✅ **Recomendaciones inteligentes**: Basadas en tus favoritos y búsquedas
- ✅ **APIs integradas**: Google Books, Episodate, Jikan (MyAnimeList), RAWG Games
- ✅ **Autenticación de usuarios**: Sistema de login y registro
- ✅ **Interfaz moderna**: Diseñada con Flet (Flutter para Python)

## Pruebas de Funcionamiento
### Login
![image](https://github.com/user-attachments/assets/a1cdb52e-bb7e-4414-86a3-8db003ea4234)

### Registro de Usuario
![image](https://github.com/user-attachments/assets/24957e7d-0752-401c-9f4c-da0a81513635)

### Búsqueda 
![image](https://github.com/user-attachments/assets/39ac82f1-e51e-4727-845e-90d20d361949)

### Favoritos
![image](https://github.com/user-attachments/assets/4f2b012e-acd3-436a-8c12-36d7e0d7cdf9)

### Contenido Recomendado
![image](https://github.com/user-attachments/assets/3f9a9554-8378-49fb-a5fe-e38d62d6c7af)


## 🛠️ Instalación Local

### 1. Crear entorno virtual
```bash
python -m venv venv
```

### 2. Activar el entorno virtual 
```bash
# En Windows
venv\Scripts\activate

# En macOS/Linux  
source venv/bin/activate
```

### 3. Configurar política de ejecución (solo Windows)
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

### 4. Instalar dependencias
```bash
pip install flet requests
```

### 5. Ejecutar aplicación 
```bash
python main.py
```

### 6. Accede al endpoint
```bash
http://localhost:8000
```
## 🐳 Docker

### Construir la imagen
```bash
docker build -t app-multimodal .
```

### Ejecutar el contenedor
```bash
docker run -p 8000:8000 app-multimodal
```

### Ejecutar en modo desarrollo (con volúmenes)
```bash
docker run -p 8000:8000 -v $(pwd):/app app-multimodal
```

### Docker Compose
```bash
# Iniciar
docker-compose -f docker-compose-new.yml up --build

# Detener
docker-compose -f docker-compose-new.yml down
```
### Accede al endpoint
```bash
http://localhost:8000
```

## 🔗 APIs Utilizadas

- **📚 Libros**: [Google Books API](https://developers.google.com/books)
- **🎬 Películas/Series**: [Episodate API](https://www.episodate.com/api)
- **🎌 Anime**: [Jikan API](https://jikan.moe/) (MyAnimeList)
- **🎮 Videojuegos**: Sistema local con datos populares

## 👥 Uso de la Aplicación

1. **Registro/Login**: Crea una cuenta o inicia sesión
2. **Buscar**: Selecciona tipo de contenido y busca
3. **Favoritos**: Agrega contenido a tus favoritos
4. **Recomendaciones**: Ve sugerencias personalizadas


### 🚀 Método QR (Recomendado)
```bash
# 1. Instalar dependencia para QR
pip install qrcode[pil]

# 2. Ejecutar versión móvil
python main_mobile.py

# 3. Se generará automáticamente:
#    ✅ Código QR en consola
#    ✅ URL para conexión
#    ✅ IP local detectada

# 4. En tu móvil:
#    📱 Abre la app "Flet" 
#    📷 Escanea el QR que aparece en consola
#    🎉 ¡Tu app se ejecuta en el móvil!
```
### Ejemplo de QR generado
![image](https://github.com/user-attachments/assets/03212202-b202-4671-ae86-3bd15ef7ff9b)

## 📊 Datos Persistentes

- `users.json`: Usuarios registrados
- `favorites_[usuario].json`: Favoritos por usuario
- `search_history_[usuario].json`: Historial de búsquedas

## 🎉 ¡Aplicación Dockerizada Exitosamente!

  Sigue los pasos de Docker para iniciar la aplicación. Una vez realizado:

1. **Abre tu navegador**
2. **Ve a**: http://localhost:8000
3. **Crea una cuenta** o inicia sesión
4. **¡Disfruta buscando contenido multimodal!**
