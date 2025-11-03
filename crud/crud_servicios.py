import tkinter as tk
from tkinter import ttk, messagebox
from core.database import DatabaseManager

COLOR_FONDO_VENTANA = "#FFF9E6"
COLOR_FONDO_FRAME = "#FFF3C4"
COLOR_BOTON = "#E6B325"
COLOR_TEXTO_OSCURO = "#333333"

class ServiciosView(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Gestión de Servicios - Espacio Creativo")
        self.geometry("700x420")
        self.config(bg=COLOR_FONDO_VENTANA)
        self.db = DatabaseManager()
        self._crear_interfaz()
        self.cargar_datos()
        print("Ventana de Servicios inicializada (POO + SOLID).")

    def _crear_interfaz(self):
        frame = tk.Frame(self, bg=COLOR_FONDO_FRAME, padx=15, pady=10)
        frame.pack(fill="both", expand=True, pady=10)

        etiquetas = ["Nombre:", "Descripción:", "Precio:"]
        for i, texto in enumerate(etiquetas):
            tk.Label(frame, text=texto, bg=COLOR_FONDO_FRAME, fg=COLOR_TEXTO_OSCURO).grid(
                row=i, column=0, sticky="e", padx=5, pady=5
            )

        self.entry_nombre = tk.Entry(frame, width=40)
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5)
        self.entry_descripcion = tk.Entry(frame, width=40)
        self.entry_descripcion.grid(row=1, column=1, padx=5, pady=5)
        self.entry_precio = tk.Entry(frame, width=20)
        self.entry_precio.grid(row=2, column=1, padx=5, pady=5)

        botones = [
            ("Agregar", self.agregar_servicio, COLOR_BOTON),
            ("Actualizar", self.actualizar_servicio, "#FFD966"),
            ("Eliminar", self.eliminar_servicio, "#F4B183"),
            ("Cargar", self.cargar_datos, "#A9D18E"),
        ]

        for i, (texto, comando, color) in enumerate(botones):
            tk.Button(frame, text=texto, bg=color, fg=COLOR_TEXTO_OSCURO, relief="flat",
                      command=comando, width=12).grid(row=3, column=i, pady=10, padx=4)

        columnas = ("id", "nombre", "descripcion", "precio")
        self.tabla = ttk.Treeview(frame, columns=columnas, show="headings", height=10)

        for col in columnas:
            self.tabla.heading(col, text=col.capitalize())
            self.tabla.column(col, width=150 if col != "descripcion" else 250)

        self.tabla.grid(row=5, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
        self.tabla.bind("<<TreeviewSelect>>", self._seleccionar_fila)

    def cargar_datos(self):
        self.tabla.delete(*self.tabla.get_children())
        try:
            cur = self.db.execute("SELECT * FROM servicios")
            for fila in cur.fetchall():
                self.tabla.insert("", tk.END, values=fila)
            print("Datos de servicios cargados correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los servicios.\n{e}")

    def agregar_servicio(self):
        nombre = self.entry_nombre.get().strip()
        descripcion = self.entry_descripcion.get().strip()
        precio = self.entry_precio.get().strip()

        if not nombre:
            messagebox.showwarning("Campo obligatorio", "El campo 'Nombre' es obligatorio.")
            return

        try:
            precio_valor = float(precio)
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser un número válido.")
            return

        sql = "INSERT INTO servicios (nombre, descripcion, precio) VALUES (?, ?, ?)"
        self.db.execute(sql, (nombre, descripcion, precio_valor), commit=True)
        self.cargar_datos()
        self._limpiar_campos()
        print("Servicio agregado exitosamente.")

    def actualizar_servicio(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona un servicio para actualizar.")
            return

        servicio_id = self.tabla.item(seleccion[0])["values"][0]
        try:
            precio_valor = float(self.entry_precio.get())
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser un número válido.")
            return

        sql = "UPDATE servicios SET nombre=?, descripcion=?, precio=? WHERE id=?"
        self.db.execute(sql, (
            self.entry_nombre.get(),
            self.entry_descripcion.get(),
            precio_valor,
            servicio_id
        ), commit=True)

        self.cargar_datos()
        print("Servicio actualizado correctamente.")

    def eliminar_servicio(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona un servicio para eliminar.")
            return

        servicio_id = self.tabla.item(seleccion[0])["values"][0]
        if not messagebox.askyesno("Confirmar", "¿Deseas eliminar este servicio?"):
            return

        sql = "DELETE FROM servicios WHERE id=?"
        self.db.execute(sql, (servicio_id,), commit=True)
        self.cargar_datos()
        print("Servicio eliminado correctamente.")

    def _seleccionar_fila(self, event):
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        valores = self.tabla.item(seleccion[0])["values"]
        self.entry_nombre.delete(0, tk.END)
        self.entry_nombre.insert(0, valores[1])
        self.entry_descripcion.delete(0, tk.END)
        self.entry_descripcion.insert(0, valores[2])
        self.entry_precio.delete(0, tk.END)
        self.entry_precio.insert(0, valores[3])
        print("Servicio seleccionado para edición.")

    def _limpiar_campos(self):
        for entry in [self.entry_nombre, self.entry_descripcion, self.entry_precio]:
            entry.delete(0, tk.END)