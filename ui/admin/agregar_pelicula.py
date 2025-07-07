import flet as ft
from services.db import db

COLOR_NARANJA = "#FF9D00"
COLOR_FONDO = "#181818"
COLOR_TEXTO = "#FFFFFF"
GENERO_LISTA = [
    "Acción", "Aventura", "Animación", "Comedia", "Crimen", "Documental", "Drama", "Familia", "Fantasía", "Historia", "Terror", "Música", "Misterio", "Romance", "Ciencia ficción", "Película de TV", "Suspense", "Bélica", "Western"
]

class AgregarPeliculaAdminSection(ft.Column):
    def __init__(self, on_volver, pelicula=None):
        super().__init__(expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        self.on_volver = on_volver
        self.pelicula = pelicula
        self.mensaje = ft.Text("", color=COLOR_NARANJA, size=16)
        self.titulo = ft.TextField(label="Título", width=600, bgcolor=COLOR_FONDO, color=COLOR_TEXTO, border_color=COLOR_NARANJA, label_style=ft.TextStyle(color=COLOR_NARANJA, weight="bold"))
        self.descripcion = ft.TextField(label="Descripción", width=600, multiline=True, min_lines=4, max_lines=6, bgcolor=COLOR_FONDO, color=COLOR_TEXTO, border_color=COLOR_NARANJA, label_style=ft.TextStyle(color=COLOR_NARANJA, weight="bold"))
        self.generos_checks = [ft.Checkbox(label=g, value=False, fill_color=COLOR_NARANJA, check_color=COLOR_TEXTO) for g in GENERO_LISTA]
        self.fecha_estreno = ft.TextField(label="Fecha de Estreno (YYYY)", width=300, bgcolor=COLOR_FONDO, color=COLOR_TEXTO, border_color=COLOR_NARANJA, label_style=ft.TextStyle(color=COLOR_NARANJA, weight="bold"))
        self.duracion = ft.TextField(label="Duración (minutos)", width=300, bgcolor=COLOR_FONDO, color=COLOR_TEXTO, border_color=COLOR_NARANJA, label_style=ft.TextStyle(color=COLOR_NARANJA, weight="bold"))
        self.trailer_url = ft.TextField(label="URL del Trailer (YouTube)", width=600, bgcolor=COLOR_FONDO, color=COLOR_TEXTO, border_color=COLOR_NARANJA, label_style=ft.TextStyle(color=COLOR_NARANJA, weight="bold"))
        self.actores = ft.TextField(label="Actores (separados por comas)", width=600, multiline=True, min_lines=2, max_lines=3, bgcolor=COLOR_FONDO, color=COLOR_TEXTO, border_color=COLOR_NARANJA, label_style=ft.TextStyle(color=COLOR_NARANJA, weight="bold"))
        self.imagen_url = ft.TextField(label="Imagen de Portada (URL)", width=600, bgcolor=COLOR_FONDO, color=COLOR_TEXTO, border_color=COLOR_NARANJA, label_style=ft.TextStyle(color=COLOR_NARANJA, weight="bold"))
        self.boton_agregar = ft.ElevatedButton(
            "Agregar Película" if not pelicula else "Guardar Cambios",
            bgcolor=COLOR_NARANJA,
            color="#ffffff",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
            on_click=self.guardar_pelicula
        )
        if pelicula:
            self.titulo.value = pelicula.get("titulo", "")
            self.descripcion.value = pelicula.get("descripcion", "")
            generos = (pelicula.get("genero") or "").split(", ")
            for g in self.generos_checks:
                g.value = g.label in generos
            self.fecha_estreno.value = str(pelicula.get("fecha_estreno") or "")
            self.duracion.value = str(pelicula.get("duracion") or "")
            self.trailer_url.value = pelicula.get("trailer_url") or ""
            self.actores.value = pelicula.get("actores") or ""
            self.imagen_url.value = pelicula.get("imagen_portada") or ""
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
            ft.Text("Editar Película Manual" if pelicula else "Agregar Película Manualmente", size=32, weight="bold", color=COLOR_NARANJA),
            ft.Container(height=10),
            ft.Container(
                content=ft.Column([
                    self.titulo,
                    self.descripcion,
                    ft.Text("Géneros:", color=COLOR_NARANJA, weight="bold"),
                    ft.Column(self.generos_checks, spacing=8),
                    self.fecha_estreno,
                    self.duracion,
                    self.trailer_url,
                    self.actores,
                    self.imagen_url,
                    self.boton_agregar,
                    self.mensaje
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=16),
                bgcolor=COLOR_FONDO,
                border_radius=16,
                padding=30,
                width=700,
                shadow=ft.BoxShadow(blur_radius=10, color=COLOR_NARANJA)
            )
        ]

    def guardar_pelicula(self, e):
        titulo = self.titulo.value.strip()
        descripcion = self.descripcion.value.strip()
        generos = ", ".join([g.label for g in self.generos_checks if g.value])
        fecha_estreno = self.fecha_estreno.value.strip()
        duracion = self.duracion.value.strip()
        trailer_url = self.trailer_url.value.strip()
        actores = self.actores.value.strip()
        imagen_url = self.imagen_url.value.strip()
        if not titulo:
            self.mensaje.value = "El título es obligatorio."
            self.update()
            return
        if not generos:
            self.mensaje.value = "Selecciona al menos un género."
            self.update()
            return
        try:
            if self.pelicula:
                db.execute_query(
                    """
                    UPDATE peliculas SET titulo=%s, descripcion=%s, genero=%s, fecha_estreno=%s, duracion=%s, imagen_portada=%s, trailer_url=%s, actores=%s, fecha_actualizada=NOW() WHERE id_pelicula=%s
                    """,
                    (titulo, descripcion, generos, fecha_estreno, duracion, imagen_url, trailer_url, actores, self.pelicula["id_pelicula"])
                )
                self.mensaje.value = f"Película '{titulo}' actualizada con éxito."
            else:
                db.execute_query(
                    """
                    INSERT INTO peliculas (origen, titulo, descripcion, genero, fecha_estreno, duracion, imagen_portada, trailer_url, actores, estado)
                    VALUES ('manual', %s, %s, %s, %s, %s, %s, %s, %s, 'activa')
                    """,
                    (titulo, descripcion, generos, fecha_estreno, duracion, imagen_url, trailer_url, actores)
                )
                self.mensaje.value = f"Película '{titulo}' agregada con éxito."
            self.update()
        except Exception as ex:
            self.mensaje.value = f"Error al guardar: {ex}"
            self.update() 