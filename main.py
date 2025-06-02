import flet as ft
from services.tmdb_api import TMDBApi
from ui.catalogo import CatalogoContent 
from ui.detalle_pelicula import DetallePeliculaContent 
from ui.comentarios import ComentariosUI
from ui.compra_entradas import CompraEntradasUI

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

    # Crear los controles de búsqueda
    campo_busqueda = ft.TextField(
        hint_text="Buscar...",
        bgcolor=COLOR_NARANJA,
        border_radius=20,
        height=44,
        width=260,
        content_padding=ft.padding.only(left=15),
        border_color=COLOR_NARANJA,
        on_change=lambda e: buscar_peliculas(e.control.value)
    )
    
    boton_buscar = ft.IconButton(
        "search", 
        icon_color=COLOR_ICONOS, 
        bgcolor=COLOR_NARANJA, 
        tooltip="Buscar", 
        width=44, 
        height=44, 
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
        on_click=lambda e: buscar_peliculas(campo_busqueda.value)
    )

    barra_superior = ft.Container(
        content=ft.Row([
            logo,
            ft.Container(expand=1),
            campo_busqueda,
            boton_buscar,
            ft.Container(width=30),
        ], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER),
    )

    # Usamos un ft.Column que expande para ocupar el espacio restante
    main_content_area = ft.Column(expand=True, scroll="auto", horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    # Crear la instancia del catálogo al inicio
    catalogo_content = CatalogoContent(page, tmdb_api, lambda p: mostrar_detalle(p))

    def mostrar_comentarios(pelicula):
        # Ocultar la barra de búsqueda
        campo_busqueda.visible = False
        boton_buscar.visible = False
        # Implementar la lógica para mostrar la pantalla de comentarios
        print("Mostrar comentarios para:", pelicula["title"])
        # Limpiar el área de contenido principal y agregar la vista de comentarios
        main_content_area.controls.clear()
        # Pasar la función mostrar_detalle como callback para el botón de volver
        comentarios_content = ComentariosUI(page, pelicula, mostrar_detalle)
        main_content_area.controls.append(comentarios_content)
        page.update()

    def mostrar_compra_entradas(pelicula):
        # Ocultar la barra de búsqueda
        campo_busqueda.visible = False
        boton_buscar.visible = False
        # Implementar la lógica para mostrar la pantalla de compra de entradas
        print("Mostrar compra de entradas para:", pelicula["title"])
        # Limpiar el área de contenido principal y agregar la vista de compra de entradas
        main_content_area.controls.clear()
        # Pasar la función mostrar_detalle como callback para el botón de volver en compra de entradas
        compra_entradas_content = CompraEntradasUI(page, pelicula, mostrar_detalle)
        main_content_area.controls.append(compra_entradas_content)
        page.update()

    def mostrar_detalle(pelicula):
        # Ocultar la barra de búsqueda
        campo_busqueda.visible = False
        boton_buscar.visible = False
        # Limpiar el área de contenido principal y agregar la vista de detalle
        main_content_area.controls.clear()
        # Pasar todos los callbacks necesarios a DetallePeliculaContent
        detalle_content = DetallePeliculaContent(
            page, tmdb_api, pelicula, mostrar_catalogo, mostrar_comentarios, mostrar_compra_entradas
        )
        main_content_area.controls.append(detalle_content)
        page.update()

    def buscar_peliculas(query):
        if not query:
            # Si el query está vacío, mostrar el catálogo completo (o según filtros aplicados)
            # Limpiar el query de búsqueda en el catálogo y aplicar filtros
            catalogo_content.filtrar_por_texto("") # Pasar string vacío para limpiar búsqueda
            return

        # Usar el método de filtrado por texto del catálogo existente
        catalogo_content.filtrar_por_texto(query)

    def mostrar_catalogo():
        # Mostrar la barra de búsqueda
        campo_busqueda.visible = True
        boton_buscar.visible = True
        # Limpiar el área de contenido principal y agregar la vista de catálogo
        main_content_area.controls.clear()

        # Añadir la instancia existente del catálogo de nuevo
        main_content_area.controls.append(catalogo_content)
        page.update()

    page.add(
        barra_superior, 
        main_content_area 
    )

    # Añadir el catálogo al área de contenido principal al inicio
    main_content_area.controls.append(catalogo_content)

    mostrar_catalogo()


ft.app(target=main)