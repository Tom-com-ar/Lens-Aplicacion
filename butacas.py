import tkinter as tk
from tkinter import messagebox

class CineApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Reservas de Cine")
        self.root.geometry("800x600")

        # Configuración de colores
        self.color_disponible = '#f0f0f0'  # Gris claro
        self.color_seleccionado = 'orange'  # Celeste para butacas seleccionadas
        self.color_ocupado = 'gray'

        # Configuración de butacas
        self.butacas_seleccionadas = set()
        self.butacas_ocupadas = {'A3', 'B5', 'C7', 'D2', 'E9', 'F4', 'G6'}  # Ejemplo de butacas ocupadas
        self.botones_butacas = {}  # Diccionario para guardar referencias a los botones

        # Interfaz
        self.crear_widgets()

    def crear_widgets(self):
        # Marco principal
        main_frame = tk.Frame(self.root)
        main_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        # Título
        tk.Label(main_frame, text="SELECCIÓN DE BUTACAS", font=('Arial', 16, 'bold')).pack(pady=10)

        # Marco para la pantalla del cine
        screen_frame = tk.Frame(main_frame, bg='gray', height=30)
        screen_frame.pack(fill=tk.X, pady=(0, 20))
        tk.Label(screen_frame, text="PANTALLA", bg='gray', fg='white', 
                font=('Arial', 12, 'bold')).pack(pady=5)

        # Marco para las butacas
        seats_frame = tk.Frame(main_frame)
        seats_frame.pack(fill=tk.BOTH, expand=True)

        # Crear butacas (filas A-J, columnas 1-10)
        for row_idx, letra in enumerate(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']):
            row_frame = tk.Frame(seats_frame)
            row_frame.pack(fill=tk.X, pady=2)

            tk.Label(row_frame, text=letra, width=2).pack(side=tk.LEFT)

            for col in range(1, 11):
                butaca = f"{letra}{col}"
                estado = 'normal' if butaca not in self.butacas_ocupadas else 'disabled'
                color = self.color_disponible if butaca not in self.butacas_ocupadas else self.color_ocupado

                btn = tk.Button(
                    row_frame,
                    text=str(col),
                    width=3,
                    state=estado,
                    bg=color,
                    command=lambda b=butaca: self.toggle_seleccion(b)
                )
                btn.pack(side=tk.LEFT, padx=2)
                self.botones_butacas[butaca] = btn  # Guardar referencia al botón

        # Leyenda
        legend_frame = tk.Frame(main_frame)
        legend_frame.pack(pady=10)

        tk.Label(legend_frame, text="Leyenda:").pack(side=tk.LEFT)
        tk.Label(legend_frame, text="Disponible", bg=self.color_disponible, width=10).pack(side=tk.LEFT, padx=5)
        tk.Label(legend_frame, text="Seleccionado", bg=self.color_seleccionado, width=10).pack(side=tk.LEFT, padx=5)
        tk.Label(legend_frame, text="Ocupado", bg=self.color_ocupado, width=10).pack(side=tk.LEFT, padx=5)

        # Botones de acción
        action_frame = tk.Frame(main_frame)
        action_frame.pack(pady=20)

        tk.Button(
            action_frame,
            text="Comprar Entradas",
            command=self.comprar_entradas,
            bg='lightgreen',
            font=('Arial', 12, 'bold'),
            padx=20
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            action_frame,
            text="Limpiar Selección",
            command=self.limpiar_seleccion,
            bg='lightcoral',
            font=('Arial', 12),
            padx=20
        ).pack(side=tk.LEFT, padx=10)

    def toggle_seleccion(self, butaca):
        if butaca in self.butacas_seleccionadas:
            self.butacas_seleccionadas.remove(butaca)
            self.botones_butacas[butaca].config(bg=self.color_disponible)
        else:
            self.butacas_seleccionadas.add(butaca)
            self.botones_butacas[butaca].config(bg=self.color_seleccionado)

    def comprar_entradas(self):
        if not self.butacas_seleccionadas:
            messagebox.showwarning("Advertencia", "Por favor seleccione al menos una butaca")
            return

        respuesta = messagebox.askyesno(
            "Confirmar Compra",
            f"¿Confirmar compra de butacas: {', '.join(sorted(self.butacas_seleccionadas))}?"
        )

        if respuesta:
            messagebox.showinfo("Éxito", "Compra realizada con éxito!")
            for butaca in self.butacas_seleccionadas:
                self.botones_butacas[butaca].config(bg=self.color_ocupado, state='disabled')
            self.butacas_ocupadas.update(self.butacas_seleccionadas)
            self.butacas_seleccionadas.clear()

    def limpiar_seleccion(self):
        for butaca in list(self.butacas_seleccionadas):
            self.botones_butacas[butaca].config(bg=self.color_disponible)
        self.butacas_seleccionadas.clear()

if __name__ == "__main__":
    root = tk.Tk()
    app = CineApp(root)
    root.mainloop()