import flet as ft
from services.db import db

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
        self.user_id = user_id
        self.spacing = 40 
        self.asientos_seleccionados = []
        self.asientos_seleccionados_text = ft.Text("Asientos seleccionados: Ninguno", color=COLOR_TEXTO, size=14) 
        self.funcion_seleccionada = None
        self.create_funciones_layout()

    def create_funciones_layout(self):
        self.controls.clear()
        funciones = db.get_funciones_by_pelicula(self.pelicula["id_pelicula"])
        self.controls.append(
            ft.Row([
                ft.Text("Selecciona una función:", color=COLOR_TEXTO, size=20, weight=ft.FontWeight.BOLD),
                ft.ElevatedButton(
                    "Actualizar",
                    bgcolor=COLOR_NARANJA,
                    color=COLOR_TEXTO,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
                    on_click=lambda e: self.create_funciones_layout()
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        )
        if not funciones:
            self.controls.append(ft.Text("no hay funciones disponibles para esta película.", color=COLOR_TEXTO, size=18))
            self.controls.append(ft.ElevatedButton(
                "Volver",
                bgcolor=COLOR_GRIS_OSCURO,
                color=COLOR_TEXTO,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
                on_click=lambda e: self.volver_detalle_callback(self.pelicula)
            ))
            self.page.update()
            return
        lista_funciones = []
        for funcion in funciones:
            texto = f"Sala: {funcion['nombre_sala']} | Fecha y hora: {funcion['fecha_hora']} | Precio: ${funcion['precio']}"
            btn = ft.ElevatedButton(
                texto,
                bgcolor=COLOR_NARANJA,
                color=COLOR_TEXTO,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
                on_click=lambda e, f=funcion: self.seleccionar_funcion(f)
            )
            lista_funciones.append(btn)
        self.controls.append(ft.Column(lista_funciones, spacing=15))
        self.controls.append(ft.ElevatedButton(
            "Volver",
            bgcolor=COLOR_GRIS_OSCURO,
            color=COLOR_TEXTO,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
            on_click=lambda e: self.volver_detalle_callback(self.pelicula)
        ))
        self.page.update()

    def seleccionar_funcion(self, funcion):
        self.funcion_seleccionada = funcion
        self.create_asientos_layout()

    def create_asientos_layout(self):
        self.controls.clear()
        sala = db.get_sala_by_id(self.funcion_seleccionada["id_sala"])
        asientos_ocupados_db = db.get_entradas_ocupadas_by_funcion(self.funcion_seleccionada["id_funcion"])
        self.asientos_ocupados_set = {f"{a['fila']}{a['numero_asiento']}" for a in asientos_ocupados_db} if asientos_ocupados_db else set()
        self.asientos_seleccionados = []
        self.asientos_seleccionados_text = ft.Text("Asientos seleccionados: Ninguno", color=COLOR_TEXTO, size=14)

        info_funcion = ft.Container(
            content=ft.Column([
                ft.Text(f"Sala: {self.funcion_seleccionada['nombre_sala']}", color=COLOR_TEXTO, size=16, weight=ft.FontWeight.BOLD),
                ft.Text(f"Fecha y hora: {self.funcion_seleccionada['fecha_hora']}", color=COLOR_TEXTO, size=14),
                ft.Text(f"Precio: ${self.funcion_seleccionada['precio']}", color=COLOR_TEXTO, size=14),
            ], spacing=5),
            bgcolor=COLOR_GRIS_OSCURO,
            border_radius=15,
            padding=15,
            margin=ft.margin.only(bottom=10)
        )

        pantalla = ft.Container(width=400, height=10, bgcolor=COLOR_GRIS_CLARO, border_radius=5, margin=ft.margin.only(bottom=20))
        asientos_grid_controls = []
        filas = "ABCDEFGHIJ"
        for i, fila_letra in enumerate(filas):
            fila_asientos = ft.Row(alignment=ft.MainAxisAlignment.CENTER, spacing=5)
            fila_asientos.controls.append(ft.Text(fila_letra, color=COLOR_TEXTO, size=12, weight=ft.FontWeight.BOLD))
            for j in range(1, 13):
                asiento_id = f"{fila_letra}{j}"
                initial_bgcolor = COLOR_OCUPADO if asiento_id in self.asientos_ocupados_set else COLOR_DISPONIBLE
                asiento_container = ft.Container(
                    width=30, height=30,
                    bgcolor=initial_bgcolor, 
                    border_radius=5,
                    alignment=ft.alignment.center,
                    data=asiento_id,
                    on_click=self.asiento_click,
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
                ft.Row([
                    ft.Container(width=20, height=20, bgcolor=COLOR_DISPONIBLE, border_radius=3),
                    ft.Text("Disponible", color=COLOR_TEXTO, size=12),
                    ft.Container(width=20, height=20, bgcolor=COLOR_SELECCIONANDO, border_radius=3),
                    ft.Text("Seleccionando", color=COLOR_TEXTO, size=12),
                    ft.Container(width=20, height=20, bgcolor=COLOR_OCUPADO, border_radius=3),
                    ft.Text("Ocupado", color=COLOR_TEXTO, size=12),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=15),
                ft.Row([
                    ft.Icon("event_seat", color=COLOR_TEXTO, size=20),
                    self.asientos_seleccionados_text,
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=5),
                ft.Row([
                    ft.ElevatedButton(
                        "Volver a funciones",
                        bgcolor=COLOR_GRIS_OSCURO,
                        color=COLOR_TEXTO,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
                        on_click=lambda e: self.create_funciones_layout()
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

        main_row = ft.Row([
            info_funcion,
            area_asientos_col,
        ], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.START, spacing=40)
        self.controls = [main_row]
        self.page.update()

    def asiento_click(self, e):
        asiento_container = e.control
        asiento_id = asiento_container.data
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
        if self.user_id is None:
            self.page.snack_bar.content = ft.Text("Error: No hay usuario autenticado para comprar entradas.")
            self.page.snack_bar.bgcolor = COLOR_ERROR
            self.page.snack_bar.open = True
            self.page.update()
            return
        compra_exitosa = True
        for asiento_id in self.asientos_seleccionados:
            fila = asiento_id[0]
            numero_asiento = int(asiento_id[1:])
            rows_affected = db.add_entrada_funcion(self.user_id, self.funcion_seleccionada["id_funcion"], fila, numero_asiento)
            if not rows_affected:
                compra_exitosa = False
                break
        if compra_exitosa:
            self.page.snack_bar.content = ft.Text("¡Entradas compradas con éxito!")
            self.page.snack_bar.bgcolor = COLOR_NARANJA
            self.page.snack_bar.open = True
            self.asientos_seleccionados.clear()
            self.asientos_seleccionados_text.value = "Asientos seleccionados: Ninguno"
            self.create_asientos_layout()
        else:
            self.page.snack_bar.content = ft.Text("Error al procesar la compra. Inténtalo de nuevo.")
            self.page.snack_bar.bgcolor = COLOR_NARANJA
            self.page.snack_bar.open = True
        self.page.update()

