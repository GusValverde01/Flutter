import flet as ft
import os
import sys

# Agregar el directorio actual al path para imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from screens.login import login_view

def main(page: ft.Page):
    # Configuración de la página
    page.title = "App Multimodal - Búsqueda de Contenido"
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # Configuración de ventana (solo para aplicaciones de escritorio)
    try:
        page.window.width = 1000
        page.window.height = 700
        page.window.min_width = 800
        page.window.min_height = 600
    except:
        # En modo web estas propiedades pueden no estar disponibles
        pass
    
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO
    
    # Iniciar con la vista de login
    login_view(page)

if __name__ == "__main__":
    # Ejecutar la aplicación
    print("🚀 Iniciando App Multimodal...")
    print("📱 Accede en: http://localhost:8000")
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8000, host="0.0.0.0")
