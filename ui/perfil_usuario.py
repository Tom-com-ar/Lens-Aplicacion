import flet as ft
from services.db import db

COLOR_NARANJA = "#FF9D00"
COLOR_FONDO = "#000000"
COLOR_TEXTO = "#FFFFFF"
COLOR_GRIS_OSCURO = "#1A1A1A"

class PerfilUsuarioContent(ft.Column):
    def __init__(self, page: ft.Page, user_data: dict, logout_callback, back_to_inicio_callback, on_admin_panel_callback=None):
        super().__init__(expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll="auto")
        self.page = page
        self.user_data = user_data
        self.logout_callback = logout_callback
        self.back_to_inicio_callback = back_to_inicio_callback
        self.on_admin_panel_callback = on_admin_panel_callback

        self.create_layout()

    def create_layout(self):
        # Información del usuario
        user_info = ft.Column([
            ft.Text("Información de Perfil", size=28, weight=ft.FontWeight.BOLD, color=COLOR_TEXTO),
            ft.Divider(color=COLOR_NARANJA),
            ft.Row([
                ft.Text("Nombre de Usuario:", size=18, weight=ft.FontWeight.BOLD, color=COLOR_TEXTO),
                ft.Text(self.user_data.get("nombre_usuario", "N/A"), size=18, color=COLOR_TEXTO),
            ], alignment=ft.MainAxisAlignment.START),
            ft.Row([
                ft.Text("Email:", size=18, weight=ft.FontWeight.BOLD, color=COLOR_TEXTO),
                ft.Text(self.user_data.get("email", "N/A"), size=18, color=COLOR_TEXTO),
            ], alignment=ft.MainAxisAlignment.START),
            ft.Divider(color=COLOR_NARANJA),
        ], horizontal_alignment=ft.CrossAxisAlignment.START, spacing=15)

        # Sección de Entradas Compradas
        entradas_compradas = self.create_entradas_section()
        
        # Sección de Comentarios Realizados
        comentarios_realizados = self.create_comentarios_section()

        # Botones
        botones = []
        if self.user_data.get("rol") == "admin" and self.on_admin_panel_callback:
            botones.append(
                ft.ElevatedButton(
                    text="Panel de Administrador",
                    icon="admin_panel_settings",
                    bgcolor=COLOR_NARANJA,
                    color=COLOR_FONDO,
                    on_click=lambda e: self.on_admin_panel_callback(),
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20))
                )
            )
        botones.append(
            ft.ElevatedButton(
                text="Cerrar Sesión",
                icon="logout",
                bgcolor=COLOR_NARANJA,
                color=COLOR_FONDO,
                on_click=lambda e: self.logout_callback(),
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20))
            )
        )
        botones.append(
            ft.TextButton(
                text="Volver al inicio",
                icon="arrow_back",
                style=ft.ButtonStyle(
                    color=COLOR_NARANJA,
                    shape=ft.RoundedRectangleBorder(radius=20)
                ),
                on_click=lambda e: self.back_to_inicio_callback()
            )
        )

        self.controls = [
            ft.Container(
                content=ft.Column([
                    user_info,
                    entradas_compradas,
                    comentarios_realizados,
                    *botones
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=30),
                padding=ft.padding.all(40),
                bgcolor=COLOR_GRIS_OSCURO,
                border_radius=20,
                width=800,
                shadow=ft.BoxShadow(blur_radius=15, color=COLOR_NARANJA)
            )
        ]

    def create_entradas_section(self):
        entradas = db.get_entradas_by_usuario(self.user_data["id_usuario"]) or []
        entradas_content = [
            ft.Text("Entradas Compradas", size=24, weight=ft.FontWeight.BOLD, color=COLOR_TEXTO),
            ft.Divider(color=COLOR_NARANJA),
        ]
        if not entradas:
            entradas_content.append(
                ft.Text("No has comprado ninguna entrada aún.", color=COLOR_TEXTO, size=16)
            )
        else:
            # Agrupar por id_funcion
            funciones = {}
            for entrada in entradas:
                key = entrada["id_funcion"]
                if key not in funciones:
                    funciones[key] = {
                        "titulo_pelicula": entrada["titulo_pelicula"],
                        "nombre_sala": entrada["nombre_sala"],
                        "fecha_hora": entrada["fecha_hora"],
                        "asientos": [],
                    }
                funciones[key]["asientos"].append(f"{entrada['fila']}{entrada['numero_asiento']}")
            for funcion in funciones.values():
                entrada_card = ft.Container(
                    content=ft.Column([
                        ft.Text(f"{funcion['titulo_pelicula']}", color=COLOR_TEXTO, size=16, weight=ft.FontWeight.BOLD),
                        ft.Text(f"Cantidad de entradas: {len(funcion['asientos'])}", color=COLOR_TEXTO, size=14),
                        ft.Text(f"Sala: {funcion['nombre_sala']}", color=COLOR_TEXTO, size=14),
                        ft.Text(f"Fecha: {funcion['fecha_hora']}", color=COLOR_TEXTO, size=14, weight=ft.FontWeight.BOLD),
                        ft.Text("Asientos:", color=COLOR_TEXTO, size=14, weight=ft.FontWeight.BOLD),
                        ft.Column([
                            ft.Text(f"Asiento: {asiento}", color=COLOR_TEXTO, size=13) for asiento in funcion["asientos"]
                        ], spacing=2, expand=False),
                    ], spacing=5),
                    bgcolor=COLOR_FONDO,
                    border_radius=10,
                    padding=15,
                    margin=ft.margin.only(bottom=10)
                )
                entradas_content.append(entrada_card)
        return ft.Column(entradas_content, horizontal_alignment=ft.CrossAxisAlignment.START, spacing=15)

    def create_comentarios_section(self):
        comentarios = db.get_comentarios_by_usuario(self.user_data["id_usuario"]) or []
        
        comentarios_content = [
            ft.Text("Comentarios Realizados", size=24, weight=ft.FontWeight.BOLD, color=COLOR_TEXTO),
            ft.Divider(color=COLOR_NARANJA),
        ]
        
        if not comentarios:
            comentarios_content.append(
                ft.Text("No has realizado ningún comentario aún.", color=COLOR_TEXTO, size=16)
            )
        else:
            for comentario in comentarios:
                comentario_card = ft.Container(
                    content=ft.Column([
                        ft.Text(f"Película: {comentario['titulo_pelicula']}", 
                               color=COLOR_TEXTO, size=16, weight=ft.FontWeight.BOLD),
                        ft.Text(f"Comentario: {comentario['comentario']}", color=COLOR_TEXTO, size=14),
                        ft.Text(f"Valoración: {comentario['valoracion']}/5", color=COLOR_TEXTO, size=14),
                        ft.Text(f"Fecha: {comentario['fecha_comentario']}", color=COLOR_TEXTO, size=14),
                    ], spacing=5),
                    bgcolor=COLOR_FONDO,
                    border_radius=10,
                    padding=15,
                    margin=ft.margin.only(bottom=10)
                )
                comentarios_content.append(comentario_card)
        
        return ft.Column(comentarios_content, horizontal_alignment=ft.CrossAxisAlignment.START, spacing=15)