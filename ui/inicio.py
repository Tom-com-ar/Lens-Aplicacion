import flet as ft
from services.db import Database

COLOR_NARANJA = "#FF9D00"
COLOR_FONDO = "#1e1e1e"
COLOR_TEXTO = "#FFFFFF"

class InicioUI(ft.Column):
    def __init__(self, page: ft.Page, on_login_success=None, on_registro_success=None, db=None):
        super().__init__(
            controls=self.build(),  # <-- Pasa los controles aquí
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
            
        )
        self.page = page
        self.on_login_success = on_login_success
        self.on_registro_success = on_registro_success
        self.db = db or Database()
        
        # Crear los campos antes de build()
        self.usuario_field = ft.TextField(
            label="Nombre de Usuario",
            border_radius=10,
            bgcolor=COLOR_NARANJA,
            color="black",
            width=300
        )
        
        self.password_field = ft.TextField(
            label="Contraseña",
            password=True,
            can_reveal_password=True,
            border_radius=10,
            bgcolor=COLOR_NARANJA,
            color="black",
            width=300
        )

        # Mensaje de error
        self.mensaje_error = ft.Text(
            color="red",
            size=14,
            visible=False
        )
        
    def build(self):
        return [
            ft.Container(
                content=ft.Column(
                    [
                        ft.Image(src="assets/logo.png", width=120, height=50),
                        ft.Text("Bienvenido", size=32, color=COLOR_TEXTO, weight=ft.FontWeight.BOLD),
                        self.usuario_field,
                        self.password_field,
                        self.mensaje_error,
                        ft.ElevatedButton(
                            "Iniciar Sesión",
                            width=200,
                            bgcolor=COLOR_NARANJA,
                            color="black",
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=10),
                            ),
                            on_click=self.login
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,

                    spacing=20,
                ),
                padding=40,
                bgcolor=COLOR_FONDO,
                border_radius=10,
                width=400
            )
        ]

    def login(self, e):
        usuario = self.usuario_field.value
        password = self.password_field.value
        
        if usuario and password:
            success, resultado = self.db.verificar_usuario(usuario, password)
            if success:
                if self.on_login_success:
                    self.on_login_success()
            else:
                self.mensaje_error.value = "Usuario o contraseña incorrectos"
                self.mensaje_error.visible = True
                self.update()
        else:
            self.mensaje_error.value = "Por favor complete todos los campos"
            self.mensaje_error.visible = True
            self.update()
            
    def ir_a_registro(self, e):
        if self.on_registro_success:
            self.on_registro_success(e)