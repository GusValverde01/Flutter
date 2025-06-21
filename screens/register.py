import flet as ft
import json
import os
import hashlib

def load_users():
    users_file = "users.json"
    if not os.path.exists(users_file):
        # Create empty users file if it doesn't exist
        with open(users_file, 'w') as f:
            json.dump([], f)
        return []
    
    try:
        with open(users_file, 'r') as f:
            content = f.read().strip()
            if not content:  # File is empty
                return []
            # Reset file pointer and load JSON
            with open(users_file, 'r') as f2:
                return json.load(f2)
    except (json.JSONDecodeError, FileNotFoundError):
        # If file is corrupted, create new empty file
        with open(users_file, 'w') as f:
            json.dump([], f)
        return []

def save_user(username, password):
    users = load_users()
    
    # Check if user already exists
    for user in users:
        if user['username'] == username:
            return False, "El usuario ya existe"
    
    # Hash the password for security
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    # Add new user
    new_user = {
        'username': username,
        'password': hashed_password
    }
    users.append(new_user)
    
    # Save to file
    with open("users.json", 'w') as f:
        json.dump(users, f, indent=2)
    
    return True, "Usuario registrado exitosamente"

def register_view(page: ft.Page):
    page.clean()
    
    # Title
    title = ft.Text(
        "Registro de Usuario",
        size=30,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.BLUE_900
    )
    
    # Input fields
    user_input = ft.TextField(
        label="Nombre de usuario",
        width=300,
        border_radius=10
    )
    
    pass_input = ft.TextField(
        label="Contraseña",
        password=True,
        can_reveal_password=True,
        width=300,
        border_radius=10
    )
    
    confirm_pass_input = ft.TextField(
        label="Confirmar contraseña",
        password=True,
        can_reveal_password=True,
        width=300,
        border_radius=10
    )
    
    # Message text
    message = ft.Text("", color=ft.Colors.RED)
    
    def on_register_click(e):
        # Validate inputs
        if not user_input.value or not pass_input.value or not confirm_pass_input.value:
            message.value = "Todos los campos son obligatorios"
            message.color = ft.Colors.RED
            page.update()
            return
        
        if pass_input.value != confirm_pass_input.value:
            message.value = "Las contraseñas no coinciden"
            message.color = ft.Colors.RED
            page.update()
            return
        
        if len(pass_input.value) < 6:
            message.value = "La contraseña debe tener al menos 6 caracteres"
            message.color = ft.Colors.RED
            page.update()
            return
        
        # Try to save user
        success, msg = save_user(user_input.value, pass_input.value)
        
        if success:
            message.value = msg
            message.color = ft.Colors.GREEN
            page.update()
            # Clear form
            user_input.value = ""
            pass_input.value = ""
            confirm_pass_input.value = ""
            page.update()
        else:
            message.value = msg
            message.color = ft.Colors.RED
            page.update()
    
    def on_back_click(e):
        from .login import login_view
        login_view(page)
    
    # Buttons
    register_btn = ft.ElevatedButton(
        "Registrarse",
        on_click=on_register_click,
        width=300,
        bgcolor=ft.Colors.BLUE_500,
        color=ft.Colors.WHITE
    )
    
    back_btn = ft.TextButton(
        "Volver al Login",
        on_click=on_back_click
    )
    
    # Layout
    page.add(
        ft.Column(
            [
                title,
                ft.Container(height=30),
                user_input,
                pass_input,
                confirm_pass_input,
                message,
                ft.Container(height=20),
                register_btn,
                back_btn
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        )
    )
