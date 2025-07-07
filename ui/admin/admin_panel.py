import flet as ft

COLOR_NARANJA = "#FF9D00"
COLOR_FONDO = "#000000"
COLOR_TEXTO = "#FFFFFF"
COLOR_ICONOS = "#000000"
COLOR_SOMBRA = "#00000022"
COLOR_ERROR = "#FF0000"

class AdminPanel(ft.Column):
    def __init__(self, page, stats, on_logout, on_volver_sitio, set_section):
        super().__init__(expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll="auto")
        self.page = page
        self.stats = stats  # Diccionario con los conteos
        self.on_logout = on_logout
        self.on_volver_sitio = on_volver_sitio
        self.set_section = set_section  # función (str) -> None
        self.build()

    def build(self):
        # Tarjetas de estadísticas
        stat_cards = ft.Row([
            ft.Container(
                content=ft.Column([
                    ft.Text(str(self.stats.get("peliculas_total", 0)), size=28, weight="bold", color=COLOR_TEXTO),
                    ft.Text("Total Películas", color=COLOR_TEXTO)
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                bgcolor="#181818",
                border_radius=12,
                padding=20,
                expand=1
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text(str(self.stats.get("peliculas_api", 0)), size=28, weight="bold", color=COLOR_TEXTO),
                    ft.Text("De la API", color=COLOR_TEXTO)
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                bgcolor="#181818",
                border_radius=12,
                padding=20,
                expand=1
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text(str(self.stats.get("peliculas_manuales", 0)), size=28, weight="bold", color=COLOR_TEXTO),
                    ft.Text("Manuales", color=COLOR_TEXTO)
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                bgcolor="#181818",
                border_radius=12,
                padding=20,
                expand=1
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text(str(self.stats.get("usuarios", 0)), size=28, weight="bold", color=COLOR_TEXTO),
                    ft.Text("Usuarios", color=COLOR_TEXTO)
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                bgcolor="#181818",
                border_radius=12,
                padding=20,
                expand=1
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text(str(self.stats.get("comentarios", 0)), size=28, weight="bold", color=COLOR_TEXTO),
                    ft.Text("Comentarios", color=COLOR_TEXTO)
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                bgcolor="#181818",
                border_radius=12,
                padding=20,
                expand=1
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text(str(self.stats.get("entradas", 0)), size=28, weight="bold", color=COLOR_TEXTO),
                    ft.Text("Entradas", color=COLOR_TEXTO)
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                bgcolor="#181818",
                border_radius=12,
                padding=20,
                expand=1
            ),
        ], spacing=16)

        # Botones de navegación (sin barra de búsqueda)
        nav_buttons = ft.Row([
            ft.Container(
                content=ft.ElevatedButton(
                    "Buscar en API",
                    icon="search",
                    bgcolor="#23272e",
                    color=COLOR_TEXTO,
                    on_click=lambda e: self.set_section("buscar_api")
                ),
                expand=1, padding=8
            ),
            ft.Container(
                content=ft.ElevatedButton(
                    "Agregar Película",
                    icon="add",
                    bgcolor="#23272e",
                    color=COLOR_TEXTO,
                    on_click=lambda e: self.set_section("agregar_pelicula")
                ),
                expand=1, padding=8
            ),
            ft.Container(
                content=ft.ElevatedButton(
                    "Gestionar Películas",
                    icon="list",
                    bgcolor="#23272e",
                    color=COLOR_TEXTO,
                    on_click=lambda e: self.set_section("gestionar_peliculas")
                ),
                expand=1, padding=8
            ),
            ft.Container(
                content=ft.ElevatedButton(
                    "Gestionar Salas",
                    icon="movie",
                    bgcolor="#23272e",
                    color=COLOR_TEXTO,
                    on_click=lambda e: self.set_section("gestionar_salas")
                ),
                expand=1, padding=8
            ),
            ft.Container(
                content=ft.ElevatedButton(
                    "Gestionar Funciones",
                    icon="event",
                    bgcolor="#23272e",
                    color=COLOR_TEXTO,
                    on_click=lambda e: self.set_section("gestionar_funciones")
                ),
                expand=1, padding=8
            ),
        ], spacing=12)

        # Botones inferiores
        bottom_buttons = ft.Row([
            ft.ElevatedButton("Volver al Sitio", icon="home", bgcolor=COLOR_NARANJA, color=COLOR_ICONOS, on_click=lambda e: self.on_volver_sitio()),
            ft.ElevatedButton("Cerrar Sesión", icon="logout", bgcolor="#ff4d4d", color=COLOR_TEXTO, on_click=lambda e: self.on_logout())
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)

        self.controls = [
            ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Column([
                            ft.Text("\U0001F3AC Panel de Administrador", size=36, weight="bold", color=COLOR_TEXTO),
                            ft.Text("Bienvenido, admin", color=COLOR_TEXTO, size=18)
                        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        bgcolor=COLOR_NARANJA,
                        border_radius=16,
                        padding=24,
                        margin=ft.margin.only(bottom=24)
                    ),
                    stat_cards,
                    ft.Container(height=24),
                    nav_buttons,
                    ft.Container(height=32),
                    bottom_buttons
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            )
        ] 