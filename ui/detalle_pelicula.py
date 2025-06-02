import flet as ft
from services.tmdb_api import TMDBApi
from ui.comentarios import ComentariosUI
import webbrowser

COLOR_NARANJA = "#FF9D00"
COLOR_FONDO = "#000000"
COLOR_TEXTO = "#FFFFFF"
COLOR_ICONOS = "#000000"
COLOR_SOMBRA = "#00000022"

# Reseñas de ejemplo (pueden ir en un archivo de datos o base de datos real después)
RESEÑAS_EJEMPLO = [
    {"usuario": "Juan Pérez", "texto": "¡Excelente película! Me encantó la historia y los personajes."},
    {"usuario": "Ana López", "texto": "Muy buena, la recomiendo para ver en familia."},
    {"usuario": "Carlos Ruiz", "texto": "La fotografía y la música son increíbles."},
    {"usuario": "Laura Giménez", "texto": "Me mantuvo al borde del asiento. ¡Muy recomendada!"},
    {"usuario": "Pedro Sánchez", "texto": "El guion es un poco flojo, pero visualmente es impresionante."},
    {"usuario": "Juan Pérez", "texto": "¡Excelente película! Me encantó la historia y los personajes."},
    {"usuario": "Ana López", "texto": "Muy buena, la recomiendo para ver en familia."},
    {"usuario": "Carlos Ruiz", "texto": "La fotografía y la música son increíbles."},
    {"usuario": "Laura Giménez", "texto": "Me mantuvo al borde del asiento. ¡Muy recomendada!"},
    {"usuario": "Pedro Sánchez", "texto": "El guion es un poco flojo, pero visualmente es impresionante."},
    {"usuario": "Juan Pérez", "texto": "¡Excelente película! Me encantó la historia y los personajes."},
    {"usuario": "Ana López", "texto": "Muy buena, la recomiendo para ver en familia."},
    {"usuario": "Carlos Ruiz", "texto": "La fotografía y la música son increíbles."},
    {"usuario": "Laura Giménez", "texto": "Me mantuvo al borde del asiento. ¡Muy recomendada!"},
    {"usuario": "Pedro Sánchez", "texto": "El guion es un poco flojo, pero visualmente es impresionante."},
    {"usuario": "Juan Pérez", "texto": "¡Excelente película! Me encantó la historia y los personajes."},
    {"usuario": "Ana López", "texto": "Muy buena, la recomiendo para ver en familia."},
    {"usuario": "Carlos Ruiz", "texto": "La fotografía y la música son increíbles."},
    {"usuario": "Laura Giménez", "texto": "Me mantuvo al borde del asiento. ¡Muy recomendada!"},
    {"usuario": "Pedro Sánchez", "texto": "El guion es un poco flojo, pero visualmente es impresionante."},
    {"usuario": "Juan Pérez", "texto": "¡Excelente película! Me encantó la historia y los personajes."},
    {"usuario": "Ana López", "texto": "Muy buena, la recomiendo para ver en familia."},
    {"usuario": "Carlos Ruiz", "texto": "La fotografía y la música son increíbles."},
    {"usuario": "Laura Giménez", "texto": "Me mantuvo al borde del asiento. ¡Muy recomendada!"},
    {"usuario": "Pedro Sánchez", "texto": "El guion es un poco flojo, pero visualmente es impresionante."},
]


class DetallePeliculaContent(ft.Column): # Cambiado a Content
    def __init__(self, page: ft.Page, tmdb_api: TMDBApi, pelicula, mostrar_catalogo_callback, mostrar_comentarios_callback, mostrar_compra_entradas_callback):
        super().__init__(expand=True, scroll="auto") 
        self.page = page
        self.tmdb_api = tmdb_api
        self.pelicula = pelicula
        self.mostrar_catalogo_callback = mostrar_catalogo_callback
        self.mostrar_comentarios_callback = mostrar_comentarios_callback
        self.mostrar_compra_entradas_callback = mostrar_compra_entradas_callback
        self.spacing = 0 # Eliminar espaciado por defecto

        detalle = self.tmdb_api.obtener_detalle_pelicula(pelicula["id"])

        if not detalle:
            self.controls = [
                 ft.Container( # Contenedor para centrar el mensaje
                    content=ft.Text("No se pudo cargar el detalle de la película.", color=COLOR_TEXTO),
                    alignment=ft.alignment.center,
                    expand=True
                 )
            ]
            # Agrega un botón para volver al catálogo si no se carga el detalle
            self.controls.append(
                 ft.Container(
                    content=ft.ElevatedButton("Volver al catálogo", on_click=lambda e: self.mostrar_catalogo_callback(), bgcolor=COLOR_NARANJA, color=COLOR_TEXTO, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20))),
                    alignment=ft.alignment.center,
                    margin=ft.margin.only(top=40)
                 )
            )
            return

        # --- Imagen y datos principales ---
        poster_url = f"https://image.tmdb.org/t/p/w500{detalle['poster_path']}" if detalle.get("poster_path") else "https://via.placeholder.com/240x380?text=Sin+Imagen"

        # --- Obtener videos y buscar trailer ---
        videos = self.tmdb_api.obtener_videos_pelicula(pelicula["id"])
        trailer_url = None
        for video in videos:
            if video.get("site") == "YouTube" and video.get("type") == "Trailer":
                # Usar la URL normal de visualización para abrir en el navegador
                trailer_url = f"https://www.youtube.com/watch?v={video['key']}"
                break # Encontramos el primer trailer y salimos

        # --- Obtener y unir todos los géneros ---
        generos = detalle.get('genres', [])
        nombres_generos = [g.get('name', 'Desconocido') for g in generos if g and g.get('name')]
        texto_generos = ", ".join(nombres_generos) if nombres_generos else "Género no disponible"

        info_content_column = [
            ft.Text(detalle.get("title", "Título no disponible"), color=COLOR_TEXTO, size=24, weight=ft.FontWeight.BOLD),
            ft.Text(
                f"{detalle.get('release_date', '')[:4]}    {texto_generos}    {detalle.get('runtime', 0)//60}H {detalle.get('runtime', 0)%60}M",
                color=COLOR_TEXTO, size=16, weight=ft.FontWeight.BOLD
            ),
            ft.Container(
                content=ft.Text("Sinopsis", color=COLOR_TEXTO, size=18, weight=ft.FontWeight.BOLD),
                margin=ft.margin.only(top=20)
            ),
            ft.Text(detalle.get("overview", "Sin sinopsis disponible."), color=COLOR_TEXTO, size=14), # Sin expand aquí
        ]

        # Botones (Enviar Reseña, Comprar Entrada, y ahora Trailer)
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

        if trailer_url:
            # Agregar botón de trailer si se encontró uno
            botones_row_controls.append(
                 ft.ElevatedButton(
                     "Ver Trailer",
                     icon="play_arrow",
                     on_click=lambda e, url=trailer_url: webbrowser.open(url), # Abrir en navegador
                     bgcolor=COLOR_FONDO,
                     color=COLOR_TEXTO,
                     style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20))
                 )
            )

        botones_row = ft.Container(
            content=ft.Row(botones_row_controls, alignment=ft.MainAxisAlignment.START, spacing=20),
            margin=ft.margin.only(top=20)
        )

        info_content_column.append(botones_row)


        info_pelicula = ft.Container(
            content=ft.Column(info_content_column, alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.START), # Sin expand en esta columna
            bgcolor="#222222",
            border_radius=30,
            padding=ft.padding.all(24),
            shadow=ft.BoxShadow(blur_radius=18, color=COLOR_SOMBRA, offset=ft.Offset(2, 4)),
            width=600, # Ajusta si es necesario
        )

        # --- Sección principal (imagen + info) ---
        seccion_principal = ft.Container(
            content=ft.Row([
                ft.Image(src=poster_url, width=240, height=380, border_radius=25, fit=ft.ImageFit.COVER),
                info_pelicula,
            ], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.START, spacing=50),
            alignment=ft.alignment.center,
            margin=ft.margin.only(top=40),
            expand=True
        )


        # --- Botón Volver ---
        boton_volver = ft.Container(
             content=ft.ElevatedButton("Volver al catálogo", on_click=lambda e: self.mostrar_catalogo_callback(), bgcolor=COLOR_NARANJA, color=COLOR_TEXTO, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20))),
             margin=ft.margin.only(top=40, bottom=20, left=10)
        )

        # --- Contenedor de reseñas con scroll individual ---
        reseñas_container = ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Text("Reseñas de usuarios", color=COLOR_TEXTO, size=18, weight=ft.FontWeight.BOLD),
                        margin=ft.margin.only(bottom=10, left=10)
                    ),
                    *[ft.Container(
                        content=ft.Row([
                            ft.CircleAvatar(content=ft.Text(r["usuario"][0], size=18), color=COLOR_TEXTO, bgcolor=COLOR_NARANJA, radius=25),
                            ft.Container(
                                content=ft.Column([
                                    ft.Text(r["usuario"], color=COLOR_TEXTO, weight=ft.FontWeight.BOLD, size=15),
                                    ft.Text(r["texto"], color=COLOR_TEXTO, size=13, expand=True),
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
                    ) for r in RESEÑAS_EJEMPLO]
                ],
                scroll=ft.ScrollMode.AUTO,
                spacing=0,
            ),
            height=400,  # Altura fija para el contenedor de reseñas
            width=900,
            border_radius=20,
            bgcolor="#1A1A1A",
            padding=ft.padding.all(20),
        )

        # --- Contenedor principal de la vista de detalle ---
        self.controls = [
            seccion_principal,
            boton_volver,
            reseñas_container,
        ]

        # Ajustar alineación de los controles en la columna
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER