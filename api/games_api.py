import requests
import json
from typing import List, Dict, Optional
import random

class GamesAPI:
    def __init__(self):
        # Como RAWG requiere API key, crearemos datos de muestra
        self.sample_games_db = {
            'halo': ['Halo Infinite', 'Halo: The Master Chief Collection', 'Halo 5: Guardians'],
            'call of duty': ['Call of Duty: Modern Warfare', 'Call of Duty: Warzone', 'Call of Duty: Black Ops'],
            'fifa': ['FIFA 24', 'FIFA 23', 'EA Sports FC 24'],
            'gta': ['Grand Theft Auto V', 'Grand Theft Auto: San Andreas', 'Grand Theft Auto IV'],
            'minecraft': ['Minecraft', 'Minecraft Dungeons', 'Minecraft Legends'],
            'fortnite': ['Fortnite', 'Fortnite: Save the World', 'Fortnite Creative'],
            'zelda': ['The Legend of Zelda: Breath of the Wild', 'The Legend of Zelda: Tears of the Kingdom', 'The Legend of Zelda: Link\'s Awakening'],
            'mario': ['Super Mario Odyssey', 'Super Mario Bros. Wonder', 'Mario Kart 8 Deluxe'],
            'pokemon': ['Pokémon Scarlet', 'Pokémon Violet', 'Pokémon Legends: Arceus'],
            'god of war': ['God of War', 'God of War Ragnarök', 'God of War III'],
        }
        
        self.genres = ['Acción', 'Aventura', 'RPG', 'Shooter', 'Deportes', 'Estrategia', 'Plataformas', 'Simulación']
        self.platforms = ['PC', 'PlayStation 5', 'Xbox Series X/S', 'Nintendo Switch', 'PlayStation 4', 'Xbox One']
    
    def search_games(self, query: str, max_results: int = 10) -> List[Dict]:
        """
        Search for games using sample data (since RAWG requires API key)
        """
        try:
            games = []
            query_lower = query.lower()
            
            # Buscar en nuestra base de datos de muestra
            for key, game_list in self.sample_games_db.items():
                if query_lower in key or any(query_lower in game.lower() for game in game_list):
                    for game_name in game_list[:3]:  # Máximo 3 por categoría
                        game_info = self._create_game_info(game_name, query)
                        games.append(game_info)
            
            # Si no encontramos nada específico, crear juegos genéricos
            if not games:
                games = self._create_generic_games(query, max_results)
            
            return games[:max_results]
            
        except Exception as e:
            print(f"Error al buscar videojuegos: {e}")
            return self._create_generic_games(query, max_results)
    
    def _create_game_info(self, name: str, search_query: str) -> Dict:
        """
        Create game information
        """
        year = random.randint(2018, 2024)
        rating = round(random.uniform(3.5, 5.0), 1)
        metacritic = random.randint(70, 95)
        selected_genres = random.sample(self.genres, random.randint(1, 3))
        selected_platforms = random.sample(self.platforms, random.randint(2, 4))
        
        return {
            'title': name,
            'released': f'{year}-{random.randint(1,12):02d}-{random.randint(1,28):02d}',
            'rating': rating,
            'rating_count': random.randint(1000, 50000),
            'background_image': '',
            'platforms': selected_platforms,
            'genres': selected_genres,
            'metacritic': metacritic,
            'type': 'Videojuego',
            'description': f'Un emocionante videojuego de {", ".join(selected_genres[:2])} lanzado en {year}. Disponible en {", ".join(selected_platforms[:2])} y más plataformas.',
            'preview_link': f'https://store.steampowered.com/search/?term={name.replace(" ", "+")}'
        }
    
    def _create_generic_games(self, query: str, max_results: int) -> List[Dict]:
        """
        Create generic games when no specific matches found
        """
        games = []
        game_types = ['Adventure', 'Action', 'RPG', 'Simulator', 'Strategy']
        
        for i in range(max_results):
            game_type = random.choice(game_types)
            name = f'{query.title()} {game_type} {i+1}'
            games.append(self._create_game_info(name, query))
        
        return games
    
    def _extract_game_info(self, item: Dict) -> Optional[Dict]:
        """
        This method is kept for compatibility but not used with sample data
        """
        return None