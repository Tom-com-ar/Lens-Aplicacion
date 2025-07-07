import flet as ft
from services.db import db

COLOR_NARANJA = "#FF9D00"
COLOR_FONDO = "#000000"
COLOR_TEXTO = "#FFFFFF"
COLOR_SOMBRA = "#00000022"

class CatalogoContent(ft.Column):
    def __init__(self, page: ft.Page, mostrar_detalle_callback):
        super().__init__()
        self.page = page
        self.mostrar_detalle_callback = mostrar_detalle_callback

        self.detalle_cache = {}

        self.filtros_activos = {
            "generos": [],
            "duracion_desde": 0,
            "duracion_hasta": 240,
            "año_desde": None,
            "año_hasta": None
        }

        self.duracion_min = 0
        self.duracion_max = 240
        self.texto_rango = ft.Text(
            f"Duración: {self.filtros_activos['duracion_desde']} - {self.filtros_activos['duracion_hasta']} minutos",
            color=COLOR_TEXTO,
            size=12
        )

        self.crear_dialogo_filtros()

        self.titulo_filtros = ft.Container(
            content=ft.Row([
                ft.Text("Películas", color=COLOR_TEXTO, size=22, weight=ft.FontWeight.BOLD),
                ft.Container(expand=1),
                ft.ElevatedButton(
                    "Actualizar",
                    bgcolor=COLOR_NARANJA,
                    color=COLOR_TEXTO,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
                    on_click=self.actualizar_catalogo
                ),
                ft.Container(width=20),
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

        self.mensaje_no_resultados = ft.Text(
            "No se encontraron películas con los filtros aplicados.",
            color=COLOR_TEXTO,
            size=18,
            visible=False
        )

        self.grilla = ft.GridView(
            expand=True,
            runs_count=10,
            max_extent=180,
            child_aspect_ratio=0.6,
            spacing=10,
            run_spacing=10,
        )

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

        self.page.overlay.append(self.dialogo_filtros)
        self.cargar_peliculas()

    def mostrar_filtros(self, e):
        self.page.dialog = self.dialogo_filtros
        self.dialogo_filtros.open = True
        self.page.update()

    def toggle_genero(self, genero, seleccionado):
        if seleccionado:
            self.filtros_activos["generos"].append(genero)
        else:
            self.filtros_activos["generos"].remove(genero)

    def actualizar_filtro(self, filtro, valor):
        if valor:
            try:
                self.filtros_activos[filtro] = int(valor)
            except ValueError:
                self.filtros_activos[filtro] = None
        else:
            self.filtros_activos[filtro] = None

    def actualizar_rango_duracion(self, e):
        self.filtros_activos["duracion_desde"] = int(e.control.start_value)
        self.filtros_activos["duracion_hasta"] = int(e.control.end_value)
        self.texto_rango.value = f"Duración: {int(e.control.start_value)} - {int(e.control.end_value)} minutos"
        self.texto_rango.update()

    def crear_dialogo_filtros(self):
        # Obtener todos los géneros únicos de la base de datos
        peliculas = db.get_peliculas() or []
        generos_unicos = set()
        for peli in peliculas:
            if peli.get("genero"):
                for g in peli["genero"].split(","):
                    if g.strip():
                        generos_unicos.add(g.strip())
        if not generos_unicos:
            self.checkboxes_generos = [
                ft.Checkbox(label="Sin géneros disponibles", value=False, disabled=True)
            ]
        else:
            self.checkboxes_generos = [
                ft.Checkbox(label=genero, value=False,
                    on_change=lambda e, g=genero: self.toggle_genero(g, e.control.value))
                for genero in sorted(generos_unicos)
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
            "duracion_desde": 0,
            "duracion_hasta": 240,
            "año_desde": None,
            "año_hasta": None
        }
        for cb in self.checkboxes_generos:
            cb.value = False
        self.textfield_ano_desde.value = ""
        self.textfield_ano_hasta.value = ""
        self.slider_duracion.start_value = 0
        self.slider_duracion.end_value = 240
        self.texto_rango.value = "Duración: 0 - 240 minutos"
        self.texto_rango.update()
        self.page.update()
        self.cargar_peliculas()

    def aplicar_filtros(self, e):
        self.cargar_peliculas()
        self.dialogo_filtros.open = False
        self.page.update()

    def filtrar_peliculas(self, peliculas):
        filtradas = []
        for peli in peliculas:
            # Filtro por género
            if self.filtros_activos["generos"]:
                peli_generos = [g.strip() for g in (peli["genero"] or "").split(",")]
                if not any(g in peli_generos for g in self.filtros_activos["generos"]):
                    continue
            # Filtro por año
            if self.filtros_activos["año_desde"] and (peli["fecha_estreno"] is not None) and int(peli["fecha_estreno"]) < self.filtros_activos["año_desde"]:
                continue
            if self.filtros_activos["año_hasta"] and (peli["fecha_estreno"] is not None) and int(peli["fecha_estreno"]) > self.filtros_activos["año_hasta"]:
                continue
            # Filtro por duración
            if peli["duracion"] is not None:
                if peli["duracion"] < self.filtros_activos["duracion_desde"] or peli["duracion"] > self.filtros_activos["duracion_hasta"]:
                    continue
            filtradas.append(peli)
        return filtradas

    def mostrar_peliculas(self, peliculas):
        self.grilla.controls.clear()
        if not peliculas:
            self.mensaje_no_resultados.visible = True
            self.page.update()
            return
        self.mensaje_no_resultados.visible = False
        for peli in peliculas:
            portada = peli["imagen_portada"] or "https://via.placeholder.com/180x300?text=Sin+Imagen"
            duracion = f"{peli['duracion']} min" if peli["duracion"] else "-"
            tarjeta = ft.Container(
                content=ft.Column([
                    ft.Image(src=portada, width=180, height=270, border_radius=15, fit=ft.ImageFit.COVER),
                ], alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
                border_radius=15,
                on_click=lambda e, peli=peli: self.mostrar_detalle_callback(peli),
            )
            self.grilla.controls.append(tarjeta)
        self.page.update()

    def cargar_peliculas(self):
        peliculas = db.get_peliculas() or []
        # Calcular valoración promedio para cada película
        for peli in peliculas:
            comentarios = db.get_comentarios_by_pelicula(peli["id_pelicula"])
            if comentarios:
                promedio = sum([c["valoracion"] for c in comentarios]) / len(comentarios)
                peli["valoracion_promedio"] = promedio
            else:
                peli["valoracion_promedio"] = 0
        # Ordenar por valoración promedio descendente
        peliculas.sort(key=lambda x: x["valoracion_promedio"], reverse=True)
        peliculas_filtradas = self.filtrar_peliculas(peliculas)
        self.mostrar_peliculas(peliculas_filtradas)

    def buscar_peliculas(self, query):
        peliculas = db.get_peliculas() or []
        query_lower = query.lower()
        peliculas_filtradas = [
            p for p in peliculas
            if query_lower in (p.get("titulo", "") or "").lower() or query_lower in (p.get("descripcion", "") or "").lower()
        ]
        peliculas_filtradas = self.filtrar_peliculas(peliculas_filtradas)
        self.mostrar_peliculas(peliculas_filtradas)

    def actualizar_catalogo(self, e=None):
        self.crear_dialogo_filtros()
        self.cargar_peliculas()
        self.page.update()