import flet as ft
import requests
from services.db import db

COLOR_NARANJA = "#FF9D00"
COLOR_FONDO = "#181818"
COLOR_TEXTO = "#FFFFFF"
API_KEY = "e6822a7ed386f7102b6a857ea5e3c17f"

class BuscarApiAdminSection(ft.Column):
    def __init__(self, on_volver):
        super().__init__(expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        self.on_volver = on_volver
        self.resultados = ft.Column(spacing=20, expand=True)
        self.campo_busqueda = ft.TextField(
            label="Buscar película",
            hint_text="Título o palabra clave",
            bgcolor=COLOR_FONDO,
            color=COLOR_TEXTO,
            border_radius=10,
            width=400,
            border_color=COLOR_NARANJA,
            label_style=ft.TextStyle(color=COLOR_NARANJA, weight="bold"),
        )
        self.boton_buscar = ft.ElevatedButton(
            "Buscar",
            bgcolor=COLOR_NARANJA,
            color="#ffffff",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
            on_click=self.buscar_peliculas
        )
        self.mensaje = ft.Text("", color=COLOR_NARANJA, size=16)
        self.controls = [
            ft.Container(
                ft.ElevatedButton(
                    "← Volver al panel principal",
                    on_click=lambda e: self.on_volver(),
                    bgcolor=COLOR_NARANJA,
                    color="#ffffff",
                    style=ft.ButtonStyle(padding=ft.padding.symmetric(horizontal=30, vertical=16), shape=ft.RoundedRectangleBorder(radius=20)),
                    icon="arrow_back"
                ),
                alignment=ft.alignment.center,
                margin=ft.margin.only(top=20, bottom=30)
            ),
            ft.Text("Buscar y Agregar Películas desde la API", size=32, weight="bold", color=COLOR_NARANJA),
            ft.Container(height=20),
            ft.Container(
                content=ft.Column([
                    self.campo_busqueda,
                    self.boton_buscar,
                    self.mensaje
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=16),
                bgcolor=COLOR_FONDO,
                border_radius=16,
                padding=30,
                width=600,
                shadow=ft.BoxShadow(blur_radius=10, color=COLOR_NARANJA)
            ),
            ft.Container(height=20),
            self.resultados
        ]

    def buscar_peliculas(self, e):
        query = self.campo_busqueda.value.strip()
        self.resultados.controls.clear()
        self.mensaje.value = ""
        if not query:
            self.mensaje.value = "Ingresa un título para buscar."
            self.update()
            return
        url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&language=es-ES&query={query}"
        try:
            resp = requests.get(url)
            data = resp.json()
            resultados = data.get("results", [])
            if not resultados:
                self.mensaje.value = "No se encontraron resultados."
                self.update()
                return
            for peli in resultados:
                self.resultados.controls.append(self.pelicula_card(peli))
            self.update()
        except Exception as ex:
            self.mensaje.value = f"Error al buscar: {ex}"
            self.update()

    def pelicula_card(self, peli):
        titulo = peli.get("title", "Sin título")
        descripcion = peli.get("overview", "Sin descripción")
        anio = peli.get("release_date", "")[:4]
        poster = peli.get("poster_path")
        poster_url = f"https://image.tmdb.org/t/p/w200{poster}" if poster else "https://via.placeholder.com/120x180?text=Sin+Imagen"
        return ft.Container(
            content=ft.Row([
                ft.Image(src=poster_url, width=120, height=180, border_radius=10),
                ft.Container(width=20),
                ft.Column([
                    ft.Text(titulo, size=20, weight="bold", color=COLOR_NARANJA),
                    ft.Text(f"Año: {anio}", color=COLOR_TEXTO),
                    ft.Text(descripcion, color=COLOR_TEXTO, size=14, max_lines=4, overflow=ft.TextOverflow.ELLIPSIS),
                    ft.ElevatedButton(
                        "Agregar",
                        bgcolor=COLOR_NARANJA,
                        color="#ffffff",
                        icon="add",
                        on_click=lambda e, peli=peli: self.agregar_pelicula_bd(peli)
                    )
                ], spacing=8)
            ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor="#222",
            border_radius=12,
            padding=16,
            margin=ft.margin.only(bottom=10),
            width=600
        )

    def agregar_pelicula_bd(self, peli):
        tmdb_id = peli.get("id")
        # Verificar si ya existe en la base de datos
        existe = db.execute_query("SELECT id_pelicula FROM peliculas WHERE tmdb_id = %s", (tmdb_id,))
        if existe:
            self.mensaje.value = "La película ya existe en la base de datos."
            self.update()
            return
        # Consultar detalles completos en TMDB
        url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={API_KEY}&language=es-ES"
        try:
            resp = requests.get(url)
            detalles = resp.json()
            titulo = detalles.get("title", "Sin título")
            descripcion = detalles.get("overview", "")
            # Géneros como string separados por coma
            generos = ", ".join([g["name"] for g in detalles.get("genres", [])])
            fecha_estreno = detalles.get("release_date", "")[:4] if detalles.get("release_date") else None
            duracion = detalles.get("runtime")
            imagen_portada = f"https://image.tmdb.org/t/p/w500{detalles.get('poster_path')}" if detalles.get("poster_path") else None
            trailer_url = None
            actores = None
            clasificacion = detalles.get("adult")
            estado = "activa"
            db.execute_query(
                """
                INSERT INTO peliculas (origen, tmdb_id, titulo, descripcion, genero, fecha_estreno, duracion, imagen_portada, trailer_url, actores, clasificacion, estado)
                VALUES ('api', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (tmdb_id, titulo, descripcion, generos, fecha_estreno, duracion, imagen_portada, trailer_url, actores, clasificacion, estado)
            )
            self.mensaje.value = f"Película '{titulo}' agregada con éxito."
            self.update()
        except Exception as ex:
            self.mensaje.value = f"Error al agregar: {ex}"
            self.update() 