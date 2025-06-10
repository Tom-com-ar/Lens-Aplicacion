import flet as ft
from services.db import Database

COLOR_NARANJA = "#FF9D00"
COLOR_FONDO = "#1e1e1e"
COLOR_TEXTO = "#FFFFFF"

class RegistroUI(ft.Column):
    def __init__(self, page: ft.Page, on_registro_success=None, db=None):
        super().__init__()
        self.page = page
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
        
        self.email_field = ft.TextField(
            label="Email",
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
        
        self.controls = self.build()

    def build(self):
        return [
            ft.Container(
                content=ft.Column(
                    [
                        ft.Image(src="assets/logo.png", width=120, height=50),
                        ft.Text("Registro", size=32, color=COLOR_TEXTO, weight=ft.FontWeight.BOLD),
                        self.usuario_field,
                        self.email_field,
                        self.password_field,
                        ft.ElevatedButton(
                            "Registrarse",
                            width=200,
                            bgcolor=COLOR_NARANJA,
                            color="black",
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=10),
                            ),
                            on_click=self.registrar
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

    def registrar(self, e):
        usuario = self.usuario_field.value
        email = self.email_field.value
        password = self.password_field.value
        
        if usuario and email and password:
            success, mensaje = self.db.registrar_usuario(usuario, email, password)
            if success:
                if self.on_registro_success:
                    self.on_registro_success(e)
            else:
                print(mensaje)
        else:
            print("Por favor complete todos los campos")

    def ir_a_login(self, e):
        if self.on_registro_success:
            self.on_registro_success(e)