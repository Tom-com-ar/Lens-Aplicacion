import flet as ft
from services.db import db

COLOR_NARANJA = "#FF9D00"
COLOR_FONDO = "#181818"
COLOR_TEXTO = "#FFFFFF"
COLOR_ROJO = "#e74c3c"
COLOR_GRIS = "#888888"

class GestionarSalasAdminSection(ft.Column):
    def __init__(self, on_volver, page=None):
        super().__init__(expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        self.on_volver = on_volver
        self.page = page
        self.mensaje = ft.Text("", color=COLOR_NARANJA, size=16)
        self.salas = []
        self.tabla_salas = ft.Column(spacing=0)
        self.cargar_salas()
        # Formulario para agregar sala
        self.nombre_nueva = ft.TextField(label="Nombre de la sala", width=300, bgcolor=COLOR_FONDO, color=COLOR_TEXTO, border_color=COLOR_NARANJA)
        self.boton_agregar = ft.ElevatedButton(
            "Agregar Sala",
            bgcolor=COLOR_NARANJA,
            color="#ffffff",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
            on_click=self.agregar_sala
        )
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
            ft.Text("Gestionar Salas", size=32, weight="bold", color=COLOR_NARANJA),
            ft.Container(height=10),
            ft.Container(
                content=ft.Column([
                    ft.Text("Salas existentes", size=18, weight="bold", color=COLOR_TEXTO),
                    ft.Container(
                        content=self.tabla_salas,
                        bgcolor="#111",
                        border_radius=12,
                        padding=20,
                        width=700,
                        alignment=ft.alignment.center
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                bgcolor=COLOR_FONDO,
                border_radius=16,
                padding=20,
                width=800,
                shadow=ft.BoxShadow(blur_radius=10, color=COLOR_NARANJA)
            ),
            ft.Container(height=30),
            ft.Container(
                content=ft.Column([
                    ft.Text("Agregar nueva sala", size=18, weight="bold", color=COLOR_TEXTO),
                    ft.Row([
                        ft.Column([
                            ft.Text("Nombre de la sala", color=COLOR_NARANJA, weight="bold"),
                            self.nombre_nueva
                        ]),
                        ft.Column([
                            ft.Text("Capacidad", color=COLOR_NARANJA, weight="bold"),
                            ft.TextField(value="120", width=100, read_only=True, bgcolor=COLOR_GRIS, color=COLOR_TEXTO, border_color=COLOR_GRIS)
                        ])
                    ], spacing=30),
                    self.boton_agregar,
                    self.mensaje
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=16),
                bgcolor=COLOR_FONDO,
                border_radius=16,
                padding=30,
                width=600,
                shadow=ft.BoxShadow(blur_radius=10, color=COLOR_NARANJA)
            )
        ]

    def cargar_salas(self):
        self.tabla_salas.controls.clear()
        self.salas = db.get_salas_with_stats() or []
        # Cabecera
        self.tabla_salas.controls.append(
            ft.Row([
                ft.Text("ID", color=COLOR_NARANJA, weight="bold", width=30),
                ft.Text("Nombre", color=COLOR_NARANJA, weight="bold", width=200),
                ft.Text("Capacidad", color=COLOR_NARANJA, weight="bold", width=100),
                ft.Text("Funciones", color=COLOR_NARANJA, weight="bold", width=100),
                ft.Text("Acciones", color=COLOR_NARANJA, weight="bold", width=200),
            ], spacing=10)
        )
        for sala in self.salas:
            self.tabla_salas.controls.append(self.fila_sala(sala))

    def fila_sala(self, sala):
        total_funciones = sala.get("total_funciones", 0)
        return ft.Row([
            ft.Text(str(sala["id_sala"]), color=COLOR_TEXTO, width=30),
            ft.TextField(value=sala["nombre"], width=200, bgcolor=COLOR_FONDO, color=COLOR_TEXTO, border_color=COLOR_NARANJA, on_change=lambda e, s=sala: self.editar_nombre_sala(e, s)),
            ft.Text("120", color=COLOR_TEXTO, width=100),
            ft.Text(str(total_funciones), color=COLOR_TEXTO, width=100),
            ft.Row([
                ft.ElevatedButton(
                    "Editar",
                    bgcolor=COLOR_NARANJA,
                    color="#ffffff",
                    icon="edit",
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                    on_click=lambda e, s=sala: self.guardar_nombre_sala(s)
                ),
                ft.ElevatedButton(
                    "Eliminar",
                    bgcolor=COLOR_ROJO,
                    color="#ffffff",
                    icon="delete",
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                    on_click=lambda e, s=sala: self.eliminar_sala(s["id_sala"])
                )
            ], spacing=8, width=200)
        ], spacing=10)

    def editar_nombre_sala(self, e, sala):
        sala["nuevo_nombre"] = e.control.value

    def guardar_nombre_sala(self, sala):
        nuevo_nombre = sala.get("nuevo_nombre", sala["nombre"])
        db.execute_query("UPDATE salas SET nombre = %s WHERE id_sala = %s", (nuevo_nombre, sala["id_sala"]))
        self.mensaje.value = f"Sala actualizada."
        self.cargar_salas()
        self.update()

    def eliminar_sala(self, id_sala):
        def confirmar(e):
            success, message = db.delete_sala_safe(id_sala)
            self.mensaje.value = message
            self.cargar_salas()
            if self.page and hasattr(self.page, 'dialog'):
                self.page.dialog.open = False
            if self.page:
                self.page.update()
            self.update()
        dlg = ft.AlertDialog(
            title=ft.Text("¿Eliminar sala?", color=COLOR_ROJO),
            content=ft.Text("Esta acción no se puede deshacer.", color=COLOR_TEXTO),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.cerrar_dialogo()),
                ft.TextButton("Eliminar", on_click=lambda e: confirmar(e), style=ft.ButtonStyle(color=COLOR_ROJO))
            ]
        )
        if self.page:
            self.page.dialog = dlg
            dlg.open = True
            self.page.update()

    def cerrar_dialogo(self):
        if self.page and hasattr(self.page, 'dialog'):
            self.page.dialog.open = False
            self.page.update()

    def agregar_sala(self, e):
        nombre = self.nombre_nueva.value.strip()
        if not nombre:
            self.mensaje.value = "El nombre de la sala es obligatorio."
            self.update()
            return
        db.execute_query("INSERT INTO salas (nombre, capacidad) VALUES (%s, 120)", (nombre,))
        self.mensaje.value = "Sala agregada correctamente."
        self.nombre_nueva.value = ""
        self.cargar_salas()
        self.update() 