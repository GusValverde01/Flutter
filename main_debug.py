import flet as ft
from screens.login import login_view
import sys
import traceback

def main(page: ft.Page):
    try:
        print("🚀 Iniciando aplicación multimodal...")
        
        # Configuración de la página
        page.title = "App Multimodal"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        
        # Configuración de ventana con nueva sintaxis (solo si no es web)
        try:
            if hasattr(page, 'window'):
                page.window.width = 1000
                page.window.height = 700
                page.window.min_width = 800
                page.window.min_height = 600
                page.window.resizable = True
                print("✅ Configuración de ventana establecida")
        except Exception as e:
            print(f"⚠️ No se pudo configurar ventana (normal en web): {e}")
        
        print("📱 Cargando vista de login...")
        # Mostrar vista de login
        login_view(page)
        print("✅ Vista de login cargada exitosamente")
        
    except Exception as e:
        print(f"❌ Error en main: {e}")
        traceback.print_exc()
        # Mostrar error en la página
        page.add(
            ft.Column([
                ft.Text("❌ Error al cargar la aplicación", size=24, color=ft.Colors.RED),
                ft.Text(f"Detalles: {str(e)}", size=14, color=ft.Colors.GREY_700),
                ft.ElevatedButton("Recargar", on_click=lambda _: login_view(page))
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )

if __name__ == "__main__":
    try:
        print("🌐 Iniciando servidor Flet en puerto 8000...")
        print("📍 La aplicación estará disponible en: http://0.0.0.0:8000")
        print("🔗 Accede desde: http://localhost:8000")
        
        # Ejecutar la aplicación
        ft.app(
            target=main, 
            view=ft.AppView.WEB_BROWSER, 
            port=8000, 
            host="0.0.0.0"
        )
        
    except Exception as e:
        print(f"❌ Error al iniciar la aplicación: {e}")
        traceback.print_exc()
        sys.exit(1)