import flet as ft
from services.tmdb_api import TMDBApi
from ui.catalogo import CatalogoContent 
from ui.detalle_pelicula import DetallePeliculaContent 
from ui.comentarios import ComentariosUI

COLOR_NARANJA = "#FF9D00"
COLOR_FONDO = "#000000"
COLOR_TEXTO = "#FFFFFF"
COLOR_ICONOS = "#000000"
COLOR_SOMBRA = "#00000022"

def main(page: ft.Page):
    page.title = "Catálogo de Películas"
    page.padding = 0
    page.window_maximized = True 
    page.bgcolor = COLOR_FONDO 
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER 

    tmdb_api = TMDBApi()

    logo = ft.Container(
        content=ft.Image(src="assets/logo.png", width=120, height=50),
        bgcolor="#fff",
        border_radius=50,
        padding=ft.padding.symmetric(horizontal=18, vertical=8),
        margin=ft.margin.only(top=20, left=20, right=0, bottom=0),
    )

    barra_superior = ft.Container(
        content=ft.Row([
            logo,
            ft.Container(expand=1),
            ft.TextField(
                hint_text="Buscar...",
                bgcolor=COLOR_NARANJA,
                border_radius=20,
                height=44,
                width=260,
                content_padding=ft.padding.only(left=15),
                border_color=COLOR_NARANJA,
            ),
            ft.IconButton("search", icon_color=COLOR_ICONOS, bgcolor=COLOR_NARANJA, tooltip="Buscar", width=44, height=44, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20))),
            ft.Container(width=30),
        ], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER),

    )

    # Usamos un ft.Column que expande para ocupar el espacio restante
    main_content_area = ft.Column(expand=True, scroll="auto", horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    def mostrar_comentarios(pelicula):
        # Aquí puedes implementar la lógica para mostrar la pantalla de comentarios
        print("Mostrar comentarios para:", pelicula["title"])
        # Ejemplo: limpiar y mostrar ComentariosUI si tienes versión Flet
        # main_content_area.controls.clear()
        # main_content_area.controls.append(ComentariosUI(page, pelicula))
        # page.update()

    def mostrar_detalle(pelicula):
        # Limpiar el área de contenido principal y agregar la vista de detalle
        main_content_area.controls.clear()
        detalle_content = DetallePeliculaContent(
            page, tmdb_api, pelicula, mostrar_catalogo, mostrar_comentarios
        )
        main_content_area.controls.append(detalle_content)
        page.update()

    def mostrar_catalogo():
        # Limpiar el área de contenido principal y agregar la vista de catálogo
        main_content_area.controls.clear()
        catalogo_content = CatalogoContent(page, tmdb_api, lambda p: mostrar_detalle(p))
        main_content_area.controls.append(catalogo_content)
        page.update()

    page.add(
        barra_superior, 
        main_content_area 
    )

    mostrar_catalogo()


ft.app(target=main)