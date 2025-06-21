import flet as ft
from screens.login import login_view

def main(page: ft.Page):
    # Configuración de la página
    page.title = "App Multimodal"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    # Configuración de ventana (solo para aplicaciones de escritorio)
    try:
        page.window.width = 1000
        page.window.height = 700
        page.window.min_width = 800
        page.window.min_height = 600
        page.window.resizable = True
    except:
        # En modo web estas propiedades no están disponibles
        pass
    
    # Mostrar vista de login
    login_view(page)

if __name__ == "__main__":
    # Ejecutar la aplicación
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8000)