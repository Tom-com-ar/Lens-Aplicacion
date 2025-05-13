import tkinter as tk
from tkinter import ttk

class FiltrosPeliculas:
    def __init__(self, root):
        self.root = root
        self.root.title("Filtros de Películas")

        # Variables para los filtros
        self.tipo_var = tk.StringVar()
        self.duracion_var = tk.StringVar()

        # Crear interfaz
        self.crear_interfaz()

    def crear_interfaz(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Frame para filtros
        filtros_frame = ttk.LabelFrame(main_frame, text="Filtrar por", padding="10")
        filtros_frame.pack(fill=tk.X, pady=5)

        # Filtro por tipo (género)
        ttk.Label(filtros_frame, text="Tipo (Género):").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        tipos = ["Todos", "Acción", "Aventura", "Comedia", "Drama", 
                "Ciencia Ficción", "Terror", "Romance", "Animación", "Documental"]

        tipo_combobox = ttk.Combobox(
            filtros_frame, 
            textvariable=self.tipo_var,
            values=tipos,
            state="readonly",
            width=20
        )
        tipo_combobox.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        tipo_combobox.set("Todos")

        # Filtro por duración
        ttk.Label(filtros_frame, text="Duración:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

        duraciones = ["Cualquiera", "Corta (<90 min)", "Media (90-120 min)", "Larga (>120 min)"]

        duracion_combobox = ttk.Combobox(
            filtros_frame,
            textvariable=self.duracion_var,
            values=duraciones,
            state="readonly",
            width=20
        )
        duracion_combobox.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        duracion_combobox.set("Cualquiera")

        # Botones
        botones_frame = ttk.Frame(main_frame)
        botones_frame.pack(fill=tk.X, pady=10)

        ttk.Button(
            botones_frame,
            text="Aplicar Filtros",
            command=self.aplicar_filtros
        ).pack(side=tk.RIGHT, padx=5)

        ttk.Button(
            botones_frame,
            text="Limpiar Filtros",
            command=self.limpiar_filtros
        ).pack(side=tk.RIGHT, padx=5)

    def aplicar_filtros(self):
        tipo = self.tipo_var.get()
        duracion = self.duracion_var.get()

        print(f"Filtros aplicados - Tipo: {tipo}, Duración: {duracion}")
        # Aquí iría la lógica para aplicar los filtros a tu catálogo

    def limpiar_filtros(self):
        self.tipo_var.set("Todos")
        self.duracion_var.set("Cualquiera")
        print("Filtros limpiados")
        # Aquí iría la lógica para mostrar todas las películas nuevamente

# Crear y ejecutar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = FiltrosPeliculas(root)
    root.mainloop()