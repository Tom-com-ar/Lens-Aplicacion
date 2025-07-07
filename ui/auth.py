import flet as ft
from services.db import db 
COLOR_NARANJA = "#FF9D00"
COLOR_FONDO = "#000000"
COLOR_TEXTO = "#FFFFFF"
COLOR_GRIS_CLARO = "#848484"
COLOR_EXITO = "#4CAF50" 
COLOR_ERROR = "#F44336"  

class AuthContent(ft.Column):
    def __init__(self, page: ft.Page, on_login_success):
        super().__init__(expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        self.page = page
        self.on_login_success = on_login_success 

        self.is_register_mode = ft.Ref[ft.Column]()
        
        self.campo_nombre_usuario = ft.TextField(
            label="Nombre de Usuario",
            label_style=ft.TextStyle(color=COLOR_TEXTO),
            bgcolor=COLOR_GRIS_CLARO,
            color=COLOR_FONDO,
            border_radius=10,
            width=300,
            text_align=ft.TextAlign.CENTER,
            capitalization=ft.TextCapitalization.WORDS,
            autocorrect=False, 
            enable_suggestions=False 
        )
        self.campo_email = ft.TextField(
            label="Email",
            label_style=ft.TextStyle(color=COLOR_TEXTO),
            bgcolor=COLOR_GRIS_CLARO,
            color=COLOR_FONDO,
            border_radius=10,
            width=300,
            text_align=ft.TextAlign.CENTER,
            keyboard_type=ft.KeyboardType.EMAIL,
            autocorrect=False, 
            enable_suggestions=False 
        )
        self.campo_password = ft.TextField(
            label="Contraseña",
            label_style=ft.TextStyle(color=COLOR_TEXTO),
            bgcolor=COLOR_GRIS_CLARO,
            color=COLOR_FONDO,
            border_radius=10,
            width=300,
            password=True, 
            can_reveal_password=True,
            text_align=ft.TextAlign.CENTER,
            autocorrect=False, 
            enable_suggestions=False 
        )

        self.toggle_button = ft.TextButton(
            text="¿Ya tienes cuenta? Inicia Sesión",
            on_click=self.toggle_mode,
            style=ft.ButtonStyle(color=COLOR_TEXTO)
        )

        self.auth_button = ft.ElevatedButton(
            text="Registrarse",
            bgcolor=COLOR_NARANJA,
            color=COLOR_FONDO,
            width=300,
            on_click=self.handle_auth,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20))
        )

        self.create_layout()

    def create_layout(self):
        self.controls = [
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("Registrarse", size=30, weight=ft.FontWeight.BOLD, color=COLOR_TEXTO, text_align=ft.TextAlign.CENTER),
                        self.campo_nombre_usuario,
                        self.campo_email,
                        self.campo_password,
                        self.auth_button,
                        self.toggle_button
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                    ref=self.is_register_mode
                ),
                padding=ft.padding.all(30),
                bgcolor=COLOR_FONDO,
                border_radius=20,
                shadow=ft.BoxShadow(blur_radius=15, color=COLOR_NARANJA)
            )
        ]

    def toggle_mode(self, e):
        if self.campo_nombre_usuario:
            self.campo_nombre_usuario.value = ""
        self.campo_email.value = ""
        self.campo_password.value = ""

        # Cambiar entre modo de registro y login
        if self.auth_button.text == "Registrarse":
            self.auth_button.text = "Iniciar Sesión"
            self.toggle_button.text = "¿No tienes cuenta? Regístrate"
            self.is_register_mode.current.controls.remove(self.campo_nombre_usuario)
            self.is_register_mode.current.controls[0].value = "Iniciar Sesión" 
        else:
            self.auth_button.text = "Registrarse"
            self.toggle_button.text = "¿Ya tienes cuenta? Inicia Sesión"
            self.is_register_mode.current.controls.insert(1, self.campo_nombre_usuario) 
            self.is_register_mode.current.controls[0].value = "Registrarse"
        self.page.update()

    def handle_auth(self, e):
        email = self.campo_email.value.strip()
        password = self.campo_password.value.strip()
        
        if not email or not password:
            self.page.snack_bar.content = ft.Text("Por favor, completa todos los campos.")
            self.page.snack_bar.bgcolor = COLOR_ERROR
            self.page.snack_bar.open = True
            self.page.update()
            return

        if self.auth_button.text == "Registrarse":
            nombre_usuario = self.campo_nombre_usuario.value.strip()
            if not nombre_usuario:
                self.page.snack_bar.content = ft.Text("Por favor, ingresa tu nombre de usuario.")
                self.page.snack_bar.bgcolor = COLOR_ERROR
                self.page.snack_bar.open = True
                self.page.update()
                return
            
            # Lógica de registro
            print(f"DEBUG: Intento de registro con email: {email}")
            existing_user = db.get_user_by_email(email)
            if existing_user:
                self.page.snack_bar.content = ft.Text("Este email ya está registrado.")
                self.page.snack_bar.bgcolor = COLOR_ERROR
                self.page.snack_bar.open = True
                print("DEBUG: Intento de registro con email existente.")
                self.page.update()
            else:
                rows_affected = db.add_user(nombre_usuario, email, password)
                if rows_affected:
                    self.page.snack_bar.content = ft.Text("¡Registro exitoso! Ya puedes iniciar sesión.")
                    self.page.snack_bar.bgcolor = COLOR_EXITO
                    self.page.snack_bar.open = True
                    print(f"DEBUG: Usuario registrado: {nombre_usuario}, {email}")
                    self.toggle_mode(None)
                else:
                    self.page.snack_bar.content = ft.Text("Error en el registro. Inténtalo de nuevo.")
                    self.page.snack_bar.bgcolor = COLOR_ERROR
                    self.page.snack_bar.open = True
                    print("DEBUG: Error al registrar usuario en DB.")
                    self.page.update()
        else:
            # Lógica de inicio de sesión
            print(f"DEBUG: Intentando iniciar sesión con email: {email}")
            user = db.get_user_by_email(email)
            if user and db.check_password(password, user["password_hash"]):
                self.page.snack_bar.content = ft.Text(f"¡Bienvenido, {user['nombre_usuario']}!")
                self.page.snack_bar.bgcolor = COLOR_EXITO
                self.page.snack_bar.open = True
                print(f"DEBUG: Inicio de sesión exitoso para usuario ID: {user['id_usuario']}")
                self.on_login_success(user["id_usuario"])
            else:
                self.page.snack_bar.content = ft.Text("Email o contraseña incorrectos.")
                self.page.snack_bar.bgcolor = COLOR_ERROR
                self.page.snack_bar.open = True
                print("DEBUG: Email o contraseña incorrectos.")
