import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

DB_PATH = "espacio_creativo.db"

COLOR_FONDO_VENTANA = "#FFF9E6"
COLOR_FONDO_FRAME = "#FFF3C4"
COLOR_BOTON = "#E6B325"
COLOR_TEXTO_OSCURO = "#333333"

class ServiciosView(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Gestión de Servicios - Espacio Creativo")
        self.geometry("650x420")
        self.config(bg=COLOR_FONDO_VENTANA)
        self.crear_interfaz()
        self.cargar_datos()
        print("Commit: Ventana de Servicios inicializada (POO).")

    def conectar(self):
        return sqlite3.connect(DB_PATH)

    def crear_interfaz(self):
        frame = tk.Frame(self, bg=COLOR_FONDO_FRAME, padx=15, pady=10)
        frame.pack(fill="both", expand=True, pady=10)

        tk.Label(frame, text="Nombre:", bg=COLOR_FONDO_FRAME, fg=COLOR_TEXTO_OSCURO).grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.entry_nombre = tk.Entry(frame, width=40)
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Descripción:", bg=COLOR_FONDO_FRAME, fg=COLOR_TEXTO_OSCURO).grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.entry_descripcion = tk.Entry(frame, width=40)
        self.entry_descripcion.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="Precio:", bg=COLOR_FONDO_FRAME, fg=COLOR_TEXTO_OSCURO).grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.entry_precio = tk.Entry(frame, width=20)
        self.entry_precio.grid(row=2, column=1, padx=5, pady=5)

        tk.Button(frame, text="Agregar", bg=COLOR_BOTON, fg=COLOR_TEXTO_OSCURO, relief="flat", command=self.agregar_servicio).grid(row=3, column=0, pady=10)
        tk.Button(frame, text="Actualizar", bg="#FFD966", fg=COLOR_TEXTO_OSCURO, relief="flat", command=self.actualizar_servicio).grid(row=3, column=1, pady=10)
        tk.Button(frame, text="Eliminar", bg="#F4B183", fg=COLOR_TEXTO_OSCURO, relief="flat", command=self.eliminar_servicio).grid(row=3, column=2, pady=10)
        tk.Button(frame, text="Cargar", bg="#A9D18E", fg=COLOR_TEXTO_OSCURO, relief="flat", command=self.cargar_datos).grid(row=3, column=3, pady=10)

        columnas = ("id", "nombre", "descripcion", "precio")
        self.tabla = ttk.Treeview(frame, columns=columnas, show="headings", height=10)
        for col in columnas:
            self.tabla.heading(col, text=col.capitalize())
            self.tabla.column(col, width=150 if col != "descripcion" else 250)
        self.tabla.grid(row=5, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_fila)

    def cargar_datos(self):
        self.tabla.delete(*self.tabla.get_children())
        conn = self.conectar()
        cur = conn.cursor()
        cur.execute("SELECT * FROM servicios")
        for fila in cur.fetchall():
            self.tabla.insert("", tk.END, values=fila)
        conn.close()
        print("Datos de servicios cargados.")

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
            messagebox.showerror("Error", "El precio debe ser un número.")
            return

        conn = self.conectar()
        cur = conn.cursor()
        cur.execute("INSERT INTO servicios (nombre, descripcion, precio) VALUES (?, ?, ?)",
                    (nombre, descripcion, precio_valor))
        conn.commit()
        conn.close()
        self.cargar_datos()
        self.limpiar_campos()
        print("Servicio agregado exitosamente.")

    def actualizar_servicio(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona un servicio para actualizar.")
            return

        servicio_id = self.tabla.item(seleccion[0])["values"][0]
        conn = self.conectar()
        cur = conn.cursor()
        cur.execute("UPDATE servicios SET nombre=?, descripcion=?, precio=? WHERE id=?",
                    (self.entry_nombre.get(), self.entry_descripcion.get(), float(self.entry_precio.get()), servicio_id))
        conn.commit()
        conn.close()
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

        conn = self.conectar()
        cur = conn.cursor()
        cur.execute("DELETE FROM servicios WHERE id=?", (servicio_id,))
        conn.commit()
        conn.close()
        self.cargar_datos()
        print("Servicio eliminado correctamente.")

    def seleccionar_fila(self, event):
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

    def limpiar_campos(self):
        self.entry_nombre.delete(0, tk.END)
        self.entry_descripcion.delete(0, tk.END)
        self.entry_precio.delete(0, tk.END)