import flet as ft
from services.tmdb_api import TMDBApi
from services.db import db # Importar la instancia de la base de datos

COLOR_NARANJA = "#FF9D00"
COLOR_FONDO = "#000000"
COLOR_TEXTO = "#FFFFFF"
COLOR_GRIS_OSCURO = "#1A1A1A"
COLOR_GRIS_CLARO = "#D9D9D9"
COLOR_SELECCIONANDO = "#FF9D00" 
COLOR_OCUPADO = "#555555" 
COLOR_DISPONIBLE = "#D9D9D9"
COLOR_ERROR = "#FF0000"

class CompraEntradasUI(ft.Column):
    def __init__(self, page: ft.Page, pelicula=None, volver_detalle_callback=None, user_id=None):
        super().__init__(expand=True, scroll="auto", horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        self.page = page
        self.pelicula = pelicula
        self.volver_detalle_callback = volver_detalle_callback
        self.user_id = user_id # Almacenar el ID del usuario
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

        # --- Obtener asientos ocupados de la base de datos ---
        tmdb_id = self.pelicula["id"]
        asientos_ocupados_db = db.get_entradas_ocupadas_by_tmdb_id(tmdb_id)
        # Convertir la lista de diccionarios a un set de strings para fácil búsqueda
        self.asientos_ocupados_set = {f"{a['fila']}{a['numero_asiento']}" for a in asientos_ocupados_db} if asientos_ocupados_db else set()

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
        asientos_grid_controls = []
        filas = "ABCDEFGHIJ"
        for i, fila_letra in enumerate(filas):
            fila_asientos = ft.Row(alignment=ft.MainAxisAlignment.CENTER, spacing=5)
            fila_asientos.controls.append(ft.Text(fila_letra, color=COLOR_TEXTO, size=12, weight=ft.FontWeight.BOLD))
            for j in range(1, 13): # 10 asientos por fila
                asiento_id = f"{fila_letra}{j}"
                
                # Determinar el color inicial del asiento
                initial_bgcolor = COLOR_OCUPADO if asiento_id in self.asientos_ocupados_set else COLOR_DISPONIBLE
                
                asiento_container = ft.Container(
                    width=30, height=30,
                    bgcolor=initial_bgcolor, 
                    border_radius=5,
                    alignment=ft.alignment.center,
                    data=asiento_id,
                    on_click=self.asiento_click,
                    # Deshabilitar click si el asiento está ocupado
                    disabled=asiento_id in self.asientos_ocupados_set
                )
                fila_asientos.controls.append(asiento_container)
            asientos_grid_controls.append(fila_asientos)
        
        asientos_grid = ft.Column(spacing=5, controls=asientos_grid_controls)

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

        # Evitar seleccionar asientos ya ocupados
        if asiento_id in self.asientos_ocupados_set:
            return

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
        if not self.asientos_seleccionados:
            self.page.snack_bar.content = ft.Text("Por favor, selecciona al menos un asiento.")
            self.page.snack_bar.bgcolor = COLOR_NARANJA
            self.page.snack_bar.open = True
            self.page.update()
            return

        tmdb_id = self.pelicula["id"]
        # Usar el id_usuario real recibido
        if self.user_id is None:
            self.page.snack_bar.content = ft.Text("Error: No hay usuario autenticado para comprar entradas.")
            self.page.snack_bar.bgcolor = COLOR_ERROR # Define COLOR_ERROR si no existe
            self.page.snack_bar.open = True
            self.page.update()
            return

        compra_exitosa = True

        for asiento_id in self.asientos_seleccionados:
            fila = asiento_id[0] # Primera letra es la fila
            numero_asiento = int(asiento_id[1:]) # Resto es el número de asiento
            
            rows_affected = db.add_entrada(self.user_id, tmdb_id, fila, numero_asiento)
            if not rows_affected:
                compra_exitosa = False
                break

        if compra_exitosa:
            self.page.snack_bar.content = ft.Text("¡Entradas compradas con éxito!")
            self.page.snack_bar.bgcolor = COLOR_NARANJA
            self.page.snack_bar.open = True
            # Limpiar selección y recargar asientos para mostrar los ocupados
            self.asientos_seleccionados.clear()
            self.asientos_seleccionados_text.value = "Asientos seleccionados: Ninguno"
            self.create_layout() # Volver a crear el layout para actualizar asientos ocupados
        else:
            self.page.snack_bar.content = ft.Text("Error al procesar la compra. Inténtalo de nuevo.")
            self.page.snack_bar.bgcolor = COLOR_NARANJA
            self.page.snack_bar.open = True
        self.page.update()

        # self.page.go("/") # Quitar esto, la navegación se manejará después de la compra

