import flet as ft
from ui.comentarios import ComentariosUI
from services.db import db 

COLOR_NARANJA = "#FF9D00"
COLOR_FONDO = "#000000"
COLOR_TEXTO = "#FFFFFF"
COLOR_ICONOS = "#000000"
COLOR_SOMBRA = "#00000022"

class DetallePeliculaContent(ft.Column):
    def __init__(self, page: ft.Page, pelicula, mostrar_catalogo_callback, mostrar_comentarios_callback, mostrar_compra_entradas_callback):
        super().__init__(expand=True, scroll="auto") 
        self.page = page
        self.pelicula = pelicula
        self.mostrar_catalogo_callback = mostrar_catalogo_callback
        self.mostrar_comentarios_callback = mostrar_comentarios_callback
        self.mostrar_compra_entradas_callback = mostrar_compra_entradas_callback
        self.spacing = 0

        if not pelicula:
            self.controls = [
                 ft.Container(
                    content=ft.Text("No se pudo cargar el detalle de la película.", color=COLOR_TEXTO),
                    alignment=ft.alignment.center,
                    expand=True
                 )
            ]
            self.controls.append(
                 ft.Container(
                    content=ft.ElevatedButton("Volver al catálogo", on_click=lambda e: self.mostrar_catalogo_callback(), bgcolor=COLOR_NARANJA, color=COLOR_TEXTO, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20))),
                    alignment=ft.alignment.center,
                    margin=ft.margin.only(top=40)
                 )
            )
            return

        poster_url = pelicula["imagen_portada"] or "https://via.placeholder.com/240x380?text=Sin+Imagen"
        texto_generos = pelicula["genero"] or "Género no disponible"
        duracion = f"{pelicula['duracion']} min" if pelicula["duracion"] not in (None, 0, '', 'NULL') else "Sin dato"
        año = str(pelicula["fecha_estreno"] or "")

        info_content_column = [
            ft.Text(pelicula.get("titulo", "Título no disponible"), color=COLOR_TEXTO, size=24, weight=ft.FontWeight.BOLD),
            ft.Text(
                f"{año}    {texto_generos}    {duracion}",
                color=COLOR_TEXTO, size=16, weight=ft.FontWeight.BOLD
            ),
            ft.Container(
                content=ft.Text("Sinopsis", color=COLOR_TEXTO, size=18, weight=ft.FontWeight.BOLD),
                margin=ft.margin.only(top=20)
            ),
            ft.Text(pelicula.get("descripcion", "Sin sinopsis disponible."), color=COLOR_TEXTO, size=14),
        ]

        botones_row_controls = [
             ft.ElevatedButton(
                 "Enviar Reseña",
                 bgcolor="#D9D9D9",
                 color="#000000",
                 style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
                 on_click=lambda e: self.mostrar_comentarios_callback(self.pelicula)
             ),
             ft.ElevatedButton("Comprar Entrada", bgcolor=COLOR_NARANJA, color="#000000", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)), 
                on_click=lambda e: self.mostrar_compra_entradas_callback(self.pelicula)),
        ]

        botones_row = ft.Container(
            content=ft.Row(botones_row_controls, alignment=ft.MainAxisAlignment.START, spacing=20),
            margin=ft.margin.only(top=20)
        )

        info_content_column.append(botones_row)

        info_pelicula = ft.Container(
            content=ft.Column(info_content_column, alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.START),
            bgcolor="#222222",
            border_radius=30,
            padding=ft.padding.all(24),
            shadow=ft.BoxShadow(blur_radius=18, color=COLOR_SOMBRA, offset=ft.Offset(2, 4)),
            width=600,
        )

        seccion_principal = ft.Container(
            content=ft.Row([
                ft.Image(src=poster_url, width=240, height=380, border_radius=25, fit=ft.ImageFit.COVER),
                info_pelicula,
            ], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.START, spacing=50),
            alignment=ft.alignment.center,
            margin=ft.margin.only(top=40),
            expand=True
        )

        boton_volver = ft.Container(
             content=ft.ElevatedButton("Volver al catálogo", on_click=lambda e: self.mostrar_catalogo_callback(), bgcolor=COLOR_NARANJA, color=COLOR_TEXTO, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20))),
             margin=ft.margin.only(top=40, bottom=20, left=10)
        )

        comentarios_db = []
        if pelicula.get("id_pelicula"):
            comentarios_db = db.get_comentarios_by_pelicula(pelicula["id_pelicula"])
        reseñas_a_mostrar = comentarios_db if comentarios_db else []

        reseñas_container = ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Text("Reseñas de usuarios", color=COLOR_TEXTO, size=18, weight=ft.FontWeight.BOLD),
                        margin=ft.margin.only(bottom=10, left=10)
                    ),
                    *[ft.Container(
                        content=ft.Row([
                            ft.CircleAvatar(content=ft.Text(r["nombre_usuario"][0].upper() if r.get("nombre_usuario") else "U", size=18), color=COLOR_TEXTO, bgcolor=COLOR_NARANJA, radius=25),
                            ft.Container(
                                content=ft.Column([
                                    ft.Text(r["nombre_usuario"], color=COLOR_TEXTO, weight=ft.FontWeight.BOLD, size=15),
                                    ft.Text(r["comentario"], color=COLOR_TEXTO, size=13, expand=True),
                                ], alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.START, expand=True),
                                margin=ft.margin.only(left=15),
                                expand=True
                            ),
                        ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.START),
                        bgcolor="#222222",
                        border_radius=20,
                        padding=ft.padding.symmetric(horizontal=20, vertical=15),
                        shadow=ft.BoxShadow(blur_radius=10, color=COLOR_SOMBRA, offset=ft.Offset(2, 4)),
                        margin=ft.margin.only(top=15, bottom=0),
                        width=850,
                    ) for r in reseñas_a_mostrar]
                ],
                scroll=ft.ScrollMode.AUTO,
                spacing=0,
            ),
            height=400, 
            width=900,
            border_radius=20,
            bgcolor="#1A1A1A",
            padding=ft.padding.all(20),
        )

        self.controls = [
            seccion_principal,
            boton_volver,
            reseñas_container,
        ]

        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER