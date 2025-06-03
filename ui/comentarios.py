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
        self.volver_callback = volver_callback
        self.spacing = 20

        # Referencia solo para el campo de reseña
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
            self.page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text("Por favor, escribe una reseña"),
                    bgcolor=COLOR_NARANJA
                )
            )
            return

        # Aquí iría la lógica para guardar la reseña con la valoración
        self.page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text("¡Reseña enviada con éxito!"),
                bgcolor=COLOR_NARANJA
            )
        )

        # Limpiar campos y resetear valoración
        if self.campo_resena_ref.current:
            self.campo_resena_ref.current.value = ""
        self.valoracion_slider.value = 5

        # Actualizar la página
        self.page.update()