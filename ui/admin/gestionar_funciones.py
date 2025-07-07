import flet as ft
from services.db import db
from datetime import datetime, timedelta

COLOR_NARANJA = "#FF9D00"
COLOR_FONDO = "#181818"
COLOR_TEXTO = "#FFFFFF"
COLOR_ROJO = "#e74c3c"
COLOR_GRIS = "#888888"

class GestionarFuncionesAdminSection(ft.Column):
    def __init__(self, on_volver, page=None):
        super().__init__(expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        self.on_volver = on_volver
        self.page = page
        self.mensaje = ft.Text("", color=COLOR_NARANJA, size=16)
        self.peliculas = db.execute_query("SELECT id_pelicula, titulo FROM peliculas WHERE estado = 'activa' ORDER BY titulo ASC") or []
        self.salas = db.execute_query("SELECT id_sala, nombre FROM salas ORDER BY nombre ASC") or []
        # Formulario agregar función
        self.pelicula_dropdown = ft.Dropdown(
            label="Película",
            options=[ft.dropdown.Option(str(p["id_pelicula"]), p["titulo"]) for p in self.peliculas],
            width=300
        )
        self.sala_dropdown = ft.Dropdown(
            label="Sala",
            options=[ft.dropdown.Option(str(s["id_sala"]), s["nombre"]) for s in self.salas],
            width=300
        )
        self.fecha_hora = ft.TextField(label="Fecha y Hora (YYYY-MM-DD HH:MM)", width=300, hint_text="2025-07-30 20:00")
        self.precio = ft.TextField(label="Precio", width=200)
        self.boton_agregar = ft.ElevatedButton(
            "Agregar Función",
            bgcolor=COLOR_NARANJA,
            color="#ffffff",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
            on_click=self.agregar_funcion
        )
        self.listado_funciones = ft.Column([])
        self.funcion_editando = None  # ID de la función que se está editando
        self.funcion_edit_data = {}   # Datos temporales de edición
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
            ft.Text("Gestionar Funciones", size=32, weight="bold", color=COLOR_NARANJA),
            ft.Container(height=10),
            ft.Container(
                content=ft.Column([
                    ft.Text("Agregar nueva función", size=18, weight="bold", color=COLOR_TEXTO),
                    self.pelicula_dropdown,
                    self.sala_dropdown,
                    self.fecha_hora,
                    self.precio,
                    self.boton_agregar,
                    self.mensaje
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=16),
                bgcolor=COLOR_FONDO,
                border_radius=16,
                padding=30,
                width=500,
                shadow=ft.BoxShadow(blur_radius=10, color=COLOR_NARANJA)
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text("Funciones programadas", size=20, weight="bold", color=COLOR_TEXTO),
                    self.listado_funciones
                ], spacing=10),
                bgcolor=COLOR_FONDO,
                border_radius=16,
                padding=30,
                width=1300,
                margin=ft.margin.only(top=30),
                shadow=ft.BoxShadow(blur_radius=10, color=COLOR_NARANJA)
            ),
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
                margin=ft.margin.only(top=30, bottom=20)
            )
        ]

    def did_mount(self):
        self.cargar_funciones()

    def cargar_funciones(self):
        self.listado_funciones.controls.clear()
        funciones = db.get_funciones_with_stats() or []
        encabezado = ft.Row([
            ft.Text("ID", weight="bold", color=COLOR_NARANJA, width=40),
            ft.Text("Película", weight="bold", color=COLOR_NARANJA, width=220),
            ft.Text("Sala", weight="bold", color=COLOR_NARANJA, width=120),
            ft.Text("Fecha y Hora", weight="bold", color=COLOR_NARANJA, width=160),
            ft.Text("Precio", weight="bold", color=COLOR_NARANJA, width=100),
            ft.Text("Entradas", weight="bold", color=COLOR_NARANJA, width=80),
            ft.Text("Estado", weight="bold", color=COLOR_NARANJA, width=100),
            ft.Text("Acciones", weight="bold", color=COLOR_NARANJA, width=260)
        ], alignment=ft.MainAxisAlignment.START)
        self.listado_funciones.controls.append(encabezado)
        ahora = datetime.now()
        for f in funciones:
            id_funcion = f["id_funcion"]
            fecha_funcion = f["fecha_hora"]
            if isinstance(fecha_funcion, str):
                fecha_funcion_dt = datetime.strptime(fecha_funcion, "%Y-%m-%d %H:%M:%S")
            else:
                fecha_funcion_dt = fecha_funcion
            duracion = f["duracion"] or 0
            fin_funcion = fecha_funcion_dt + timedelta(minutes=duracion)
            estado = "Próxima" if fin_funcion > ahora else "Finalizado"
            color_estado = COLOR_NARANJA if estado == "Próxima" else COLOR_ROJO
            editable = estado == "Próxima"
            en_edicion = self.funcion_editando == id_funcion
            entradas_vendidas = f.get("entradas_vendidas", 0)
            # Si está en edición, usar los datos temporales
            if en_edicion:
                edit_data = self.funcion_edit_data
                pelicula_value = edit_data.get("id_pelicula", str(f["id_pelicula"]))
                sala_value = edit_data.get("id_sala", str(f["id_sala"]))
                # Mostrar y editar fecha en formato dd/mm/yyyy HH:MM
                fecha_value = edit_data.get("fecha_hora", fecha_funcion_dt.strftime("%d/%m/%Y %H:%M"))
                precio_value = edit_data.get("precio", str(f["precio"]))
            else:
                pelicula_value = str(f["id_pelicula"])
                sala_value = str(f["id_sala"])
                fecha_value = fecha_funcion_dt.strftime("%d/%m/%Y %H:%M")
                precio_value = str(f["precio"])
            row = ft.Row([
                ft.Text(str(id_funcion), width=40, color=COLOR_TEXTO),
                ft.Dropdown(
                    value=pelicula_value,
                    options=[ft.dropdown.Option(str(p["id_pelicula"]), p["titulo"]) for p in self.peliculas],
                    width=220,
                    disabled=not (editable and en_edicion),
                    color=COLOR_TEXTO,
                    bgcolor=COLOR_FONDO,
                    border_color=COLOR_GRIS,
                    text_style=ft.TextStyle(color=COLOR_TEXTO),
                    on_change=(lambda e, fid=id_funcion: self._on_edit_change(fid, "id_pelicula", e.control.value)) if en_edicion else None
                ) if editable else ft.Text(f["titulo"], width=220, color=COLOR_TEXTO),
                ft.Dropdown(
                    value=sala_value,
                    options=[ft.dropdown.Option(str(s["id_sala"]), s["nombre"]) for s in self.salas],
                    width=120,
                    disabled=not (editable and en_edicion),
                    color=COLOR_TEXTO,
                    bgcolor=COLOR_FONDO,
                    border_color=COLOR_GRIS,
                    text_style=ft.TextStyle(color=COLOR_TEXTO),
                    on_change=(lambda e, fid=id_funcion: self._on_edit_change(fid, "id_sala", e.control.value)) if en_edicion else None
                ) if editable else ft.Text(f["nombre_sala"], width=120, color=COLOR_TEXTO),
                ft.TextField(
                    value=fecha_value,
                    width=160,
                    disabled=not (editable and en_edicion),
                    color=COLOR_TEXTO,
                    bgcolor=COLOR_FONDO,
                    border_color=COLOR_GRIS,
                    text_style=ft.TextStyle(color=COLOR_TEXTO),
                    on_change=(lambda e, fid=id_funcion: self._on_edit_change(fid, "fecha_hora", e.control.value)) if en_edicion else None,
                    hint_text="dd/mm/yyyy HH:MM"
                ) if editable else ft.Text(fecha_value, width=160, color=COLOR_TEXTO),
                ft.TextField(
                    value=precio_value,
                    width=100,
                    disabled=not (editable and en_edicion),
                    color=COLOR_TEXTO,
                    bgcolor=COLOR_FONDO,
                    border_color=COLOR_GRIS,
                    text_style=ft.TextStyle(color=COLOR_TEXTO),
                    on_change=(lambda e, fid=id_funcion: self._on_edit_change(fid, "precio", e.control.value)) if en_edicion else None
                ) if editable else ft.Text(precio_value, width=100, color=COLOR_TEXTO),
                ft.Text(str(entradas_vendidas), width=80, color=COLOR_TEXTO),
                ft.Text(estado, width=100, color=color_estado, weight="bold"),
                ft.Row([
                    ft.ElevatedButton(
                        "Guardar" if en_edicion else "Editar",
                        bgcolor=COLOR_NARANJA,
                        color="#ffffff",
                        disabled=not editable,
                        width=100,
                        on_click=(lambda e, fid=id_funcion: self._guardar_edicion(fid)) if en_edicion else (lambda e, fid=id_funcion: self._iniciar_edicion(fid, f))
                    ),
                    ft.ElevatedButton(
                        "Cancelar" if en_edicion else "Eliminar",
                        bgcolor=COLOR_ROJO,
                        color="#ffffff",
                        width=100,
                        on_click=(lambda e: self._cancelar_edicion()) if en_edicion else (lambda e, fid=id_funcion: self._eliminar_funcion(fid))
                    )
                ], spacing=10, width=260)
            ], alignment=ft.MainAxisAlignment.START)
            self.listado_funciones.controls.append(row)
        # Mensaje de advertencia si hay funciones finalizadas
        if any((f["fecha_hora"] if isinstance(f["fecha_hora"], datetime) else datetime.strptime(f["fecha_hora"], "%Y-%m-%d %H:%M:%S")) + timedelta(minutes=f["duracion"] or 0) <= ahora for f in funciones):
            self.listado_funciones.controls.append(
                ft.Text("Solo puedes eliminar funciones finalizadas. La edición está deshabilitada.", color=COLOR_ROJO, size=14)
            )
        self.update()

    def _iniciar_edicion(self, id_funcion, datos):
        self.funcion_editando = id_funcion
        self.funcion_edit_data = {
            "id_pelicula": str(datos["id_pelicula"]),
            "id_sala": str(datos["id_sala"]),
            "fecha_hora": datos["fecha_hora"][:16] if isinstance(datos["fecha_hora"], str) else datos["fecha_hora"].strftime("%Y-%m-%d %H:%M"),
            "precio": str(datos["precio"])
        }
        self.cargar_funciones()

    def _on_edit_change(self, id_funcion, campo, valor):
        if self.funcion_editando == id_funcion:
            self.funcion_edit_data[campo] = valor
        self.listado_funciones.update()

    def _cancelar_edicion(self):
        self.funcion_editando = None
        self.funcion_edit_data = {}
        self.cargar_funciones()

    def _guardar_edicion(self, id_funcion):
        try:
            data = self.funcion_edit_data
            id_pelicula = int(data.get("id_pelicula", 0))
            id_sala = int(data.get("id_sala", 0))
            fecha_hora_str = data.get("fecha_hora", "").strip()
            precio = float(data.get("precio", 0))
            if not (id_pelicula and id_sala and fecha_hora_str):
                self.mensaje.value = "Completa todos los campos correctamente."
                self.update()
                return
            # Convertir fecha de dd/mm/yyyy HH:MM a yyyy-mm-dd HH:MM
            try:
                fecha_dt = datetime.strptime(fecha_hora_str, "%d/%m/%Y %H:%M")
                fecha_hora_db = fecha_dt.strftime("%Y-%m-%d %H:%M")
            except Exception:
                self.mensaje.value = "Formato de fecha inválido. Usa dd/mm/yyyy HH:MM."
                self.update()
                return
            # Obtener duración de la película
            peli = db.execute_query("SELECT duracion FROM peliculas WHERE id_pelicula = %s", (id_pelicula,))
            duracion = peli[0]["duracion"] if peli and peli[0]["duracion"] else 0
            if not duracion or duracion <= 0:
                self.mensaje.value = "La película seleccionada no tiene duración válida."
                self.update()
                return
            inicio = fecha_dt
            fin = inicio + timedelta(minutes=duracion + 15)
            # Validar solapamiento (excluyendo la función actual)
            query = '''
                SELECT f.*, p.titulo FROM funciones f
                JOIN peliculas p ON f.id_pelicula = p.id_pelicula
                WHERE f.id_sala = %s AND f.id_funcion != %s AND ((f.fecha_hora <= %s AND DATE_ADD(f.fecha_hora, INTERVAL (p.duracion + 15) MINUTE) > %s) OR (f.fecha_hora < %s AND DATE_ADD(f.fecha_hora, INTERVAL (p.duracion + 15) MINUTE) >= %s))
            '''
            solapadas = db.execute_query(query, (id_sala, id_funcion, fecha_hora_db, fecha_hora_db, fin.strftime("%Y-%m-%d %H:%M:%S"), fin.strftime("%Y-%m-%d %H:%M:%S")))
            if solapadas:
                self.mensaje.value = "Ya existe una función en la misma sala y horario que se solapa. Corrige el horario."
                self.update()
                return
            db.execute_query(
                "UPDATE funciones SET id_pelicula=%s, id_sala=%s, fecha_hora=%s, precio=%s WHERE id_funcion=%s",
                (id_pelicula, id_sala, fecha_hora_db, precio, id_funcion)
            )
            self.mensaje.value = "Función actualizada correctamente."
            self.funcion_editando = None
            self.funcion_edit_data = {}
            self.cargar_funciones()
        except Exception as ex:
            self.mensaje.value = f"Error: {ex}"
            self.update()

    def _eliminar_funcion(self, id_funcion):
        dlg = ft.AlertDialog(
            title=ft.Text("¿Eliminar función?", color=COLOR_ROJO),
            content=ft.Text("¿Estás seguro de que deseas eliminar esta función? Esta acción no se puede deshacer.", color=COLOR_TEXTO),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self._cerrar_dialogo(dlg)),
                ft.TextButton("Eliminar", on_click=lambda e: self._confirmar_eliminar_funcion(id_funcion, dlg), style=ft.ButtonStyle(color=COLOR_ROJO))
            ]
        )
        if self.page:
            self.page.dialog = dlg
            dlg.open = True
            self.page.update()

    def _cerrar_dialogo(self, dlg):
        if self.page:
            dlg.open = False
            self.page.update()

    def _confirmar_eliminar_funcion(self, id_funcion, dlg):
        try:
            success, message = db.delete_funcion_safe(id_funcion)
            self.mensaje.value = message
            if self.page:
                dlg.open = False
            self.cargar_funciones()
            if self.page:
                self.page.update()
        except Exception as ex:
            self.mensaje.value = f"Error al eliminar: {ex}"
            if self.page:
                dlg.open = False
                self.page.update()

    def agregar_funcion(self, e):
        try:
            id_pelicula = int(self.pelicula_dropdown.value or 0)
            id_sala = int(self.sala_dropdown.value or 0)
            fecha_hora_str = self.fecha_hora.value.strip()
            precio = float(self.precio.value.strip() or 0)
            if not (id_pelicula and id_sala and fecha_hora_str):
                self.mensaje.value = "Completa todos los campos correctamente."
                self.update()
                return
            # Obtener duración de la película
            peli = db.execute_query("SELECT duracion FROM peliculas WHERE id_pelicula = %s", (id_pelicula,))
            duracion = peli[0]["duracion"] if peli and peli[0]["duracion"] else 0
            if not duracion or duracion <= 0:
                self.mensaje.value = "La película seleccionada no tiene duración válida."
                self.update()
                return
            inicio = datetime.strptime(fecha_hora_str, "%Y-%m-%d %H:%M")
            fin = inicio + timedelta(minutes=duracion + 15)
            # Buscar solapamientos en la misma sala
            query = '''
                SELECT f.*, p.titulo FROM funciones f
                JOIN peliculas p ON f.id_pelicula = p.id_pelicula
                WHERE f.id_sala = %s AND ((f.fecha_hora <= %s AND DATE_ADD(f.fecha_hora, INTERVAL (p.duracion + 15) MINUTE) > %s) OR (f.fecha_hora < %s AND DATE_ADD(f.fecha_hora, INTERVAL (p.duracion + 15) MINUTE) >= %s))
            '''
            solapadas = db.execute_query(query, (id_sala, fecha_hora_str, fecha_hora_str, fin.strftime("%Y-%m-%d %H:%M:%S"), fin.strftime("%Y-%m-%d %H:%M:%S")))
            if solapadas:
                self.mensaje.value = "Ya existe una función en la misma sala y horario que se solapa. Corrige el horario."
                self.update()
                return
            db.execute_query(
                "INSERT INTO funciones (id_pelicula, id_sala, fecha_hora, precio) VALUES (%s, %s, %s, %s)",
                (id_pelicula, id_sala, fecha_hora_str, precio)
            )
            self.mensaje.value = "Función agregada correctamente."
            self.pelicula_dropdown.value = None
            self.sala_dropdown.value = None
            self.fecha_hora.value = ""
            self.precio.value = ""
            self.update()
        except Exception as ex:
            self.mensaje.value = f"Error: {ex}"
            self.update() 