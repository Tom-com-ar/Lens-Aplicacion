import flet as ft
from services.tmdb_api import TMDBApi

COLOR_NARANJA = "#FF9D00"
COLOR_FONDO = "#000000"
COLOR_TEXTO = "#FFFFFF"
COLOR_GRIS_OSCURO = "#1A1A1A"
COLOR_GRIS_CLARO = "#D9D9D9"
COLOR_SELECCIONANDO = "#FF9D00" 
COLOR_OCUPADO = "#555555" 
COLOR_DISPONIBLE = "#D9D9D9"

class CompraEntradasUI(ft.Column):
    def __init__(self, page: ft.Page, pelicula=None, volver_detalle_callback=None):
        super().__init__(expand=True, scroll="auto", horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        self.page = page
        self.pelicula = pelicula
        self.volver_detalle_callback = volver_detalle_callback
        self.spacing = 40 # Espaciado general
        self.tmdb_api = TMDBApi()

        self.asientos_seleccionados = [] # Lista para almacenar los asientos seleccionados
        self.asientos_seleccionados_text = ft.Text("Asientos seleccionados: Ninguno", color=COLOR_TEXTO, size=14) # Referencia para actualizar el texto

        self.create_layout()

    def create_layout(self):
        # Obtener detalles completos de la película
        detalle = self.tmdb_api.obtener_detalle_pelicula(self.pelicula["id"])
        if not detalle:
            detalle = self.pelicula

        poster_url = f"https://image.tmdb.org/t/p/w500{detalle['poster_path']}" if detalle.get("poster_path") else "https://via.placeholder.com/240x380?text=Sin+Imagen"

        # --- Información de la película (izquierda) ---
        info_pelicula_col = ft.Container(
            content=ft.Column([
                ft.Image(src=poster_url, width=200, height=300, border_radius=15, fit=ft.ImageFit.COVER),
                ft.Text(detalle.get('title', 'Título no disponible'), color=COLOR_TEXTO, size=18, weight=ft.FontWeight.BOLD),
                
                # Géneros
                ft.Container(
                    content=ft.Text(
                        ", ".join([g.get('name', 'Desconocido') for g in detalle.get('genres', []) if g and g.get('name')]) or "Género no disponible",
                        color=COLOR_TEXTO,
                        size=14,
                        weight=ft.FontWeight.BOLD
                    ),
                    margin=ft.margin.only(top=10)
                ),
                
                # Sinopsis
                ft.Container(
                    content=ft.Text(
                        detalle.get("overview", "Sinopsis no disponible"),
                        color=COLOR_TEXTO,
                        size=12,
                        max_lines=10,
                        overflow=ft.TextOverflow.ELLIPSIS
                    ),
                    margin=ft.margin.only(top=10)
                ),
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, width=250, spacing=10),
            bgcolor=COLOR_GRIS_OSCURO,
            border_radius=20,
            padding=20,
            width=300
        )

        # --- Área de selección de asientos (derecha) ---
        pantalla = ft.Container(width=400, height=10, bgcolor=COLOR_GRIS_CLARO, border_radius=5, margin=ft.margin.only(bottom=20))

        # Cuadrícula de asientos
        asientos_grid = ft.Column(spacing=5)
        filas = "ABCDEFGHIJ"
        for i, fila_letra in enumerate(filas):
            fila_asientos = ft.Row(alignment=ft.MainAxisAlignment.CENTER, spacing=5)
            fila_asientos.controls.append(ft.Text(fila_letra, color=COLOR_TEXTO, size=12, weight=ft.FontWeight.BOLD))
            for j in range(1, 11): # 10 asientos por fila
                asiento_id = f"{fila_letra}{j}"
                asiento_container = ft.Container(
                    width=30, height=30,
                    bgcolor=COLOR_DISPONIBLE, 
                    border_radius=5,
                    alignment=ft.alignment.center,
                    data=asiento_id,
                    on_click=self.asiento_click,
                )
                fila_asientos.controls.append(asiento_container)
            asientos_grid.controls.append(fila_asientos)

        area_asientos_col = ft.Container(
            content=ft.Column([
                ft.Text("Butacas", color=COLOR_TEXTO, size=20, weight=ft.FontWeight.BOLD),
                pantalla,
                asientos_grid,

                # Leyenda de asientos
                ft.Row([
                    ft.Container(width=20, height=20, bgcolor=COLOR_DISPONIBLE, border_radius=3),
                    ft.Text("Disponible", color=COLOR_TEXTO, size=12),
                    ft.Container(width=20, height=20, bgcolor=COLOR_SELECCIONANDO, border_radius=3),
                    ft.Text("Seleccionando", color=COLOR_TEXTO, size=12),
                    ft.Container(width=20, height=20, bgcolor=COLOR_OCUPADO, border_radius=3),
                    ft.Text("Ocupado", color=COLOR_TEXTO, size=12),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=15),

                # Asientos seleccionados indicador
                ft.Row([
                    ft.Icon("event_seat", color=COLOR_TEXTO, size=20),
                    self.asientos_seleccionados_text,
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=5),

                # Botones de acción
                ft.Row([
                    ft.ElevatedButton(
                        "Volver",
                        bgcolor=COLOR_GRIS_OSCURO,
                        color=COLOR_TEXTO,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
                        on_click=lambda e: self.volver_detalle_callback(self.pelicula)
                    ),
                    ft.ElevatedButton(
                        "Comprar Entradas",
                        bgcolor=COLOR_NARANJA,
                        color=COLOR_TEXTO,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
                        on_click=self.comprar_entradas_click
                    ),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            ], alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20),
            bgcolor=COLOR_GRIS_OSCURO,
            border_radius=20,
            padding=20,
            width=500
        )

        # Combinar información de película y área de asientos
        main_row = ft.Row([
            info_pelicula_col,
            area_asientos_col,
        ], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.START, spacing=40)

        self.controls = [
            main_row,
        ]

    def asiento_click(self, e):
        asiento_container = e.control
        asiento_id = asiento_container.data

        if asiento_container.bgcolor == COLOR_DISPONIBLE:
            asiento_container.bgcolor = COLOR_SELECCIONANDO
            self.asientos_seleccionados.append(asiento_id)
        elif asiento_container.bgcolor == COLOR_SELECCIONANDO:
            asiento_container.bgcolor = COLOR_DISPONIBLE
            self.asientos_seleccionados.remove(asiento_id)

        if self.asientos_seleccionados:
            self.asientos_seleccionados_text.value = f"Asientos seleccionados: {', '.join(sorted(self.asientos_seleccionados))}"
        else:
            self.asientos_seleccionados_text.value = "Asientos seleccionados: Ninguno"

        self.page.update()

    def comprar_entradas_click(self, e):
        print("Botón Comprar Entradas clicado.")
        print("Asientos seleccionados:", self.asientos_seleccionados)
        self.page.go("/")

