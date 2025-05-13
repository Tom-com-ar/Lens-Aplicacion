import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import requests
from io import BytesIO

API_KEY = "e6822a7ed386f7102b6a857ea5e3c17f"

# Obtener películas populares
def get_movies():
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}&language=es-ES&page=1"
    response = requests.get(url)
    return response.json().get('results', [])

# Redondear imagen
def round_corners(img, radius):
    circle = Image.new('L', (radius * 2, radius * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, radius * 2, radius * 2), fill=255)

    alpha = Image.new('L', img.size, 255)
    w, h = img.size

    alpha.paste(circle.crop((0, 0, radius, radius)), (0, 0))
    alpha.paste(circle.crop((0, radius, radius, radius * 2)), (0, h - radius))
    alpha.paste(circle.crop((radius, 0, radius * 2, radius)), (w - radius, 0))
    alpha.paste(circle.crop((radius, radius, radius * 2, radius * 2)), (w - radius, h - radius))

    img.putalpha(alpha)
    return img

# Mostrar películas
def show_movies():
    movies = get_movies()
    images.clear()

    for index, movie in enumerate(movies[:100]):  # Mostrar 100
        poster_path = movie['poster_path']
        title = movie['title']
        release_date = movie['release_date'][:4]

        # Cargar imagen
        img_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
        img_data = requests.get(img_url).content
        img = Image.open(BytesIO(img_data)).convert("RGBA")
        img = img.resize((175, 300))

        # Redondear bordes
        img = round_corners(img, 25)
        img_tk = ImageTk.PhotoImage(img)
        images.append(img_tk)

        # Frame
        movie_frame = tk.Frame(inner_frame, bg='#1e1e1e')
        movie_frame.grid(row=index//6, column=index%6, padx=25, pady=25)

        # Poster
        poster_label = tk.Label(movie_frame, image=img_tk, bg='#1e1e1e')
        poster_label.pack()

        # Título
        title_label = tk.Label(movie_frame, text=title, bg='#1e1e1e', fg='white', font=('Arial', 10), wraplength=175)
        title_label.pack(pady=5)

# Crear ventana
root = tk.Tk()
root.title("Catálogo de Películas")
root.configure(bg='#1e1e1e')
root.state('zoomed')

# Logo
logo_label = tk.Label(root, text="LOGO", bg='#1e1e1e', fg='white', font=('Arial', 20))
logo_label.place(x=30, y=20)

# 🟠 Barra búsqueda en esquina superior derecha
search_canvas = tk.Canvas(root, width=300, height=35, bg='#1e1e1e', highlightthickness=0)
search_canvas.place(relx=1.0, x=-320, y=26, anchor="ne")  # ESQUINA DERECHA

search_canvas.create_oval(0, 0, 35, 35, fill='#FF9900', outline='#FF9900')
search_canvas.create_oval(300-35, 0, 300, 35, fill='#FF9900', outline='#FF9900')
search_canvas.create_rectangle(17, 0, 300-17, 35, fill='#FF9900', outline='#FF9900')

search_entry = tk.Entry(root, font=('Arial', 12), bd=0, relief='flat', bg='#FF9900', fg='black')
search_entry.place(relx=1.0, x=-300, y=30, width=220, height=25, anchor="ne")

search_btn = tk.Button(root, text="🔍", font=('Arial', 12), bg='#FF9900', fg='black', bd=0, relief='flat', cursor="hand2")
search_btn.place(relx=1.0, x=-50, y=30, anchor="ne")

# Frame + Scroll
canvas = tk.Canvas(root, bg='#1e1e1e', highlightthickness=0)
canvas.place(x=50, y=100, relwidth=0.9, relheight=0.8)

# Ocultar barra de scroll pero habilitar scroll con mouse
def _on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

canvas.bind_all("<MouseWheel>", _on_mousewheel)

inner_frame = tk.Frame(canvas, bg='#1e1e1e')
inner_frame_window = canvas.create_window((0, 0), window=inner_frame, anchor="nw")

# Centrar películas + ajustar scroll
def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox('all'))
    canvas_width = event.width
    inner_frame_width = inner_frame.winfo_reqwidth()
    x_offset = max((canvas_width - inner_frame_width) // 2, 0)
    canvas.coords(inner_frame_window, x_offset, 0)

inner_frame.bind("<Configure>", on_configure)

# Guardar imagenes
images = []
show_movies()

root.mainloop()
