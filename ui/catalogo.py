import flet as ft
from services.tmdb_api import TMDBApi

COLOR_NARANJA = "#FF9D00"
COLOR_FONDO = "#000000"
COLOR_TEXTO = "#FFFFFF"
COLOR_SOMBRA = "#00000022"

class CatalogoContent(ft.Column):
    def __init__(self, page: ft.Page, tmdb_api: TMDBApi, mostrar_detalle_callback):
        super().__init__()
        self.page = page
        self.tmdb_api = tmdb_api
        self.mostrar_detalle_callback = mostrar_detalle_callback

        self.detalle_cache = {}  # <-- Agrega esto

        # filtros_activos
        self.filtros_activos = {
            "generos": [],
            "duracion_desde": 0,
            "duracion_hasta": 240,
            "año_desde": None,
            "año_hasta": None
        }

        # Variables para el rango de duración
        self.duracion_min = 0
        self.duracion_max = 240
        
        # Texto para mostrar el rango seleccionado
        self.texto_rango = ft.Text(
            f"Duración: {self.filtros_activos['duracion_desde']} - {self.filtros_activos['duracion_hasta']} minutos",
            color=COLOR_TEXTO,
            size=12
        )

        # Modificar el diálogo de filtros
        self.crear_dialogo_filtros()

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
            visible=False 
        )

        # --- Grilla de tarjetas con 6 columnas fijas ---
        self.grilla = ft.GridView(
            expand=True,
            runs_count=10,  
            max_extent=180,  
            child_aspect_ratio=0.6,  
            spacing=10,
            run_spacing=10,
        )

        # Contenedor principal de este contenido
        self.controls = [
            ft.Container(
                content=ft.Column([
                    self.titulo_filtros,
                    self.mensaje_no_resultados,
                    self.grilla
                ], alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True),
                alignment=ft.alignment.center,
                padding=ft.padding.all(20),
                bgcolor=COLOR_FONDO,
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

    def actualizar_rango_duracion(self, e):
        """Actualiza los filtros con el nuevo rango de duración"""
        self.filtros_activos["duracion_desde"] = int(e.control.start_value)
        self.filtros_activos["duracion_hasta"] = int(e.control.end_value)
        self.texto_rango.value = f"Duración: {int(e.control.start_value)} - {int(e.control.end_value)} minutos"
        self.texto_rango.update()

    def crear_dialogo_filtros(self):
        self.checkboxes_generos = [
            ft.Checkbox(label=genero["name"], value=False, 
                on_change=lambda e, g=genero: self.toggle_genero(g, e.control.value))
            for genero in self.tmdb_api.generos
        ]
        self.textfield_ano_desde = ft.TextField(
            label="Desde",
            width=100,
            bgcolor=COLOR_FONDO,
            border_color=COLOR_NARANJA,
            color=COLOR_TEXTO,
            on_change=lambda e: self.actualizar_filtro("año_desde", e.control.value)
        )
        self.textfield_ano_hasta = ft.TextField(
            label="Hasta",
            width=100,
            bgcolor=COLOR_FONDO,
            border_color=COLOR_NARANJA,
            color=COLOR_TEXTO,
            on_change=lambda e: self.actualizar_filtro("año_hasta", e.control.value)
        )
        self.slider_duracion = ft.RangeSlider(
            min=0,
            max=240,
            start_value=0,
            end_value=240,
            divisions=12,
            label="{value}",
            active_color=COLOR_NARANJA,
            inactive_color=COLOR_FONDO,
            on_change=self.actualizar_rango_duracion
        )

        self.dialogo_filtros = ft.AlertDialog(
            title=ft.Text("Filtros", color=COLOR_TEXTO),
            content=ft.Column([
                ft.Text("Géneros", color=COLOR_TEXTO, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=ft.Column(
                        self.checkboxes_generos,
                        scroll=ft.ScrollMode.AUTO,
                        height=200
                    ),
                    padding=10
                ),
                ft.Divider(color=COLOR_NARANJA),
                ft.Text("Año de estreno", color=COLOR_TEXTO, weight=ft.FontWeight.BOLD),
                ft.Row([
                    self.textfield_ano_desde,
                    self.textfield_ano_hasta,
                ]),
                ft.Divider(color=COLOR_NARANJA),
                ft.Text("Duración (minutos)", color=COLOR_TEXTO, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=ft.Column([
                        self.slider_duracion,
                        self.texto_rango
                    ]),
                    padding=10
                ),
            ], spacing=20),
            actions=[
                ft.TextButton("Limpiar", on_click=self.limpiar_filtros),
                ft.TextButton("Aplicar", on_click=self.aplicar_filtros),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor=COLOR_FONDO,
        )

    def limpiar_filtros(self, e=None):
        self.filtros_activos = {
            "generos": [],
            "año_desde": None,
            "año_hasta": None,
            "duracion_desde": 0,
            "duracion_hasta": 240
        }
        # Limpiar checkboxes
        for cb in self.checkboxes_generos:
            cb.value = False
            cb.update()
        # Limpiar campos de año
        self.textfield_ano_desde.value = ""
        self.textfield_ano_desde.update()
        self.textfield_ano_hasta.value = ""
        self.textfield_ano_hasta.update()
        # Limpiar slider de duración
        self.slider_duracion.start_value = 0
        self.slider_duracion.end_value = 240
        self.slider_duracion.update()
        # Limpiar texto de rango
        self.texto_rango.value = "Duración: 0 - 240 minutos"
        self.texto_rango.update()
        # Mostrar todas las películas
        self.filtrar_por_texto("")
        self.page.update()

    def aplicar_filtros(self, e):
        """Aplica los filtros y cierra el diálogo"""
        print("\n=== DEBUG: Aplicando filtros ===")
        print(f"Filtros activos: {self.filtros_activos}")
        
        self.dialogo_filtros.open = False
        self.filtrar_peliculas()
        self.page.update()

    def filtrar_por_texto(self, query):
        self.query_busqueda = query
        self.filtrar_peliculas(query) 
        self.page.update()

    def filtrar_peliculas(self, query=""):
        print("\n=== DEBUG: Iniciando filtrado de películas ===")
        
        peliculas_filtradas = self.peliculas_catalogo.copy()
        

        # Filtrar por géneros
        if self.filtros_activos["generos"]:
            print(f"Filtrando por géneros: {self.filtros_activos['generos']}")
            peliculas_filtradas = [
                p for p in peliculas_filtradas
                if any(genero_id in p.get("genre_ids", []) 
                      for genero_id in self.filtros_activos["generos"])
            ]
            print(f"Después de filtrar por géneros: {len(peliculas_filtradas)} películas")

        # Filtrar por año
        año_desde = self.filtros_activos["año_desde"]
        año_hasta = self.filtros_activos["año_hasta"]
        
        if año_desde or año_hasta:
            print(f"Filtrando por año: {año_desde} - {año_hasta}")
            peliculas_filtradas = [
                p for p in peliculas_filtradas
                if (not año_desde or int(p.get("release_date", "0")[:4]) >= año_desde) and
                   (not año_hasta or int(p.get("release_date", "0")[:4]) <= año_hasta)
            ]
            print(f"Después de filtrar por año: {len(peliculas_filtradas)} películas")

        # Obtener duración de las películas filtradas
        duracion_desde = self.filtros_activos["duracion_desde"]
        duracion_hasta = self.filtros_activos["duracion_hasta"]
        
        if duracion_desde > 0 or duracion_hasta < 240:
            print(f"Filtrando por duración: {duracion_desde} - {duracion_hasta}")
            for pelicula in peliculas_filtradas:
                if "runtime" not in pelicula:
                    if pelicula["id"] in self.detalle_cache:
                        pelicula["runtime"] = self.detalle_cache[pelicula["id"]]
                    else:
                        detalle = self.tmdb_api.obtener_detalle_pelicula(pelicula["id"])
                        runtime = detalle.get("runtime", 0) if detalle else 0
                        pelicula["runtime"] = runtime
                        self.detalle_cache[pelicula["id"]] = runtime

            peliculas_filtradas = [
                p for p in peliculas_filtradas
                if duracion_desde <= p.get("runtime", 0) <= duracion_hasta
            ]
            print(f"Después de filtrar por duración: {len(peliculas_filtradas)} películas")

        # Mostrar resultados
        print(f"Total de películas filtradas: {len(peliculas_filtradas)}")
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
        self.peliculas_catalizadas = self.peliculas_catalogo.copy() 
        self.mostrar_peliculas(self.peliculas_catalogo)
        self.query_busqueda = ""