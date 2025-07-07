import flet as ft
from services.db import db

COLOR_NARANJA = "#FF9D00"
COLOR_FONDO = "#181818"
COLOR_TEXTO = "#FFFFFF"
COLOR_VERDE = "#27ae60"
COLOR_ROJO = "#e74c3c"
COLOR_GRIS = "#888888"

class GestionarPeliculasAdminSection(ft.Column):
    def __init__(self, on_volver, on_agregar_manual=None, on_sincronizar_api=None, on_editar_manual=None, page=None):
        super().__init__(expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        self.on_volver = on_volver
        self.on_agregar_manual = on_agregar_manual
        self.on_sincronizar_api = on_sincronizar_api
        self.on_editar_manual = on_editar_manual
        self.page = page
        self.mensaje = ft.Text("", color=COLOR_NARANJA, size=16)
        # Estadísticas
        self.stats = self.obtener_stats()
        # Barra de búsqueda
        self.campo_busqueda = ft.TextField(
            hint_text="Buscar por título...",
            bgcolor=COLOR_FONDO,
            color=COLOR_TEXTO,
            border_radius=10,
            width=300,
            border_color=COLOR_NARANJA,
        )
        self.boton_buscar = ft.ElevatedButton(
            "Buscar",
            bgcolor=COLOR_NARANJA,
            color="#ffffff",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
            on_click=self.buscar_peliculas
        )
        self.boton_agregar = ft.ElevatedButton(
            "Agregar Nueva Película",
            bgcolor=COLOR_VERDE,
            color="#ffffff",
            icon="add",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
            on_click=lambda e: self.on_agregar_manual() if self.on_agregar_manual else None
        )
        self.boton_sincronizar = ft.ElevatedButton(
            "Sincronizar API",
            bgcolor=COLOR_ROJO,
            color="#ffffff",
            icon="sync",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
            on_click=lambda e: self.on_sincronizar_api() if self.on_sincronizar_api else None
        )
        self.boton_volver = ft.ElevatedButton(
            "← Volver al Panel",
            bgcolor=COLOR_GRIS,
            color="#ffffff",
            icon="arrow_back",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
            on_click=lambda e: self.on_volver()
        )
        # Tabla de películas
        self.tabla_peliculas = ft.Column(spacing=0)
        self.cargar_peliculas()
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
            ft.Text("Gestionar Películas", size=32, weight="bold", color=COLOR_NARANJA),
            ft.Container(height=10),
            ft.Row([
                self.stat_card(self.stats["manuales"], "Películas Manuales"),
                self.stat_card(self.stats["api"], "Películas de la API"),
                self.stat_card(self.stats["total"], "Total de Películas"),
            ], spacing=20),
            ft.Container(height=20),
            ft.Row([
                self.campo_busqueda,
                self.boton_buscar,
                self.boton_agregar,
                self.boton_sincronizar,
                self.boton_volver
            ], spacing=10),
            ft.Container(height=20),
            self.tabla_peliculas,
            self.mensaje
        ]

    def stat_card(self, valor, label):
        return ft.Container(
            content=ft.Column([
                ft.Text(str(valor), size=28, weight="bold", color=COLOR_NARANJA),
                ft.Text(label, color=COLOR_TEXTO)
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor="#181818",
            border_radius=12,
            padding=20,
            expand=1
        )

    def obtener_stats(self):
        total = db.count_peliculas_total()
        api = db.count_peliculas_api()
        manuales = db.count_peliculas_manuales()
        return {"total": total, "api": api, "manuales": manuales}

    def cargar_peliculas(self, filtro=None):
        self.tabla_peliculas.controls.clear()
        peliculas = db.get_peliculas_with_stats() or []
        if filtro:
            peliculas = [p for p in peliculas if filtro.lower() in p["titulo"].lower()]
        # Cabecera
        self.tabla_peliculas.controls.append(
            ft.Row([
                ft.Text("Imagen", color=COLOR_TEXTO, weight="bold", width=80),
                ft.Text("Título", color=COLOR_TEXTO, weight="bold", width=180),
                ft.Text("Tipo", color=COLOR_TEXTO, weight="bold", width=60),
                ft.Text("Género", color=COLOR_TEXTO, weight="bold", width=120),
                ft.Text("Año", color=COLOR_TEXTO, weight="bold", width=50),
                ft.Text("Funciones", color=COLOR_TEXTO, weight="bold", width=80),
                ft.Text("Comentarios", color=COLOR_TEXTO, weight="bold", width=100),
                ft.Text("Estado", color=COLOR_TEXTO, weight="bold", width=60),
                ft.Text("Acciones", color=COLOR_TEXTO, weight="bold", width=160),
            ], spacing=10)
        )
        for peli in peliculas:
            self.tabla_peliculas.controls.append(self.fila_pelicula(peli))

    def fila_pelicula(self, peli):
        portada = peli["imagen_portada"] or "https://via.placeholder.com/80x120?text=Sin+Imagen"
        tipo = "Manual" if peli["origen"] == "manual" else "API"
        color_tipo = COLOR_NARANJA if tipo == "Manual" else COLOR_GRIS
        total_funciones = peli.get("total_funciones", 0)
        total_comentarios = peli.get("total_comentarios", 0)
        return ft.Row([
            ft.Image(src=portada, width=60, height=90, border_radius=8),
            ft.Text(peli["titulo"], color=COLOR_TEXTO, width=180, max_lines=2, overflow=ft.TextOverflow.ELLIPSIS),
            ft.Text(tipo, color=color_tipo, width=60),
            ft.Text(peli["genero"] or "-", color=COLOR_TEXTO, width=120, max_lines=2, overflow=ft.TextOverflow.ELLIPSIS),
            ft.Text(str(peli["fecha_estreno"] or "-"), color=COLOR_TEXTO, width=50),
            ft.Text(str(total_funciones), color=COLOR_TEXTO, width=80),
            ft.Text(str(total_comentarios), color=COLOR_TEXTO, width=100),
            ft.Text(peli["estado"].capitalize(), color=COLOR_VERDE if peli["estado"]=="activa" else COLOR_ROJO, width=60),
            ft.Row([
                ft.ElevatedButton(
                    "Editar",
                    icon="edit",
                    bgcolor=COLOR_NARANJA,
                    color="#ffffff",
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                    disabled=(tipo!="Manual"),
                    on_click=(lambda e, peli=peli: self.on_editar_manual(peli)) if tipo=="Manual" and self.on_editar_manual else None
                ),
                ft.ElevatedButton(
                    "Eliminar",
                    icon="delete",
                    bgcolor=COLOR_ROJO,
                    color="#ffffff",
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                    on_click=lambda e, peli_id=peli["id_pelicula"]: self.eliminar_pelicula(peli_id)
                )
            ], spacing=4, width=160)
        ], spacing=10)

    def buscar_peliculas(self, e):
        filtro = self.campo_busqueda.value.strip()
        self.cargar_peliculas(filtro=filtro)
        self.update()

    def eliminar_pelicula(self, peli_id):
        print(f"Eliminar película con id: {peli_id}")  # Debug
        self.peli_id_a_eliminar = peli_id
        dlg = ft.AlertDialog(
            title=ft.Text("¿Eliminar película?", color=COLOR_ROJO),
            content=ft.Text("Esta acción no se puede deshacer.", color=COLOR_TEXTO),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.cerrar_dialogo()),
                ft.TextButton("Eliminar", on_click=lambda e: self.confirmar_eliminar(e), style=ft.ButtonStyle(color=COLOR_ROJO))
            ]
        )
        if self.page:
            self.page.dialog = dlg
            dlg.open = True
            self.page.update()

    def confirmar_eliminar(self, e):
        peli_id = getattr(self, 'peli_id_a_eliminar', None)
        if peli_id is not None:
            print(f"Intentando borrar película con id: {peli_id}")
            success, message = db.delete_pelicula_safe(peli_id)
            self.mensaje.value = message
            if self.page and hasattr(self.page, 'dialog'):
                self.page.dialog.open = False
            self.stats = self.obtener_stats()  # Actualizar estadísticas
            self.cargar_peliculas()
            self.update()
            if self.page:
                self.page.update()

    def cerrar_dialogo(self):
        if self.page and hasattr(self.page, 'dialog'):
            self.page.dialog.open = False
            self.page.update()