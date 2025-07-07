import flet as ft
from ui.catalogo import CatalogoContent 
from ui.detalle_pelicula import DetallePeliculaContent 
from ui.comentarios import ComentariosUI
from ui.compra_entradas import CompraEntradasUI
from ui.auth import AuthContent
from ui.perfil_usuario import PerfilUsuarioContent
from ui.admin.admin_panel import AdminPanel
from ui.admin.buscar_api import BuscarApiAdminSection
from ui.admin.agregar_pelicula import AgregarPeliculaAdminSection
from ui.admin.gestionar_peliculas import GestionarPeliculasAdminSection
from ui.admin.gestionar_salas import GestionarSalasAdminSection
from ui.admin.gestionar_funciones import GestionarFuncionesAdminSection

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

    # Variable para almacenar el ID del usuario logueado
    logged_in_user_id = None

    def on_login_success(user_id):
        nonlocal logged_in_user_id
        logged_in_user_id = user_id
        print(f"Usuario {logged_in_user_id} ha iniciado sesión con éxito.")
        # Cambia la barra superior al modo normal (con búsqueda y usuario)
        barra_superior.content = crear_barra_superior(modo_auth=False).content
        mostrar_catalogo()
        page.update()

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
        # Cambia la barra superior al modo auth (solo logo centrado)
        barra_superior.content = crear_barra_superior(modo_auth=True).content
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

        def mostrar_panel_admin():
            from services.db import db
            campo_busqueda.visible = False
            boton_buscar.visible = False
            def set_section(seccion):
                if seccion == "buscar_api":
                    main_content_area.controls.clear()
                    main_content_area.controls.append(BuscarApiAdminSection(on_volver=mostrar_dashboard))
                    page.update()
                elif seccion == "agregar_pelicula":
                    main_content_area.controls.clear()
                    main_content_area.controls.append(AgregarPeliculaAdminSection(on_volver=mostrar_dashboard))
                    page.update()
                elif seccion == "gestionar_peliculas":
                    mostrar_gestionar_peliculas()
                elif seccion == "gestionar_salas":
                    main_content_area.controls.clear()
                    main_content_area.controls.append(GestionarSalasAdminSection(on_volver=mostrar_dashboard, page=page))
                    page.update()
                elif seccion == "gestionar_funciones":
                    main_content_area.controls.clear()
                    seccion_funciones = GestionarFuncionesAdminSection(on_volver=mostrar_dashboard, page=page)
                    main_content_area.controls.append(seccion_funciones)
                    page.update()
                    seccion_funciones.did_mount()
            def volver_al_sitio():
                campo_busqueda.visible = True
                boton_buscar.visible = True
                mostrar_catalogo()
            mostrar_dashboard()

        perfil_content = PerfilUsuarioContent(
            page, 
            user_data, 
            logout, 
            mostrar_catalogo,
            mostrar_panel_admin if user_data.get("rol") == "admin" else None
        )
        main_content_area.controls.append(perfil_content)
        page.update()

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

    def crear_barra_superior(modo_auth=False):
        if modo_auth:
            # Solo logo centrado
            return ft.Container(
                content=ft.Row([
                    ft.Container(expand=1),
                    ft.Container(
                        content=ft.Image(src="assets/logo.png", width=120, height=50),
                        bgcolor="#fff",
                        border_radius=50,
                        padding=ft.padding.symmetric(horizontal=18, vertical=8),
                        margin=ft.margin.only(top=20, left=0, right=0, bottom=0),
                    ),
                    ft.Container(expand=1),
                ], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            )
        else:
            # Logo a la izquierda, barra de búsqueda y botón usuario
            return ft.Container(
                content=ft.Row([
                    ft.Container(
                        content=ft.Image(src="assets/logo.png", width=120, height=50),
                        bgcolor="#fff",
                        border_radius=50,
                        padding=ft.padding.symmetric(horizontal=18, vertical=8),
                        margin=ft.margin.only(top=20, left=20, right=0, bottom=0),
                    ),
                    ft.Container(expand=1),
                    campo_busqueda,
                    boton_buscar,
                    boton_perfil,
                    ft.Container(width=30),
                ], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            )

    barra_superior = crear_barra_superior(modo_auth=True)

    main_content_area = ft.Column(expand=True, scroll="auto", horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    catalogo_content = CatalogoContent(page, lambda p: mostrar_detalle(p))

    reseña_en_progreso = False

    def mostrar_comentarios(pelicula):
        nonlocal reseña_en_progreso
        if reseña_en_progreso:
            return
        reseña_en_progreso = True

        def volver():
            nonlocal reseña_en_progreso
            reseña_en_progreso = False
            mostrar_detalle(pelicula)

        def reseña_enviada():
            mostrar_detalle(pelicula)

        main_content_area.controls.clear()
        comentarios_content = ComentariosUI(
            page, pelicula, logged_in_user_id,
            on_volver=volver,
            on_enviar=reseña_enviada
        )
        main_content_area.controls.append(comentarios_content)
        page.update()
        reseña_en_progreso = False

    compra_en_progreso = False  # Variable global o de la función main

    def mostrar_compra_entradas(pelicula):
        nonlocal compra_en_progreso
        if compra_en_progreso:
            return  # Ya hay una compra en curso, ignora el nuevo click
        compra_en_progreso = True

        campo_busqueda.visible = False
        boton_buscar.visible = False
        main_content_area.controls.clear()
        compra_entradas_content = CompraEntradasUI(page, pelicula, mostrar_detalle, logged_in_user_id)
        main_content_area.controls.append(compra_entradas_content)
        page.update()
        compra_en_progreso = False  # Permite otra compra después

    detalle_mostrado = False  # Variable global o de la función main

    def mostrar_detalle(pelicula):
        nonlocal detalle_mostrado
        if detalle_mostrado:
            return  # Ya hay un detalle mostrándose, ignora el nuevo click
        detalle_mostrado = True

        campo_busqueda.visible = False
        boton_buscar.visible = False
        main_content_area.controls.clear()
        detalle_content = DetallePeliculaContent(page, pelicula, mostrar_catalogo, mostrar_comentarios, mostrar_compra_entradas)
        main_content_area.controls.append(detalle_content)
        page.update()
        detalle_mostrado = False  # Permite mostrar otro detalle después

    def buscar_peliculas(query):
        if query.strip() == "":
            catalogo_content.cargar_peliculas()
        else:
            catalogo_content.buscar_peliculas(query)

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

    class SincronizarApiAdminSection(ft.Column):
        def __init__(self, on_volver):
            super().__init__(expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            self.on_volver = on_volver
            self.mensaje = ft.Text("", color=COLOR_NARANJA, size=16)
            self.categorias = {
                "Populares": "popular",
                "Mejor valoradas": "top_rated",
                "Cartelera": "now_playing"
            }
            self.cantidad_opciones = [20, 40, 60, 80, 100]
            self.categoria = ft.Dropdown(
                label="Categoría de Películas:",
                options=[ft.dropdown.Option(k) for k in self.categorias.keys()],
                value="Populares",
                width=300
            )
            self.cantidad = ft.Dropdown(
                label="Cantidad de Páginas:",
                options=[ft.dropdown.Option(str(c)) for c in self.cantidad_opciones],
                value="20",
                width=300
            )
            self.solo_nuevas = ft.Checkbox(label="Solo agregar películas nuevas (no actualizar existentes)", value=False, fill_color=COLOR_NARANJA, check_color=COLOR_TEXTO)
            self.boton_sincronizar = ft.ElevatedButton(
                "Sincronizar API",
                bgcolor=COLOR_NARANJA,
                color="#ffffff",
                icon="sync",
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
                on_click=self.sincronizar
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
                ft.Text("Sincronizar Películas de la API", size=32, weight="bold", color=COLOR_NARANJA),
                ft.Container(height=20),
                ft.Container(
                    content=ft.Column([
                        self.categoria,
                        self.cantidad,
                        self.solo_nuevas,
                        self.boton_sincronizar,
                        self.mensaje
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=16),
                    bgcolor=COLOR_FONDO,
                    border_radius=16,
                    padding=30,
                    width=500,
                    shadow=ft.BoxShadow(blur_radius=10, color=COLOR_NARANJA)
                )
            ]

        def sincronizar(self, e):
            import requests
            from services.db import db
            API_KEY = "e6822a7ed386f7102b6a857ea5e3c17f"
            categoria = self.categorias[self.categoria.value]
            cantidad = int(self.cantidad.value)
            solo_nuevas = self.solo_nuevas.value
            agregadas = 0
            actualizadas = 0
            page = 1
            try:
                while (agregadas if solo_nuevas else actualizadas) < cantidad:
                    url = f"https://api.themoviedb.org/3/movie/{categoria}?api_key={API_KEY}&language=es-ES&page={page}"
                    resp = requests.get(url)
                    data = resp.json()
                    resultados = data.get("results", [])
                    if not resultados:
                        break  # No hay más resultados
                    for peli in resultados:
                        tmdb_id = peli.get("id")
                        existe = db.execute_query("SELECT id_pelicula FROM peliculas WHERE tmdb_id = %s", (tmdb_id,))
                        # Obtener detalles completos
                        detalles_url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={API_KEY}&language=es-ES"
                        detalles = requests.get(detalles_url).json()
                        titulo = detalles.get("title", "Sin título")
                        descripcion = detalles.get("overview", "")
                        generos = ", ".join([g["name"] for g in detalles.get("genres", [])])
                        fecha_estreno = detalles.get("release_date", "")[:4] if detalles.get("release_date") else None
                        duracion = detalles.get("runtime")
                        imagen_portada = f"https://image.tmdb.org/t/p/w500{detalles.get('poster_path')}" if detalles.get("poster_path") else None
                        if solo_nuevas:
                            if not existe and agregadas < cantidad:
                                db.execute_query(
                                    """
                                    INSERT INTO peliculas (origen, tmdb_id, titulo, descripcion, genero, fecha_estreno, duracion, imagen_portada, estado)
                                    VALUES ('api', %s, %s, %s, %s, %s, %s, %s, 'activa')
                                    """,
                                    (tmdb_id, titulo, descripcion, generos, fecha_estreno, duracion, imagen_portada)
                                )
                                agregadas += 1
                        else:
                            if existe and actualizadas < cantidad:
                                db.execute_query(
                                    """
                                    UPDATE peliculas SET titulo=%s, descripcion=%s, genero=%s, fecha_estreno=%s, duracion=%s, imagen_portada=%s, estado='activa', fecha_actualizada=NOW() WHERE tmdb_id=%s
                                    """,
                                    (titulo, descripcion, generos, fecha_estreno, duracion, imagen_portada, tmdb_id)
                                )
                                actualizadas += 1
                        if (agregadas if solo_nuevas else actualizadas) >= cantidad:
                            break
                    page += 1
                self.mensaje.value = f"Sincronización completada. Agregadas: {agregadas}, Actualizadas: {actualizadas}"
                self.update()
            except Exception as ex:
                self.mensaje.value = f"Error: {ex}"
                self.update()

    def mostrar_gestionar_peliculas():
        main_content_area.controls.clear()
        main_content_area.controls.append(
            GestionarPeliculasAdminSection(
                on_volver=mostrar_dashboard,
                on_agregar_manual=mostrar_agregar_manual,
                on_sincronizar_api=mostrar_sincronizar_api,
                on_editar_manual=mostrar_editar_manual,
                page=page
            )
        )
        page.update()

    def mostrar_agregar_manual():
        main_content_area.controls.clear()
        main_content_area.controls.append(
            AgregarPeliculaAdminSection(on_volver=mostrar_gestionar_peliculas)
        )
        page.update()

    def mostrar_sincronizar_api():
        main_content_area.controls.clear()
        main_content_area.controls.append(
            SincronizarApiAdminSection(on_volver=mostrar_gestionar_peliculas)
        )
        page.update()

    def mostrar_editar_manual(peli):
        main_content_area.controls.clear()
        main_content_area.controls.append(
            AgregarPeliculaAdminSection(
                on_volver=mostrar_gestionar_peliculas,
                pelicula=peli
            )
        )
        page.update()

    # --- Dashboard global para navegación admin ---
    def mostrar_dashboard():
        from services.db import db
        def set_section(seccion):
            if seccion == "buscar_api":
                main_content_area.controls.clear()
                main_content_area.controls.append(BuscarApiAdminSection(on_volver=mostrar_dashboard))
                page.update()
            elif seccion == "agregar_pelicula":
                main_content_area.controls.clear()
                main_content_area.controls.append(AgregarPeliculaAdminSection(on_volver=mostrar_dashboard))
                page.update()
            elif seccion == "gestionar_peliculas":
                mostrar_gestionar_peliculas()
            elif seccion == "gestionar_salas":
                main_content_area.controls.clear()
                main_content_area.controls.append(GestionarSalasAdminSection(on_volver=mostrar_dashboard, page=page))
                page.update()
            elif seccion == "gestionar_funciones":
                main_content_area.controls.clear()
                seccion_funciones = GestionarFuncionesAdminSection(on_volver=mostrar_dashboard, page=page)
                main_content_area.controls.append(seccion_funciones)
                page.update()
                seccion_funciones.did_mount()
        def volver_al_sitio():
            campo_busqueda.visible = True
            boton_buscar.visible = True
            mostrar_catalogo()
        stats = {
            "peliculas_total": db.count_peliculas_total(),
            "peliculas_api": db.count_peliculas_api(),
            "peliculas_manuales": db.count_peliculas_manuales(),
            "usuarios": db.count_usuarios(),
            "comentarios": db.count_comentarios(),
            "entradas": db.count_entradas()
        }
        main_content_area.controls.clear()
        admin_panel = AdminPanel(page, stats, logout, volver_al_sitio, set_section)
        main_content_area.controls.append(admin_panel)
        page.update()

ft.app(target=main)