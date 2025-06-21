import flet as ft
import webbrowser

def create_result_card(content, favorites_manager, content_type):
    """Create a card widget for search results with favorites functionality"""
    card_content = ft.Column(spacing=5)
    
    # Title
    card_content.controls.append(
        ft.Text(content['title'], size=16, weight=ft.FontWeight.BOLD, max_lines=2)
    )
    
    # Content-specific information
    if content_type == "Libros":
        authors = content.get('authors', ['Autor desconocido'])
        authors_str = ", ".join(authors) if isinstance(authors, list) else str(authors)
        rating_text = f"⭐ {content.get('average_rating', 'Sin calificación')}"
        
        card_content.controls.extend([
            ft.Text(f"Por: {authors_str}", size=12, color=ft.Colors.GREY_700),
            ft.Text(f"Publicado: {content.get('published_date', 'N/A')}", size=10, color=ft.Colors.GREY_600),
            ft.Text(f"Páginas: {content.get('page_count', 'N/A')}", size=10, color=ft.Colors.GREY_600),
            ft.Text(rating_text, size=10, color=ft.Colors.ORANGE_600),
        ])
        card_color = ft.Colors.BLUE_50
        border_color = ft.Colors.BLUE_200
        
    elif content_type == "Películas":
        card_content.controls.extend([
            ft.Text(f"Año: {content.get('year', 'N/A')}", size=12, color=ft.Colors.GREY_700),
            ft.Text(f"Tipo: {content.get('type', 'N/A')}", size=10, color=ft.Colors.GREY_600),
        ])
        card_color = ft.Colors.YELLOW_50
        border_color = ft.Colors.YELLOW_200
        
    elif content_type == "Anime":
        rating_text = f"⭐ {content.get('score', 'Sin calificación')}"
        episodes_text = f"Episodios: {content.get('episodes', 'No disponible')}"
        
        card_content.controls.extend([
            ft.Text(f"Año: {content.get('year', 'N/A')}", size=12, color=ft.Colors.GREY_700),
            ft.Text(episodes_text, size=10, color=ft.Colors.GREY_600),
            ft.Text(f"Estado: {content.get('status', 'N/A')}", size=10, color=ft.Colors.GREY_600),
            ft.Text(rating_text, size=10, color=ft.Colors.ORANGE_600),
        ])
        card_color = ft.Colors.PURPLE_50
        border_color = ft.Colors.PURPLE_200
        
    elif content_type == "Videojuegos":
        rating_text = f"⭐ {content.get('rating', 'Sin calificación')}"
        metacritic = content.get('metacritic', '')
        
        card_content.controls.extend([
            ft.Text(f"Lanzamiento: {content.get('released', 'N/A')}", size=12, color=ft.Colors.GREY_700),
            ft.Text(rating_text, size=10, color=ft.Colors.ORANGE_600),
        ])
        if metacritic and metacritic != 'Sin puntuación':
            card_content.controls.append(ft.Text(f"Metacritic: {metacritic}", size=10, color=ft.Colors.GREY_600))
        card_color = ft.Colors.GREEN_50
        border_color = ft.Colors.GREEN_200
    else:
        card_color = ft.Colors.GREY_50
        border_color = ft.Colors.GREY_200
    
    # Description
    description = content.get('description', 'Sin descripción disponible')
    card_content.controls.append(
        ft.Text(description, size=11, max_lines=3, color=ft.Colors.GREY_800)
    )
    
    # Buttons row
    buttons_row = ft.Row(spacing=10)
    
    # Preview button
    if content.get('preview_link'):
        def open_preview(e, link=content['preview_link']):
            import webbrowser
            webbrowser.open(link)
        
        preview_btn = ft.ElevatedButton(
            "Ver más",
            on_click=open_preview,
            bgcolor=ft.Colors.GREEN_500,
            color=ft.Colors.WHITE,
            height=30
        )
        buttons_row.controls.append(preview_btn)
    
    # Favorite button
    is_fav = favorites_manager.is_favorite(content['title'], content.get('type', content_type))
    fav_icon = "❤️" if is_fav else "🤍"
    fav_text = "Quitar" if is_fav else "Favorito"
    
    def toggle_favorite(e, item=content):
        title = item['title']
        item_type = item.get('type', content_type)
        
        if favorites_manager.is_favorite(title, item_type):
            # Remove from favorites
            favorites = favorites_manager.load_favorites()
            for fav in favorites:
                if (fav.get('title', '').lower() == title.lower() and 
                    fav.get('type', '') == item_type):
                    favorites_manager.remove_favorite(fav.get('favorite_id'))
                    break
            e.control.text = "🤍 Favorito"
            e.control.bgcolor = ft.Colors.GREY_300
        else:
            # Add to favorites
            favorites_manager.add_favorite(item)
            e.control.text = "❤️ Quitar"
            e.control.bgcolor = ft.Colors.RED_400
    
    favorite_btn = ft.ElevatedButton(
        f"{fav_icon} {fav_text}",
        on_click=toggle_favorite,
        bgcolor=ft.Colors.RED_400 if is_fav else ft.Colors.GREY_300,
        color=ft.Colors.WHITE,
        height=30
    )
    buttons_row.controls.append(favorite_btn)
    
    card_content.controls.append(buttons_row)
    
    return ft.Container(
        content=card_content,
        padding=15,
        bgcolor=card_color,
        border_radius=10,
        width=300,
        border=ft.border.all(1, border_color)
    )