import requests
import json
from typing import List, Dict, Optional

class BooksAPI:
    def __init__(self):
        self.base_url = "https://www.googleapis.com/books/v1/volumes"
    
    def search_books(self, query: str, max_results: int = 10) -> List[Dict]:
        """
        Search for books using Google Books API
        """
        try:
            params = {
                'q': query,
                'maxResults': max_results,
                'printType': 'books',
                'orderBy': 'relevance'
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            books = []
            
            if 'items' in data:
                for item in data['items']:
                    book_info = self._extract_book_info(item)
                    if book_info:
                        books.append(book_info)
            
            return books
            
        except requests.exceptions.RequestException as e:
            print(f"Error al buscar libros: {e}")
            return []
        except json.JSONDecodeError as e:
            print(f"Error al procesar respuesta: {e}")
            return []
    
    def _extract_book_info(self, item: Dict) -> Optional[Dict]:
        """
        Extract relevant book information from API response
        """
        try:
            volume_info = item.get('volumeInfo', {})
            
            # Extract basic info
            title = volume_info.get('title', 'Título no disponible')
            authors = volume_info.get('authors', ['Autor desconocido'])
            description = volume_info.get('description', 'Sin descripción disponible')
            
            # Limit description length
            if len(description) > 200:
                description = description[:200] + "..."
            
            # Extract additional info
            published_date = volume_info.get('publishedDate', 'Fecha no disponible')
            page_count = volume_info.get('pageCount', 'No disponible')
            categories = volume_info.get('categories', ['Sin categoría'])
            
            # Extract image
            image_links = volume_info.get('imageLinks', {})
            thumbnail = image_links.get('thumbnail', '')
            
            # Extract preview link
            preview_link = volume_info.get('previewLink', '')
            
            # Extract rating
            average_rating = volume_info.get('averageRating', 'Sin calificación')
            ratings_count = volume_info.get('ratingsCount', 0)
            
            return {
                'title': title,
                'authors': authors,
                'description': description,
                'published_date': published_date,
                'page_count': page_count,
                'categories': categories,
                'thumbnail': thumbnail,
                'preview_link': preview_link,
                'average_rating': average_rating,
                'ratings_count': ratings_count,
                'type': 'Libros'
            }
            
        except Exception as e:
            print(f"Error al extraer información del libro: {e}")
            return None
    
    def get_book_by_id(self, book_id: str) -> Optional[Dict]:
        """
        Get detailed book information by ID
        """
        try:
            url = f"{self.base_url}/{book_id}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return self._extract_book_info(data)
            
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener libro por ID: {e}")
            return None