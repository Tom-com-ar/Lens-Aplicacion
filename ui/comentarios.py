import tkinter as tk

class ComentariosUI(tk.Frame):
    def __init__(self, master=None, pelicula=None):
        super().__init__(master)
        self.pelicula = pelicula
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # Aquí irán los widgets para los comentarios
        pass 