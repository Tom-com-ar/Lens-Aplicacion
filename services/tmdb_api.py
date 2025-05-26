import requests

API_KEY = "e6822a7ed386f7102b6a857ea5e3c17f"

class TMDBApi:
    def __init__(self):
        self.api_key = API_KEY
        self.base_url = "https://api.themoviedb.org/3"
        self.generos = self.obtener_generos()  # Cargar géneros al iniciar

    def obtener_generos(self):
        url = f"{self.base_url}/genre/movie/list"
        params = {
            "api_key": self.api_key,
            "language": "es-ES"
        }
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                return response.json().get("genres", [])
            else:
                print(f"Error al obtener géneros: {response.status_code}")
                return []
        except Exception as e:
            print(f"Error al conectar con TMDB (géneros): {str(e)}")
            return []

    def obtener_peliculas_populares(self, pagina=1):
        url = f"{self.base_url}/movie/popular"
        params = {
            "api_key": self.api_key,
            "language": "es-ES",
            "page": pagina
        }
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                return response.json().get("results", [])
            else:
                return []
        except Exception as e:
            print(f"Error al conectar con TMDB (populares): {str(e)}")
            return []

    def obtener_detalle_pelicula(self, pelicula_id):
        url = f"{self.base_url}/movie/{pelicula_id}"
        params = {
            "api_key": self.api_key,
            "language": "es-ES"
        }
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as e:
            print(f"Error al conectar con TMDB (detalle): {str(e)}")
            return None

    def buscar_peliculas(self, query, pagina=1):
        url = f"{self.base_url}/search/movie"
        params = {
            "api_key": self.api_key,
            "language": "es-ES",
            "query": query,
            "page": pagina
        }
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                return response.json().get("results", [])
            else:
                return []
        except Exception as e:
            print(f"Error al conectar con TMDB (buscar): {str(e)}")
            return []
        
    def obtener_videos_pelicula(self, pelicula_id):
        url = f"{self.base_url}/movie/{pelicula_id}/videos"
        params = {
            "api_key": self.api_key,
            "language": "es-ES"
        }
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                return response.json().get("results", [])
            else:
                print(f"Error en la respuesta (videos): {response.status_code}")
                return []
        except Exception as e:
            print(f"Error al conectar con TMDB (videos): {str(e)}")
            return []