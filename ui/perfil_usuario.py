import flet as ft

COLOR_NARANJA = "#FF9D00"
COLOR_FONDO = "#000000"
COLOR_TEXTO = "#FFFFFF"
COLOR_GRIS_OSCURO = "#1A1A1A"

class PerfilUsuarioContent(ft.Column):
    def __init__(self, page: ft.Page, user_data: dict, logout_callback):
        super().__init__(expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        self.page = page
        self.user_data = user_data
        self.logout_callback = logout_callback

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

        # Botón para cerrar sesión
        logout_button = ft.ElevatedButton(
            text="Cerrar Sesión",
            icon="logout",
            bgcolor=COLOR_NARANJA,
            color=COLOR_FONDO,
            on_click=lambda e: self.logout_callback(),
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20))
        )

        self.controls = [
            ft.Container(
                content=ft.Column([
                    user_info,
                    logout_button
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=30),
                padding=ft.padding.all(40),
                bgcolor=COLOR_GRIS_OSCURO,
                border_radius=20,
                width=450, # Ancho fijo para el contenedor del perfil
                shadow=ft.BoxShadow(blur_radius=15, color=COLOR_NARANJA)
            )
        ] 