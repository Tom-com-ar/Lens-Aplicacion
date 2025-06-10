import flet as ft
from services.tmdb_api import TMDBApi
from ui.catalogo import CatalogoContent 
from ui.detalle_pelicula import DetallePeliculaContent 
from ui.comentarios import ComentariosUI
from ui.compra_entradas import CompraEntradasUI
from ui.auth import AuthContent
from ui.perfil_usuario import PerfilUsuarioContent

COLOR_NARANJA = "#FF9D00"
COLOR_FONDO = "#000000"
COLOR_TEXTO = "#FFFFFF"
COLOR_ICONOS = "#000000"
COLOR_SOMBRA = "#00000022"
COLOR_ERROR = "#FF0000"

def main(page: ft.Page):
    page.title = "Catálogo de Películas"
    page.padding = 0
    page.window_maximized = True 
    page.bgcolor = COLOR_FONDO 
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER 
    
    page.snack_bar = ft.SnackBar(content=ft.Text(""), bgcolor=COLOR_NARANJA)

    tmdb_api = TMDBApi()

    # Variable para almacenar el ID del usuario logueado
    logged_in_user_id = None

    def on_login_success(user_id):
        nonlocal logged_in_user_id
        logged_in_user_id = user_id
        print(f"Usuario {logged_in_user_id} ha iniciado sesión con éxito.")
        mostrar_catalogo() # Navegar al catálogo principal

    # Crear la instancia de la pantalla de autenticación
    auth_content = AuthContent(page, on_login_success)

    # Función para manejar el cierre de sesión
    def logout():
        nonlocal logged_in_user_id
        logged_in_user_id = None
        page.snack_bar.content = ft.Text("Sesión cerrada correctamente.")
        page.snack_bar.bgcolor = COLOR_NARANJA
        page.snack_bar.open = True
        main_content_area.controls.clear()
        main_content_area.controls.append(auth_content)
        page.update()

    # Función para mostrar la pantalla de perfil
    def mostrar_perfil():
        nonlocal logged_in_user_id
        if logged_in_user_id is None:
            page.snack_bar.content = ft.Text("Debes iniciar sesión para ver tu perfil.")
            page.snack_bar.bgcolor = COLOR_NARANJA
            page.snack_bar.open = True
            page.update()
            return
        
        print(f"DEBUG: Mostrando perfil para usuario ID: {logged_in_user_id}")
        main_content_area.controls.clear()
        from services.db import db 
        user_data = db.get_user_by_id(logged_in_user_id) 
        
        # Si no se encuentra el usuario
        if not user_data:
            page.snack_bar.content = ft.Text("No se pudo cargar la información del perfil.")
            page.snack_bar.bgcolor = COLOR_ERROR
            page.snack_bar.open = True
            page.update()
            logout()
            return

        perfil_content = PerfilUsuarioContent(
            page, 
            user_data, 
            logout, 
            mostrar_catalogo  # <-- Pasa aquí la función para volver al inicio
        )
        main_content_area.controls.append(perfil_content)
        page.update()

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
        on_change=lambda e: buscar_peliculas(e.control.value),
        text_style=ft.TextStyle(color=COLOR_TEXTO),
        cursor_color=COLOR_TEXTO
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

    # Botón de perfil
    boton_perfil = ft.IconButton(
        content=ft.Image(src="assets/User.png", width=44, height=44), # Usar la imagen directamente
        tooltip="Perfil de Usuario", 
        width=44, 
        height=44, 
        on_click=lambda e: mostrar_perfil() # Llamar a la función para mostrar el perfil
    )

    barra_superior = ft.Container(
        content=ft.Row([
            logo,
            ft.Container(expand=1),
            campo_busqueda,
            boton_buscar,
            boton_perfil, # Añadir el botón de perfil aquí
            ft.Container(width=30),
        ], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER),
    )

    main_content_area = ft.Column(expand=True, scroll="auto", horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    catalogo_content = CatalogoContent(page, tmdb_api, lambda p: mostrar_detalle(p))

    def mostrar_comentarios(pelicula):
        nonlocal logged_in_user_id
        if logged_in_user_id is None:
            page.snack_bar.content = ft.Text("Debes iniciar sesión para dejar un comentario.")
            page.snack_bar.bgcolor = COLOR_NARANJA # O un color de advertencia
            page.snack_bar.open = True
            page.update()
            return

        # Ocultar la barra de búsqueda
        campo_busqueda.visible = False
        boton_buscar.visible = False
        print("Mostrar comentarios para:", pelicula["title"])
        main_content_area.controls.clear()
        comentarios_content = ComentariosUI(page, pelicula, mostrar_detalle, logged_in_user_id) 
        main_content_area.controls.append(comentarios_content)
        page.update()

    def mostrar_compra_entradas(pelicula):
        nonlocal logged_in_user_id
        if logged_in_user_id is None:
            page.snack_bar.content = ft.Text("Debes iniciar sesión para comprar entradas.")
            page.snack_bar.bgcolor = COLOR_NARANJA # O un color de advertencia
            page.snack_bar.open = True
            page.update()
            return

        # Ocultar la barra de búsqueda
        campo_busqueda.visible = False
        boton_buscar.visible = False
        print("Mostrar compra de entradas para:", pelicula["title"])
        main_content_area.controls.clear()
        compra_entradas_content = CompraEntradasUI(page, pelicula, mostrar_detalle, logged_in_user_id)
        main_content_area.controls.append(compra_entradas_content)
        page.update()

    def mostrar_detalle(pelicula):
        # Ocultar la barra de búsqueda
        campo_busqueda.visible = False
        boton_buscar.visible = False
        main_content_area.controls.clear()
        detalle_content = DetallePeliculaContent(
            page, tmdb_api, pelicula, mostrar_catalogo, mostrar_comentarios, mostrar_compra_entradas
        )
        main_content_area.controls.append(detalle_content)
        page.update()

    def buscar_peliculas(query):
        if not query:
            # Si el query está vacío, mostrar el catálogo completo
            catalogo_content.filtrar_por_texto("")
            page.update()
            return

        # Usar el método de filtrado por texto del catálogo existente
        catalogo_content.filtrar_por_texto(query)
        page.update()

    def mostrar_catalogo():
        # Mostrar la barra de búsqueda
        campo_busqueda.visible = True
        boton_buscar.visible = True
        # Limpiar el área de contenido principal y agregar la vista de catálogo
        main_content_area.controls.clear()

        main_content_area.controls.append(catalogo_content)
        page.update()

    page.add(
        barra_superior, 
        main_content_area 
    )

    # Al inicio, mostrar la pantalla de autenticación
    main_content_area.controls.append(auth_content)
    page.update() 


ft.app(target=main)