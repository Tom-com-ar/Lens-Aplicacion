import tkinter as tk
from tkinter import font

class ComentariosUI(tk.Frame):
    def __init__(self, master=None, pelicula=None):
        super().__init__(master, bg="#000000")
        self.pelicula = pelicula
        self.pack(fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self):
        # Fuente grande y negrita para el título
        titulo_font = font.Font(family="Arial", size=22, weight="bold")
        label_font = font.Font(family="Arial", size=12, weight="bold")

        # Título
        titulo = tk.Label(self, text="Deja aqui tu reseña de la pelicula !!!!!", bg="#000000", fg="#FFFFFF", font=titulo_font)
        titulo.pack(pady=(20, 20))

        # Nombre de la persona
        frame_nombre = tk.Frame(self, bg="#000000")
        frame_nombre.pack(pady=(0, 10), padx=40, fill="x")
        label_nombre = tk.Label(frame_nombre, text="Nombre de la persona:", bg="#D9D9D9", fg="#000000", font=label_font, anchor="w")
        label_nombre.pack(fill="x", padx=0, pady=0)
        entry_nombre = tk.Entry(frame_nombre, bg="#D9D9D9", fg="#000000", relief="flat", font=("Arial", 12))
        entry_nombre.pack(fill="x", padx=0, pady=0, ipady=4)

        # Nombre de la película
        frame_pelicula = tk.Frame(self, bg="#000000")
        frame_pelicula.pack(pady=(0, 10), padx=40, fill="x")
        label_pelicula = tk.Label(frame_pelicula, text="Nombre de la pelicula:", bg="#D9D9D9", fg="#000000", font=label_font, anchor="w")
        label_pelicula.pack(fill="x", padx=0, pady=0)
        entry_pelicula = tk.Entry(frame_pelicula, bg="#D9D9D9", fg="#000000", relief="flat", font=("Arial", 12))
        entry_pelicula.pack(fill="x", padx=0, pady=0, ipady=4)

        # Reseña
        frame_resena = tk.Frame(self, bg="#000000")
        frame_resena.pack(pady=(0, 10), padx=40, fill="both", expand=True)
        label_resena = tk.Label(frame_resena, text="Reseña de la pelicula:", bg="#D9D9D9", fg="#000000", font=label_font, anchor="w")
        label_resena.pack(fill="x", padx=0, pady=0)
        text_resena = tk.Text(frame_resena, bg="#D9D9D9", fg="#000000", relief="flat", font=("Arial", 12), height=10, wrap="word")
        text_resena.pack(fill="both", padx=0, pady=0, expand=True)

        # Bordes redondeados no son nativos en Tkinter, pero el efecto visual se logra con el color y padding.

# Para probar la interfaz:
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Comentarios")
    root.geometry("900x500")
    app = ComentariosUI(master=root)
    app.mainloop()