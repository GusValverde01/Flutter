import requests
import json
from datetime import datetime

class BooksAPI:
    def __init__(self):
        self.base_url = "https://www.googleapis.com/books/v1/volumes"
    
    def search_books(self, query):
        """Busca libros usando la API de Google Books"""
        try:
            params = {
                'q': query,
                'maxResults': 15,
                'printType': 'books',
                'orderBy': 'relevance'
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            books = []
            
            if 'items' in data:
                for item in data['items']:
                    volume_info = item.get('volumeInfo', {})
                    
                    # Extraer información del libro
                    title = volume_info.get('title', 'Título no disponible')
                    authors = volume_info.get('authors', ['Autor no disponible'])
                    author = ', '.join(authors) if isinstance(authors, list) else str(authors)
                    
                    description = volume_info.get('description', 'Descripción no disponible')
                    if len(description) > 200:
                        description = description[:200] + '...'
                    
                    published_date = volume_info.get('publishedDate', 'No disponible')
                    page_count = volume_info.get('pageCount', 'No disponible')
                    
                    # Calificación promedio
                    average_rating = volume_info.get('averageRating', 0)
                    ratings_count = volume_info.get('ratingsCount', 0)
                    
                    # Link de vista previa
                    preview_link = volume_info.get('previewLink', '#')
                    
                    # Categorías
                    categories = volume_info.get('categories', ['Sin categoría'])
                    category = categories[0] if categories else 'Sin categoría'
                    
                    book = {
                        'id': item.get('id', ''),
                        'title': title,
                        'author': author,
                        'description': description,
                        'published_date': published_date,
                        'page_count': page_count,
                        'average_rating': average_rating,
                        'ratings_count': ratings_count,
                        'preview_link': preview_link,
                        'category': category,
                        'type': 'libro'
                    }
                    books.append(book)
            
            return books
            
        except requests.exceptions.RequestException as e:
            print(f"Error en la API de Google Books: {e}")
            return self._get_fallback_books(query)
        except Exception as e:
            print(f"Error inesperado en búsqueda de libros: {e}")
            return self._get_fallback_books(query)
    
    def _get_fallback_books(self, query):
        """Libros de respaldo cuando la API falla"""
        fallback_books = [
            {
                'id': 'fb_1',
                'title': 'Cien años de soledad',
                'author': 'Gabriel García Márquez',
                'description': 'Una obra maestra del realismo mágico que narra la historia de la familia Buendía en el pueblo ficticio de Macondo.',
                'published_date': '1967',
                'page_count': 417,
                'average_rating': 4.5,
                'ratings_count': 50000,
                'preview_link': 'https://books.google.com',
                'category': 'Ficción Literaria',
                'type': 'libro'
            },
            {
                'id': 'fb_2',
                'title': 'El principito',
                'author': 'Antoine de Saint-Exupéry',
                'description': 'Una historia poética sobre un pequeño príncipe que viaja por diferentes planetas y sus reflexiones sobre la vida.',
                'published_date': '1943',
                'page_count': 96,
                'average_rating': 4.7,
                'ratings_count': 75000,
                'preview_link': 'https://books.google.com',
                'category': 'Literatura Infantil',
                'type': 'libro'
            },
            {
                'id': 'fb_3',
                'title': 'Don Quijote de la Mancha',
                'author': 'Miguel de Cervantes',
                'description': 'Las aventuras del ingenioso hidalgo Don Quijote y su fiel escudero Sancho Panza.',
                'published_date': '1605',
                'page_count': 863,
                'average_rating': 4.3,
                'ratings_count': 40000,
                'preview_link': 'https://books.google.com',
                'category': 'Clásicos',
                'type': 'libro'
            },
            {
                'id': 'fb_4',
                'title': '1984',
                'author': 'George Orwell',
                'description': 'Una distopía sobre un futuro totalitario donde el Gran Hermano controla todos los aspectos de la vida.',
                'published_date': '1949',
                'page_count': 328,
                'average_rating': 4.6,
                'ratings_count': 85000,
                'preview_link': 'https://books.google.com',
                'category': 'Ciencia Ficción',
                'type': 'libro'
            },
            {
                'id': 'fb_5',
                'title': 'Harry Potter y la Piedra Filosofal',
                'author': 'J.K. Rowling',
                'description': 'La historia de un joven mago que descubre su verdadera identidad en su undécimo cumpleaños.',
                'published_date': '1997',
                'page_count': 223,
                'average_rating': 4.8,
                'ratings_count': 120000,
                'preview_link': 'https://books.google.com',
                'category': 'Fantasía',
                'type': 'libro'
            }
        ]
        
        # Filtrar libros que coincidan con la búsqueda
        query_lower = query.lower()
        matching_books = []
        
        for book in fallback_books:
            if (query_lower in book['title'].lower() or 
                query_lower in book['author'].lower() or 
                query_lower in book['category'].lower() or
                any(word in book['title'].lower() for word in query_lower.split())):
                matching_books.append(book)
        
        # Si no hay coincidencias, devolver algunos libros populares
        if not matching_books:
            return fallback_books[:3]
        
        return matching_books