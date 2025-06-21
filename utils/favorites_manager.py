import json
import os
from typing import List, Dict, Optional
from collections import Counter
import random

class FavoritesManager:
    def __init__(self, username: str):
        self.username = username
        self.favorites_file = f"favorites_{username}.json"
        self.search_history_file = f"search_history_{username}.json"
    
    def load_favorites(self) -> List[Dict]:
        """Load user's favorites from file"""
        if not os.path.exists(self.favorites_file):
            return []
        
        try:
            with open(self.favorites_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    return []
                return json.loads(content)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def save_favorites(self, favorites: List[Dict]) -> bool:
        """Save user's favorites to file"""
        try:
            with open(self.favorites_file, 'w', encoding='utf-8') as f:
                json.dump(favorites, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving favorites: {e}")
            return False
    
    def add_favorite(self, item: Dict) -> bool:
        """Add item to favorites"""
        favorites = self.load_favorites()
        
        # Check if item already exists (by title and type)
        for fav in favorites:
            if (fav.get('title', '').lower() == item.get('title', '').lower() and 
                fav.get('type', '') == item.get('type', '')):
                return False  # Already in favorites
        
        # Add timestamp and favorite ID
        item['favorite_id'] = len(favorites) + 1
        item['added_date'] = self._get_current_date()
        
        favorites.append(item)
        return self.save_favorites(favorites)
    
    def remove_favorite(self, favorite_id: int) -> bool:
        """Remove item from favorites by ID"""
        favorites = self.load_favorites()
        favorites = [fav for fav in favorites if fav.get('favorite_id') != favorite_id]
        return self.save_favorites(favorites)
    
    def is_favorite(self, title: str, content_type: str) -> bool:
        """Check if item is in favorites"""
        favorites = self.load_favorites()
        for fav in favorites:
            if (fav.get('title', '').lower() == title.lower() and 
                fav.get('type', '') == content_type):
                return True
        return False
    
    def load_search_history(self) -> List[Dict]:
        """Load user's search history"""
        if not os.path.exists(self.search_history_file):
            return []
        
        try:
            with open(self.search_history_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    return []
                return json.loads(content)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def save_search_history(self, history: List[Dict]) -> bool:
        """Save search history to file"""
        try:
            with open(self.search_history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving search history: {e}")
            return False
    
    def add_search(self, query: str, content_type: str, results_count: int):
        """Add search to history"""
        history = self.load_search_history()
        
        search_entry = {
            'query': query,
            'content_type': content_type,
            'results_count': results_count,
            'date': self._get_current_date(),
            'timestamp': self._get_timestamp()
        }
        
        # Keep only last 50 searches
        history.append(search_entry)
        if len(history) > 50:
            history = history[-50:]
        
        self.save_search_history(history)
    
    def generate_recommendations(self, books_api, movies_api, anime_api, games_api) -> Dict[str, List[Dict]]:
        """Generate recommendations based on favorites and search history"""
        favorites = self.load_favorites()
        search_history = self.load_search_history()
        
        recommendations = {
            'Libros': [],
            'Películas': [],
            'Anime': [],
            'Videojuegos': []
        }
        
        # Analyze favorite content types
        favorite_types = Counter([fav.get('type', '') for fav in favorites])
        search_types = Counter([search.get('content_type', '') for search in search_history[-20:]])  # Last 20 searches
        
        # Extract keywords from favorites and searches
        keywords = self._extract_keywords(favorites, search_history)
        
        # Generate recommendations for each type
        try:
            if keywords:
                # Books recommendations
                if 'Libros' in favorite_types or 'Libros' in search_types:
                    book_keywords = [kw for kw in keywords if random.random() > 0.5][:3]
                    for keyword in book_keywords:
                        books = books_api.search_books(keyword, max_results=2)
                        recommendations['Libros'].extend(books)
                
                # Movies recommendations  
                if 'Películas' in favorite_types or 'Serie/Película' in favorite_types or 'Películas' in search_types:
                    movie_keywords = [kw for kw in keywords if random.random() > 0.5][:3]
                    for keyword in movie_keywords:
                        movies = movies_api.search_movies(keyword, max_results=2)
                        recommendations['Películas'].extend(movies)
                
                # Anime recommendations
                if 'Anime' in favorite_types or 'Anime' in search_types:
                    anime_keywords = [kw for kw in keywords if random.random() > 0.5][:3]
                    for keyword in anime_keywords:
                        animes = anime_api.search_anime(keyword, max_results=2)
                        recommendations['Anime'].extend(animes)
                
                # Games recommendations
                if 'Videojuego' in favorite_types or 'Videojuegos' in search_types:
                    game_keywords = [kw for kw in keywords if random.random() > 0.5][:3]
                    for keyword in game_keywords:
                        games = games_api.search_games(keyword, max_results=2)
                        recommendations['Videojuegos'].extend(games)
            
            # If no specific recommendations, add popular content
            self._add_popular_recommendations(recommendations, books_api, movies_api, anime_api, games_api)
            
        except Exception as e:
            print(f"Error generating recommendations: {e}")
            self._add_popular_recommendations(recommendations, books_api, movies_api, anime_api, games_api)
        
        # Limit recommendations per category
        for category in recommendations:
            recommendations[category] = recommendations[category][:5]  # Max 5 per category
        
        return recommendations
    
    def _extract_keywords(self, favorites: List[Dict], search_history: List[Dict]) -> List[str]:
        """Extract keywords from favorites and search history"""
        keywords = []
        
        # From favorites
        for fav in favorites:
            title = fav.get('title', '')
            if title:
                # Extract words from title (simple approach)
                words = title.lower().split()
                keywords.extend([word for word in words if len(word) > 3])
        
        # From search history
        for search in search_history[-10:]:  # Last 10 searches
            query = search.get('query', '')
            if query:
                words = query.lower().split()
                keywords.extend([word for word in words if len(word) > 3])
        
        # Return most common keywords
        keyword_counts = Counter(keywords)
        return [keyword for keyword, count in keyword_counts.most_common(10)]
    
    def _add_popular_recommendations(self, recommendations: Dict, books_api, movies_api, anime_api, games_api):
        """Add popular content when no specific recommendations available"""
        popular_queries = {
            'Libros': ['bestseller', 'fiction', 'mystery'],
            'Películas': ['action', 'comedy', 'drama'],
            'Anime': ['popular', 'action', 'adventure'],
            'Videojuegos': ['popular', 'action', 'adventure']
        }
        
        for category, queries in popular_queries.items():
            if len(recommendations[category]) < 3:
                try:
                    query = random.choice(queries)
                    if category == 'Libros':
                        results = books_api.search_books(query, max_results=3)
                    elif category == 'Películas':
                        results = movies_api.search_movies(query, max_results=3)
                    elif category == 'Anime':
                        results = anime_api.search_anime(query, max_results=3)
                    elif category == 'Videojuegos':
                        results = games_api.search_games(query, max_results=3)
                    
                    recommendations[category].extend(results)
                except:
                    pass
    
    def _get_current_date(self) -> str:
        """Get current date as string"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d")
    
    def _get_timestamp(self) -> float:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().timestamp()