import flet as ft

COLOR_NARANJA = "#FF9D00"
COLOR_FONDO = "#000000"
COLOR_TEXTO = "#FFFFFF"
COLOR_GRIS_CLARO = "#D9D9D9"

class ComentariosUI(ft.Column):
    def __init__(self, page: ft.Page, pelicula=None, volver_callback=None):
        super().__init__(expand=True, scroll="auto", horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        self.page = page
        self.pelicula = pelicula
        self.volver_callback = volver_callback # Guardar el callback para volver
        self.spacing = 20 # Espaciado entre elementos

        # Referencias a los campos de entrada para acceder a sus valores después
        self.campo_nombre_ref = ft.Ref[ft.TextField]()
        self.campo_resena_ref = ft.Ref[ft.TextField]()

        self.create_widgets()

    def create_widgets(self):
        # Título
        titulo = ft.Text(
            f"Deja tu reseña para: {self.pelicula.get('title', 'Película desconocida')}",
            color=COLOR_TEXTO,
            size=24,
            weight=ft.FontWeight.BOLD
        )

        # Campo de nombre
        label_nombre = ft.Text("Nombre de la persona:", color=COLOR_TEXTO, size=14, weight=ft.FontWeight.BOLD)
        campo_nombre = ft.TextField(
            ref=self.campo_nombre_ref,
            bgcolor=COLOR_GRIS_CLARO,
            color=COLOR_FONDO, # Color del texto de entrada (negro)
            border_radius=10,
            width=400,
            border_color=COLOR_GRIS_CLARO,
            content_padding=ft.padding.symmetric(horizontal=15, vertical=10),
            height=40, # Ajustar altura
        )

        # Campo de reseña
        label_resena = ft.Text("Reseña de la pelicula:", color=COLOR_TEXTO, size=14, weight=ft.FontWeight.BOLD)
        campo_resena = ft.TextField(
            ref=self.campo_resena_ref,
            bgcolor=COLOR_GRIS_CLARO,
            color=COLOR_FONDO,
            border_radius=10,
            multiline=True, # Permite múltiples líneas
            min_lines=8, # Aumentar tamaño
            max_lines=8,
            width=400,
            border_color=COLOR_GRIS_CLARO,
            content_padding=ft.padding.symmetric(horizontal=15, vertical=10),
        )

        # Botón para enviar reseña
        boton_enviar = ft.ElevatedButton(
            "Enviar Reseña",
            bgcolor=COLOR_NARANJA,
            color=COLOR_TEXTO,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
            on_click=self.enviar_resena 
        )

        # Botón para volver
        boton_volver = ft.ElevatedButton(
            "Volver",
            on_click=lambda e: self.volver_callback(self.pelicula) if self.volver_callback else None,
            bgcolor="#555555", # Color gris oscuro para el botón de volver
            color=COLOR_TEXTO,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
        )

        self.controls = [
            titulo,
            label_nombre,
            campo_nombre,
            label_resena,
            campo_resena,
            boton_enviar,
            boton_volver, 
        ]

    def enviar_resena(self, e):
        # Obtener los valores de los campos
        nombre = self.campo_nombre_ref.current.value.strip() if self.campo_nombre_ref.current else ""
        resena = self.campo_resena_ref.current.value.strip() if self.campo_resena_ref.current else ""

        # Validar que los campos no estén vacíos
        if not nombre or not resena:
            # Mostrar mensaje de error
            self.page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text("Por favor, completa todos los campos"),
                    bgcolor=COLOR_NARANJA
                )
            )
            return

        # Aquí iría la lógica para guardar la reseña
        # Por ahora solo mostramos un mensaje de éxito
        self.page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text("¡Reseña enviada con éxito!"),
                bgcolor=COLOR_NARANJA
            )
        )

        # Limpiar los campos
        if self.campo_nombre_ref.current:
            self.campo_nombre_ref.current.value = ""
        if self.campo_resena_ref.current:
            self.campo_resena_ref.current.value = ""

        # Actualizar la página
        self.page.update()