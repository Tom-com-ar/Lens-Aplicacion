import flet as ft
from services.db import db # Importar la instancia de la base de datos

COLOR_NARANJA = "#FF9D00"
COLOR_FONDO = "#000000"
COLOR_TEXTO = "#FFFFFF"
COLOR_GRIS_CLARO = "#D9D9D9"
COLOR_ERROR = "#FF0000"

class ComentariosUI(ft.Column):
    def __init__(self, page: ft.Page, pelicula=None, volver_callback=None, user_id=None):
        super().__init__(expand=True, scroll="auto", horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        self.page = page
        self.pelicula = pelicula
        self.volver_callback = volver_callback
        self.user_id = user_id # Almacenar el ID del usuario
        self.spacing = 20

        self.campo_resena_ref = ft.Ref[ft.TextField]()
        
        # Slider para la valoración
        self.valoracion_slider = ft.Slider(
            min=1,
            max=5,
            divisions=4,
            label="{value}",
            value=5,
            width=400,
            active_color=COLOR_NARANJA,
            inactive_color=COLOR_GRIS_CLARO
        )

        self.create_widgets()

    def create_widgets(self):
        titulo = ft.Text(
            f"Deja tu reseña para: {self.pelicula.get('title', 'Película desconocida')}",
            color=COLOR_TEXTO,
            size=24,
            weight=ft.FontWeight.BOLD
        )

        # Sección de valoración
        label_valoracion = ft.Text(
            "Valoración:", 
            color=COLOR_TEXTO, 
            size=14, 
            weight=ft.FontWeight.BOLD
        )
        
        container_valoracion = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text("1", color=COLOR_TEXTO),
                    ft.Text("5", color=COLOR_TEXTO)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                self.valoracion_slider
            ]),
            width=400
        )

        # Campo de reseña
        label_resena = ft.Text(
            "Reseña de la película:", 
            color=COLOR_TEXTO, 
            size=14, 
            weight=ft.FontWeight.BOLD
        )
        
        campo_resena = ft.TextField(
            ref=self.campo_resena_ref,
            bgcolor=COLOR_GRIS_CLARO,
            color=COLOR_FONDO,
            border_radius=10,
            multiline=True,
            min_lines=8,
            max_lines=8,
            width=400,
            border_color=COLOR_GRIS_CLARO,
            content_padding=ft.padding.symmetric(horizontal=15, vertical=10),
        )

        # Botones
        boton_enviar = ft.ElevatedButton(
            "Enviar Reseña",
            bgcolor=COLOR_NARANJA,
            color=COLOR_TEXTO,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
            on_click=self.enviar_resena 
        )

        boton_volver = ft.ElevatedButton(
            "Volver",
            on_click=lambda e: self.volver_callback(self.pelicula) if self.volver_callback else None,
            bgcolor="#555555",
            color=COLOR_TEXTO,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
        )

        self.controls = [
            titulo,
            label_valoracion,
            container_valoracion,
            label_resena,
            campo_resena,
            boton_enviar,
            boton_volver, 
        ]

    def enviar_resena(self, e):
        resena = self.campo_resena_ref.current.value.strip() if self.campo_resena_ref.current else ""
        valoracion = int(self.valoracion_slider.value)

        if not resena:
            self.page.snack_bar.content = ft.Text("Por favor, escribe una reseña")
            self.page.snack_bar.bgcolor = COLOR_NARANJA
            self.page.snack_bar.open = True
            return

        # Obtener el TMDB ID de la película
        tmdb_id = self.pelicula.get("id")
        
        # --- Guardar la reseña en la base de datos ---
        if self.user_id is None:
            self.page.snack_bar.content = ft.Text("Error: No hay usuario autenticado para enviar la reseña.")
            self.page.snack_bar.bgcolor = COLOR_ERROR
            self.page.snack_bar.open = True
            self.page.update()
            return

        if tmdb_id:
            rows_affected = db.add_comentario(self.user_id, tmdb_id, resena, valoracion)
            if rows_affected:
                self.page.snack_bar.content = ft.Text("¡Reseña enviada con éxito!")
                self.page.snack_bar.bgcolor = COLOR_NARANJA
                self.page.snack_bar.open = True
                # Limpiar campos y resetear valoración
                if self.campo_resena_ref.current:
                    self.campo_resena_ref.current.value = ""
                self.valoracion_slider.value = 5
                
            else:
                self.page.snack_bar.content = ft.Text("Error al enviar la reseña. Inténtalo de nuevo.")
                self.page.snack_bar.bgcolor = COLOR_NARANJA
                self.page.snack_bar.open = True
        else:
            self.page.snack_bar.content = ft.Text("No se pudo obtener el ID de la película.")
            self.page.snack_bar.bgcolor = COLOR_NARANJA
            self.page.snack_bar.open = True

        self.page.update()