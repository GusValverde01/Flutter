import flet as ft
import os
import sys
import socket
import qrcode

# Agregar el directorio actual al path para imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from screens.login import login_view

def get_local_ip():
    """Obtener la IP local de la máquina"""
    try:
        # Conectar a una dirección externa para obtener la IP local
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "localhost"

def generate_qr_code(url):
    """Generar y mostrar código QR en consola"""
    try:
        # Crear código QR
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        # Mostrar QR en consola usando caracteres
        print("\n" + "="*60)
        print("📱 CÓDIGO QR PARA LA APP FLET MÓVIL")
        print("="*60)
        
        # Generar QR con caracteres ASCII
        qr_ascii = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=1,
            border=2,
        )
        qr_ascii.add_data(url)
        qr_ascii.make(fit=True)
        
        # Imprimir QR en consola
        qr_ascii.print_ascii(invert=True)
        
        print("="*60)
        print(f"📡 URL: {url}")
        print("📱 Escanea este QR con la app Flet en tu móvil")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"❌ Error generando QR: {e}")
        print(f"📡 URL manual: {url}")

def main(page: ft.Page):
    # Configuración optimizada para móvil
    page.title = "App Multimodal"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 10
    page.scroll = ft.ScrollMode.AUTO
    
    # Responsive design para móvil
    page.adaptive = True
    
    # Iniciar con la vista de login
    login_view(page)

if __name__ == "__main__":
    # Obtener IP local
    local_ip = get_local_ip()
    port = 8000
    url = f"http://{local_ip}:{port}"
    
    print("📱 Iniciando App Multimodal para MÓVIL...")
    print("🔍 Asegúrate de tener la app 'Flet' instalada:")
    print("   📱 Android: Google Play Store")
    print("   🍎 iOS: App Store")
    print("📲 Generando código QR...")
    
    # Generar y mostrar código QR
    generate_qr_code(url)
    
    # Ejecutar aplicación
    ft.app(target=main, view=ft.AppView.FLET_APP, port=port, host="0.0.0.0")