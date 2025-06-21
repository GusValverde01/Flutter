import flet as ft
import json
import hashlib
import os
import threading
from api.books_api_new import BooksAPI
from api.movies_api import MoviesAPI
from api.anime_api import AnimeAPI
from api.games_api import GamesAPI
from utils.favorites_manager import FavoritesManager
from utils.card_helpers import create_result_card

def load_users():
    users_file = "users.json"
    if not os.path.exists(users_file):
        return []
    
    try:
        with open(users_file, 'r') as f:
            content = f.read().strip()
            if not content:
                return []
            with open(users_file, 'r') as f2:
                return json.load(f2)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def authenticate_user(username, password):
    users = load_users()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    for user in users:
        if user['username'] == username and user['password'] == hashed_password:
            return True
    return False

def login_view(page: ft.Page):
    page.clean()
    
    # Title
    title = ft.Text(
        "App Multimodal",
        size=35,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.BLUE_900
    )
    
    subtitle = ft.Text(
        "Busca libros y contenido multimodal",
        size=16,
        color=ft.Colors.GREY_700
    )
    
    # Input fields
    user_input = ft.TextField(
        label="Usuario",
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
    
    # Message text
    message = ft.Text("", color=ft.Colors.RED)
    
    def on_login_click(e):
        if not user_input.value or not pass_input.value:
            message.value = "Por favor ingresa usuario y contraseña"
            page.update()
            return
        
        if authenticate_user(user_input.value, pass_input.value):
            message.value = "Login exitoso"
            message.color = ft.Colors.GREEN
            page.update()
            # Here you would navigate to the main app
            main_app_view(page, user_input.value)
        else:
            message.value = "Usuario o contraseña incorrectos"
            message.color = ft.Colors.RED
            page.update()
    
    def on_register_click(e):
        from .register import register_view
        register_view(page)
    
    # Buttons
    login_btn = ft.ElevatedButton(
        "Iniciar Sesión",
        on_click=on_login_click,
        width=300,
        bgcolor=ft.Colors.BLUE_500,
        color=ft.Colors.WHITE
    )
    
    register_btn = ft.TextButton(
        "¿No tienes cuenta? Regístrate",
        on_click=on_register_click
    )
    
    # Layout
    page.add(
        ft.Column(
            [
                title,
                subtitle,
                ft.Container(height=50),
                user_input,
                pass_input,
                message,
                ft.Container(height=20),
                login_btn,
                register_btn
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        )
    )

def main_app_view(page: ft.Page, username):
    page.clean()
    
    # Initialize APIs and favorites manager
    books_api = BooksAPI()
    movies_api = MoviesAPI()
    anime_api = AnimeAPI()
    games_api = GamesAPI()
    favorites_manager = FavoritesManager(username)
    
    # Current search type
    current_search_type = "Libros"
    
    # Welcome message
    welcome = ft.Text(
        f"¡Bienvenido, {username}!",
        size=25,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.BLUE_900
    )
    
    # Navigation tabs
    def show_search_view(e):
        search_view(page, username, favorites_manager, books_api, movies_api, anime_api, games_api)
    
    def show_favorites_view(e):
        favorites_view(page, username, favorites_manager, books_api, movies_api, anime_api, games_api)
    
    def show_recommendations_view(e):
        recommendations_view(page, username, favorites_manager, books_api, movies_api, anime_api, games_api)
    
    # Navigation buttons
    nav_buttons = ft.Row([
        ft.ElevatedButton(
            "🔍 Buscar",
            on_click=show_search_view,
            bgcolor=ft.Colors.BLUE_500,
            color=ft.Colors.WHITE
        ),
        ft.ElevatedButton(
            "❤️ Favoritos",
            on_click=show_favorites_view,
            bgcolor=ft.Colors.RED_500,
            color=ft.Colors.WHITE
        ),
        ft.ElevatedButton(
            "🎯 Recomendaciones",
            on_click=show_recommendations_view,
            bgcolor=ft.Colors.PURPLE_500,
            color=ft.Colors.WHITE
        ),
    ], alignment=ft.MainAxisAlignment.CENTER, spacing=10)
    
    def on_logout_click(e):
        login_view(page)
    
    logout_btn = ft.TextButton(
        "Cerrar Sesión",
        on_click=on_logout_click
    )
    
    # Default to search view
    page.add(
        ft.Column([
            welcome,
            ft.Container(height=20),
            nav_buttons,
            ft.Container(height=20),
            logout_btn
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )
    
    # Show search view by default
    show_search_view(None)

def search_view(page: ft.Page, username: str, favorites_manager, books_api, movies_api, anime_api, games_api):
    """Search view with favorites functionality"""
    page.clean()
    
    # Current search type
    current_search_type = "Libros"
    
    # Welcome message
    welcome = ft.Text(
        f"¡Bienvenido, {username}!",
        size=25,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.BLUE_900
    )
    
    # Navigation buttons
    def show_search_view(e):
        search_view(page, username, favorites_manager, books_api, movies_api, anime_api, games_api)
    
    def show_favorites_view(e):
        favorites_view(page, username, favorites_manager, books_api, movies_api, anime_api, games_api)
    
    def show_recommendations_view(e):
        recommendations_view(page, username, favorites_manager, books_api, movies_api, anime_api, games_api)
    
    nav_buttons = ft.Row([
        ft.ElevatedButton(
            "🔍 Buscar",
            on_click=show_search_view,
            bgcolor=ft.Colors.BLUE_700,
            color=ft.Colors.WHITE
        ),
        ft.ElevatedButton(
            "❤️ Favoritos",
            on_click=show_favorites_view,
            bgcolor=ft.Colors.RED_500,
            color=ft.Colors.WHITE
        ),
        ft.ElevatedButton(
            "🎯 Recomendaciones",
            on_click=show_recommendations_view,
            bgcolor=ft.Colors.PURPLE_500,
            color=ft.Colors.WHITE
        ),
    ], alignment=ft.MainAxisAlignment.CENTER, spacing=10)
    
    # Content type selector
    content_type_dropdown = ft.Dropdown(
        label="Tipo de contenido",
        width=300,
        options=[
            ft.dropdown.Option("Libros"),
            ft.dropdown.Option("Películas"),
            ft.dropdown.Option("Anime"),
            ft.dropdown.Option("Videojuegos"),
        ],
        value="Libros"
    )
    
    # Search field
    search_input = ft.TextField(
        label="Buscar contenido...",
        width=300,
        border_radius=10
    )
    
    # Loading indicator
    loading = ft.ProgressRing(visible=False)
    
    # Search results container
    results_container = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, height=350)
    
    # Status message
    status_message = ft.Text("", size=14, color=ft.Colors.GREY_600)
    
    def update_search_placeholder(e):
        nonlocal current_search_type
        current_search_type = content_type_dropdown.value
        placeholders = {
            "Libros": "Buscar libros por título, autor o tema...",
            "Películas": "Buscar películas por título...",
            "Anime": "Buscar anime por título...",
            "Videojuegos": "Buscar videojuegos por nombre..."
        }
        search_input.label = placeholders.get(current_search_type, "Buscar contenido...")
        page.update()
    
    content_type_dropdown.on_change = update_search_placeholder
    
    def search_content_async(query, content_type):
        """Perform content search in background thread"""
        try:
            results = []
            
            if content_type == "Libros":
                results = books_api.search_books(query, max_results=15)
            elif content_type == "Películas":
                results = movies_api.search_movies(query, max_results=15)
            elif content_type == "Anime":
                results = anime_api.search_anime(query, max_results=15)
            elif content_type == "Videojuegos":
                results = games_api.search_games(query, max_results=15)
            
            # Add search to history
            favorites_manager.add_search(query, content_type, len(results))
            
            # Update UI on main thread
            def update_results():
                loading.visible = False
                results_container.controls.clear()
                
                if results:
                    status_message.value = f"Se encontraron {len(results)} resultado(s) de {content_type.lower()}"
                    for item in results:
                        results_container.controls.append(create_result_card(item, favorites_manager, content_type))
                else:
                    status_message.value = f"No se encontraron {content_type.lower()} para tu búsqueda"
                    results_container.controls.append(
                        ft.Container(
                            content=ft.Text(
                                "Intenta con otros términos de búsqueda",
                                size=14,
                                color=ft.Colors.GREY_600
                            ),
                            padding=20,
                            alignment=ft.alignment.center
                        )
                    )
                
                page.update()
            
            update_results()
            
        except Exception as e:
            def update_error():
                loading.visible = False
                status_message.value = f"Error en la búsqueda: {str(e)}"
                page.update()
            
            update_error()
    
    def on_search_click(e):
        if not search_input.value or search_input.value.strip() == "":
            status_message.value = "Por favor ingresa un término de búsqueda"
            page.update()
            return
        
        # Show loading
        loading.visible = True
        results_container.controls.clear()
        status_message.value = f"Buscando {current_search_type.lower()}..."
        page.update()
        
        # Start search in background thread
        search_thread = threading.Thread(
            target=search_content_async, 
            args=(search_input.value.strip(), current_search_type)
        )
        search_thread.daemon = True
        search_thread.start()
    
    def on_enter_pressed(e):
        """Handle Enter key press in search field"""
        on_search_click(e)
    
    # Add enter key handler to search input
    search_input.on_submit = on_enter_pressed
    
    def on_logout_click(e):
        login_view(page)
    
    # Buttons
    search_btn = ft.ElevatedButton(
        "🔍 Buscar",
        on_click=on_search_click,
        bgcolor=ft.Colors.GREEN_500,
        color=ft.Colors.WHITE,
        width=200
    )
    
    logout_btn = ft.TextButton(
        "Cerrar Sesión",
        on_click=on_logout_click
    )
    
    # Layout
    page.add(
        ft.Column(
            [
                welcome,
                ft.Container(height=10),
                nav_buttons,
                ft.Container(height=15),
                content_type_dropdown,
                search_input,
                ft.Row([search_btn, loading], alignment=ft.MainAxisAlignment.CENTER),
                status_message,
                ft.Container(height=10),
                results_container,
                ft.Container(height=15),
                logout_btn
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        )
    )

def favorites_view(page: ft.Page, username: str, favorites_manager, books_api, movies_api, anime_api, games_api):
    """Favorites view"""
    page.clean()
    
    # Welcome message
    welcome = ft.Text(
        f"Favoritos de {username}",
        size=25,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.RED_800
    )
    
    # Navigation buttons
    def show_search_view(e):
        search_view(page, username, favorites_manager, books_api, movies_api, anime_api, games_api)
    
    def show_favorites_view(e):
        favorites_view(page, username, favorites_manager, books_api, movies_api, anime_api, games_api)
    
    def show_recommendations_view(e):
        recommendations_view(page, username, favorites_manager, books_api, movies_api, anime_api, games_api)
    
    nav_buttons = ft.Row([
        ft.ElevatedButton(
            "🔍 Buscar",
            on_click=show_search_view,
            bgcolor=ft.Colors.BLUE_500,
            color=ft.Colors.WHITE
        ),
        ft.ElevatedButton(
            "❤️ Favoritos",
            on_click=show_favorites_view,
            bgcolor=ft.Colors.RED_700,
            color=ft.Colors.WHITE
        ),
        ft.ElevatedButton(
            "🎯 Recomendaciones",
            on_click=show_recommendations_view,
            bgcolor=ft.Colors.PURPLE_500,
            color=ft.Colors.WHITE
        ),
    ], alignment=ft.MainAxisAlignment.CENTER, spacing=10)
    
    # Favorites container
    favorites_container = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, height=400)
    
    def load_favorites():
        favorites = favorites_manager.load_favorites()
        favorites_container.controls.clear()
        
        if not favorites:
            favorites_container.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Text("No tienes favoritos aún", size=18, color=ft.Colors.GREY_600),
                        ft.Text("Busca contenido y agrega elementos a tus favoritos", size=14, color=ft.Colors.GREY_500)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=30,
                    alignment=ft.alignment.center
                )
            )
        else:
            for fav in favorites:
                card = create_favorite_card(fav)
                favorites_container.controls.append(card)
        
        page.update()
    
    def create_favorite_card(favorite):
        """Create a card for favorite item"""
        content_type = favorite.get('type', '')
        
        card_content = ft.Column([
            ft.Text(favorite['title'], size=16, weight=ft.FontWeight.BOLD, max_lines=2),
            ft.Text(f"Tipo: {content_type}", size=12, color=ft.Colors.GREY_700),
            ft.Text(f"Agregado: {favorite.get('added_date', 'Fecha desconocida')}", size=10, color=ft.Colors.GREY_600),
            ft.Text(favorite.get('description', ''), size=11, max_lines=2, color=ft.Colors.GREY_800),
        ], spacing=5)
        
        # Buttons row
        buttons_row = ft.Row(spacing=10)
        
        # Preview button
        if favorite.get('preview_link'):
            def open_preview(e, link=favorite['preview_link']):
                page.launch_url(link)
            preview_btn = ft.ElevatedButton(
                "Ver más",
                on_click=open_preview,
                bgcolor=ft.Colors.GREEN_500,
                color=ft.Colors.WHITE,
                height=30
            )
            buttons_row.controls.append(preview_btn)
        
        # Remove favorite button
        def remove_favorite(e, fav_id=favorite.get('favorite_id')):
            favorites_manager.remove_favorite(fav_id)
            load_favorites()  # Reload favorites
        
        remove_btn = ft.ElevatedButton(
            "🗑️ Quitar",
            on_click=remove_favorite,
            bgcolor=ft.Colors.RED_500,
            color=ft.Colors.WHITE,
            height=30
        )
        buttons_row.controls.append(remove_btn)
        
        card_content.controls.append(buttons_row)
        
        # Set color based on content type
        colors = {
            'Libros': (ft.Colors.BLUE_50, ft.Colors.BLUE_200),
            'Películas': (ft.Colors.YELLOW_50, ft.Colors.YELLOW_200),
            'Serie/Película': (ft.Colors.YELLOW_50, ft.Colors.YELLOW_200),
            'Anime': (ft.Colors.PURPLE_50, ft.Colors.PURPLE_200),
            'Videojuego': (ft.Colors.GREEN_50, ft.Colors.GREEN_200)
        }
        
        bg_color, border_color = colors.get(content_type, (ft.Colors.GREY_50, ft.Colors.GREY_200))
        
        return ft.Container(
            content=card_content,
            padding=15,
            bgcolor=bg_color,
            border_radius=10,
            width=300,
            border=ft.border.all(1, border_color)
        )
    
    def on_logout_click(e):
        login_view(page)
    
    logout_btn = ft.TextButton(
        "Cerrar Sesión",
        on_click=on_logout_click
    )
    
    # Layout
    page.add(
        ft.Column(
            [
                welcome,
                ft.Container(height=10),
                nav_buttons,
                ft.Container(height=15),
                favorites_container,
                ft.Container(height=15),
                logout_btn
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        )
    )
    
    # Load favorites on view load
    load_favorites()

def recommendations_view(page: ft.Page, username: str, favorites_manager, books_api, movies_api, anime_api, games_api):
    """Recommendations view"""
    page.clean()
    
    # Welcome message
    welcome = ft.Text(
        f"Recomendaciones para {username}",
        size=25,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.PURPLE_800
    )
    
    # Navigation buttons
    def show_search_view(e):
        search_view(page, username, favorites_manager, books_api, movies_api, anime_api, games_api)
    
    def show_favorites_view(e):
        favorites_view(page, username, favorites_manager, books_api, movies_api, anime_api, games_api)
    
    def show_recommendations_view(e):
        recommendations_view(page, username, favorites_manager, books_api, movies_api, anime_api, games_api)
    
    nav_buttons = ft.Row([
        ft.ElevatedButton(
            "🔍 Buscar",
            on_click=show_search_view,
            bgcolor=ft.Colors.BLUE_500,
            color=ft.Colors.WHITE
        ),
        ft.ElevatedButton(
            "❤️ Favoritos",
            on_click=show_favorites_view,
            bgcolor=ft.Colors.RED_500,
            color=ft.Colors.WHITE
        ),
        ft.ElevatedButton(
            "🎯 Recomendaciones",
            on_click=show_recommendations_view,
            bgcolor=ft.Colors.PURPLE_700,
            color=ft.Colors.WHITE
        ),
    ], alignment=ft.MainAxisAlignment.CENTER, spacing=10)
    
    # Loading indicator
    loading = ft.ProgressRing(visible=True)
    
    # Recommendations container
    recommendations_container = ft.Column(spacing=15, scroll=ft.ScrollMode.AUTO, height=400)
    
    def load_recommendations():
        """Load recommendations in background thread"""
        def generate_recommendations():
            try:
                recommendations = favorites_manager.generate_recommendations(
                    books_api, movies_api, anime_api, games_api
                )
                
                def update_ui():
                    loading.visible = False
                    recommendations_container.controls.clear()
                    
                    if not any(recommendations.values()):
                        recommendations_container.controls.append(
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("No hay recomendaciones disponibles", size=18, color=ft.Colors.GREY_600),
                                    ft.Text("Agrega algunos favoritos para obtener mejores recomendaciones", size=14, color=ft.Colors.GREY_500)
                                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                padding=30,
                                alignment=ft.alignment.center
                            )
                        )
                    else:
                        for category, items in recommendations.items():
                            if items:
                                # Category header
                                recommendations_container.controls.append(
                                    ft.Text(f"📚 {category}", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_700)
                                )
                                
                                # Items in this category
                                for item in items:
                                    card = create_recommendation_card(item, category)
                                    recommendations_container.controls.append(card)
                                
                                recommendations_container.controls.append(ft.Container(height=10))
                    
                    page.update()
                
                update_ui()
                
            except Exception as e:
                def update_error():
                    loading.visible = False
                    recommendations_container.controls.clear()
                    recommendations_container.controls.append(
                        ft.Container(
                            content=ft.Text(f"Error al generar recomendaciones: {str(e)}", color=ft.Colors.RED),
                            padding=20,
                            alignment=ft.alignment.center
                        )
                    )
                    page.update()
                
                update_error()
        
        # Start generation in background thread
        thread = threading.Thread(target=generate_recommendations)
        thread.daemon = True
        thread.start()
    
    def create_recommendation_card(item, category):
        """Create a card for recommended item"""
        card_content = ft.Column([
            ft.Text(item['title'], size=16, weight=ft.FontWeight.BOLD, max_lines=2),
            ft.Text(item.get('description', ''), size=11, max_lines=2, color=ft.Colors.GREY_800),
        ], spacing=5)
        
        # Buttons row
        buttons_row = ft.Row(spacing=10)
        
        # Preview button
        if item.get('preview_link'):
            def open_preview(e, link=item['preview_link']):
                page.launch_url(link)
            preview_btn = ft.ElevatedButton(
                "Ver más",
                on_click=open_preview,
                bgcolor=ft.Colors.GREEN_500,
                color=ft.Colors.WHITE,
                height=30
            )
            buttons_row.controls.append(preview_btn)
        
        # Add to favorites button
        def add_to_favorites(e, content=item):
            if favorites_manager.add_favorite(content):
                e.control.text = "❤️ Agregado"
                e.control.bgcolor = ft.Colors.RED_400
            else:
                e.control.text = "Ya en favoritos"
                e.control.bgcolor = ft.Colors.GREY_400
            page.update()
        
        fav_btn = ft.ElevatedButton(
            "🤍 Agregar",
            on_click=add_to_favorites,
            bgcolor=ft.Colors.GREY_300,
            color=ft.Colors.WHITE,
            height=30
        )
        buttons_row.controls.append(fav_btn)
        
        card_content.controls.append(buttons_row)
        
        # Set color based on content type
        colors = {
            'Libros': (ft.Colors.BLUE_50, ft.Colors.BLUE_200),
            'Películas': (ft.Colors.YELLOW_50, ft.Colors.YELLOW_200),
            'Anime': (ft.Colors.PURPLE_50, ft.Colors.PURPLE_200),
            'Videojuegos': (ft.Colors.GREEN_50, ft.Colors.GREEN_200)
        }
        
        bg_color, border_color = colors.get(category, (ft.Colors.GREY_50, ft.Colors.GREY_200))
        
        return ft.Container(
            content=card_content,
            padding=15,
            bgcolor=bg_color,
            border_radius=10,
            width=300,
            border=ft.border.all(1, border_color)
        )
    
    def on_logout_click(e):
        login_view(page)
    
    logout_btn = ft.TextButton(
        "Cerrar Sesión",
        on_click=on_logout_click
    )
    
    # Layout
    page.add(
        ft.Column(
            [
                welcome,
                ft.Container(height=10),
                nav_buttons,
                ft.Container(height=15),
                loading,
                recommendations_container,
                ft.Container(height=15),
                logout_btn
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        )
    )
    
    # Load recommendations on view load
    load_recommendations()
