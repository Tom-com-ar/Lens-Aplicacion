import flet as ft
from services.tmdb_api import TMDBApi

COLOR_NARANJA = "#FF9D00"
COLOR_FONDO = "#000000"
COLOR_TEXTO = "#FFFFFF"
COLOR_SOMBRA = "#00000022"

class CatalogoContent(ft.Column): # Cambiado a Content para evitar confusión con Vista completa
    def __init__(self, page: ft.Page, tmdb_api: TMDBApi, mostrar_detalle_callback):
        super().__init__(expand=True, scroll="auto")
        self.page = page
        self.tmdb_api = tmdb_api
        self.mostrar_detalle_callback = mostrar_detalle_callback
        self.spacing = 0
        self.peliculas_catalogo = []  # Lista para almacenar todas las películas
        self.filtros_activos = {
            "generos": [],
            "año_desde": None,
            "año_hasta": None,
            "duracion_desde": None,
            "duracion_hasta": None
        }

        # --- Diálogo de filtros ---
        self.dialogo_filtros = ft.AlertDialog(
            title=ft.Text("Filtros", color=COLOR_TEXTO),
            content=ft.Column([
                ft.Text("Géneros", color=COLOR_TEXTO, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=ft.Column(
                        [ft.Checkbox(label=genero["name"], value=False, 
                                   on_change=lambda e, g=genero: self.toggle_genero(g, e.control.value))
                         for genero in self.tmdb_api.generos],
                        scroll=ft.ScrollMode.AUTO,
                        height=200
                    ),
                    padding=10
                ),
                ft.Divider(color=COLOR_NARANJA),
                ft.Text("Año de estreno", color=COLOR_TEXTO, weight=ft.FontWeight.BOLD),
                ft.Row([
                    ft.TextField(
                        label="Desde",
                        width=100,
                        bgcolor=COLOR_FONDO,
                        border_color=COLOR_NARANJA,
                        color=COLOR_TEXTO,
                        on_change=lambda e: self.actualizar_filtro("año_desde", e.control.value)
                    ),
                    ft.TextField(
                        label="Hasta",
                        width=100,
                        bgcolor=COLOR_FONDO,
                        border_color=COLOR_NARANJA,
                        color=COLOR_TEXTO,
                        on_change=lambda e: self.actualizar_filtro("año_hasta", e.control.value)
                    ),
                ]),
                ft.Divider(color=COLOR_NARANJA),
                ft.Text("Duración (minutos)", color=COLOR_TEXTO, weight=ft.FontWeight.BOLD),
                ft.Row([
                    ft.TextField(
                        label="Desde",
                        width=100,
                        bgcolor=COLOR_FONDO,
                        border_color=COLOR_NARANJA,
                        color=COLOR_TEXTO,
                        on_change=lambda e: self.actualizar_filtro("duracion_desde", e.control.value)
                    ),
                    ft.TextField(
                        label="Hasta",
                        width=100,
                        bgcolor=COLOR_FONDO,
                        border_color=COLOR_NARANJA,
                        color=COLOR_TEXTO,
                        on_change=lambda e: self.actualizar_filtro("duracion_hasta", e.control.value)
                    ),
                ]),
            ], spacing=20),
            actions=[
                ft.TextButton("Limpiar", on_click=self.limpiar_filtros),
                ft.TextButton("Aplicar", on_click=self.aplicar_filtros),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor=COLOR_FONDO,
        )

        # --- Título y botón de filtros ---
        self.titulo_filtros = ft.Container(
            content=ft.Row([
                ft.Text("Películas", color=COLOR_TEXTO, size=22, weight=ft.FontWeight.BOLD),
                ft.Container(expand=1),
                ft.ElevatedButton(
                    "Filtros",
                    icon="arrow_drop_down",
                    bgcolor=COLOR_FONDO,
                    color=COLOR_TEXTO,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
                    height=44,
                    on_click=self.mostrar_filtros
                ),
                ft.Container(width=30),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            margin=ft.margin.only(top=10, bottom=10, left=10, right=10)
        )

        # --- Mensaje de no resultados ---
        self.mensaje_no_resultados = ft.Text(
            "No se encontraron películas con los filtros aplicados.",
            color=COLOR_TEXTO,
            size=18,
            visible=False # Inicialmente oculto
        )

        # --- Grilla de tarjetas con 6 columnas fijas ---
        self.grilla = ft.GridView(
            expand=True,
            runs_count=6,  # SIEMPRE 6 COLUMNAS
            max_extent=180,  # Ancho máximo de cada tarjeta
            child_aspect_ratio=0.6,  # Relación ancho/alto
            spacing=10,
            run_spacing=10,
        )

        # Contenedor principal de este contenido (para centrar la grilla y título/filtros)
        self.controls = [
            ft.Container(
                content=ft.Column([
                    self.titulo_filtros,
                    self.mensaje_no_resultados,
                    self.grilla
                ], alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True),
                alignment=ft.alignment.center,
                padding=ft.padding.all(20),
                bgcolor=COLOR_FONDO, # El fondo del contenido
                border_radius=0,
                margin=ft.margin.all(0),
                expand=True,
            )
        ]

        # --- Añadir el diálogo a la página ---
        self.page.overlay.append(self.dialogo_filtros)

        # --- Cargar películas iniciales ---
        self.cargar_peliculas()

    def mostrar_filtros(self, e):
        self.page.dialog = self.dialogo_filtros
        self.dialogo_filtros.open = True
        self.page.update()

    def toggle_genero(self, genero, seleccionado):
        if seleccionado:
            self.filtros_activos["generos"].append(genero["id"])
        else:
            self.filtros_activos["generos"].remove(genero["id"])

    def actualizar_filtro(self, filtro, valor):
        if valor:
            try:
                self.filtros_activos[filtro] = int(valor)
            except ValueError:
                self.filtros_activos[filtro] = None
        else:
            self.filtros_activos[filtro] = None

    def limpiar_filtros(self, e):
        self.filtros_activos = {
            "generos": [],
            "año_desde": None,
            "año_hasta": None,
            "duracion_desde": None,
            "duracion_hasta": None
        }
        # Resetear checkboxes
        for control in self.dialogo_filtros.content.controls[1].content.controls:
            if isinstance(control, ft.Checkbox):
                control.value = False
        # Resetear campos de texto
        for control in self.dialogo_filtros.content.controls:
            if isinstance(control, ft.Row):
                for text_field in control.controls:
                    if isinstance(text_field, ft.TextField):
                        text_field.value = ""
        self.aplicar_filtros(e)

    def aplicar_filtros(self, e):
        self.dialogo_filtros.open = False
        self.filtrar_peliculas()
        self.page.update()

    def filtrar_peliculas(self):
        peliculas_filtradas = self.peliculas_catalogo.copy()

        # Filtrar por géneros
        if self.filtros_activos["generos"]:
            peliculas_filtradas = [
                p for p in peliculas_filtradas
                if any(genero_id in p.get("genre_ids", []) for genero_id in self.filtros_activos["generos"])
            ]

        # Filtrar por año
        if self.filtros_activos["año_desde"] or self.filtros_activos["año_hasta"]:
            peliculas_filtradas = [
                p for p in peliculas_filtradas
                if self.filtros_activos["año_desde"] is None or 
                   int(p.get("release_date", "0")[:4]) >= self.filtros_activos["año_desde"]
            ]
            peliculas_filtradas = [
                p for p in peliculas_filtradas
                if self.filtros_activos["año_hasta"] is None or 
                   int(p.get("release_date", "0")[:4]) <= self.filtros_activos["año_hasta"]
            ]

        # Filtrar por duración
        if self.filtros_activos["duracion_desde"] or self.filtros_activos["duracion_hasta"]:
            for pelicula in peliculas_filtradas:
                detalle = self.tmdb_api.obtener_detalle_pelicula(pelicula["id"])
                if detalle:
                    duracion = detalle.get("runtime", 0)
                    pelicula["runtime"] = duracion

            peliculas_filtradas = [
                p for p in peliculas_filtradas
                if self.filtros_activos["duracion_desde"] is None or 
                   p.get("runtime", 0) >= self.filtros_activos["duracion_desde"]
            ]
            peliculas_filtradas = [
                p for p in peliculas_filtradas
                if self.filtros_activos["duracion_hasta"] is None or 
                   p.get("runtime", 0) <= self.filtros_activos["duracion_hasta"]
            ]

        self.mostrar_peliculas(peliculas_filtradas)
        self.actualizar_visibilidad()

    def mostrar_peliculas(self, peliculas):
        tarjetas = []
        for peli in peliculas:
            poster_url = (
                f"https://image.tmdb.org/t/p/w500{peli['poster_path']}"
                if peli.get("poster_path") else "https://via.placeholder.com/140x200?text=Sin+Imagen"
            )
            tarjetas.append(
                ft.GestureDetector(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Image(src=poster_url, width=140, height=200, border_radius=18, fit=ft.ImageFit.COVER),
                            ft.Text(
                                peli["title"],
                                color=COLOR_TEXTO,
                                size=13,
                                weight=ft.FontWeight.BOLD,
                                text_align=ft.TextAlign.CENTER,
                                max_lines=2,
                                overflow=ft.TextOverflow.ELLIPSIS
                            ),
                        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        bgcolor=COLOR_FONDO,
                        border_radius=22,
                        padding=ft.padding.all(0),
                        margin=ft.margin.all(16),
                        width=150,
                        height=250,
                        shadow=ft.BoxShadow(blur_radius=16, color=COLOR_SOMBRA, offset=ft.Offset(2, 4)),
                    ),
                    on_tap=lambda e, peli=peli: self.mostrar_detalle_callback(peli)
                )
            )
        self.grilla.controls = tarjetas
        self.page.update()

    def actualizar_visibilidad(self):
        if not self.grilla.controls:
            self.mensaje_no_resultados.visible = True
            self.grilla.visible = False
        else:
            self.mensaje_no_resultados.visible = False
            self.grilla.visible = True

    def cargar_peliculas(self):
        self.peliculas_catalogo = self.tmdb_api.obtener_peliculas_populares()
        self.mostrar_peliculas(self.peliculas_catalogo)