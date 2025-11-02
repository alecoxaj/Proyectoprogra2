import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

DB_PATH = "espacio_creativo.db"

COLOR_FONDO_VENTANA = "#FFF9E6"
COLOR_FONDO_FRAME = "#FFF3C4"
COLOR_BOTON = "#E6B325"
COLOR_TEXTO_OSCURO = "#333333"

class ClientesView(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Gestión de Clientes - Espacio Creativo")
        self.geometry("700x420")
        self.config(bg=COLOR_FONDO_VENTANA)
        self.crear_interfaz()
        self.cargar_datos()
        print("Ventana de Clientes inicializada (POO).")

    def conectar(self):
        return sqlite3.connect(DB_PATH)

    def crear_interfaz(self):
        frame = tk.Frame(self, bg=COLOR_FONDO_FRAME, padx=15, pady=10)
        frame.pack(fill="both", expand=True, pady=10)

        tk.Label(frame, text="Nombre:", bg=COLOR_FONDO_FRAME, fg=COLOR_TEXTO_OSCURO).grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.entry_nombre = tk.Entry(frame, width=40)
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Correo:", bg=COLOR_FONDO_FRAME, fg=COLOR_TEXTO_OSCURO).grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.entry_correo = tk.Entry(frame, width=40)
        self.entry_correo.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="Teléfono:", bg=COLOR_FONDO_FRAME, fg=COLOR_TEXTO_OSCURO).grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.entry_telefono = tk.Entry(frame, width=40)
        self.entry_telefono.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(frame, text="Tipo de servicio:", bg=COLOR_FONDO_FRAME, fg=COLOR_TEXTO_OSCURO).grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.entry_tipo = tk.Entry(frame, width=40)
        self.entry_tipo.grid(row=3, column=1, padx=5, pady=5)

        tk.Button(frame, text="Agregar", bg=COLOR_BOTON, fg=COLOR_TEXTO_OSCURO, relief="flat", command=self.agregar_cliente).grid(row=4, column=0, pady=10)
        tk.Button(frame, text="Actualizar", bg="#FFD966", fg=COLOR_TEXTO_OSCURO, relief="flat", command=self.actualizar_cliente).grid(row=4, column=1, pady=10)
        tk.Button(frame, text="Eliminar", bg="#F4B183", fg=COLOR_TEXTO_OSCURO, relief="flat", command=self.eliminar_cliente).grid(row=4, column=2, pady=10)
        tk.Button(frame, text="Cargar", bg="#A9D18E", fg=COLOR_TEXTO_OSCURO, relief="flat", command=self.cargar_datos).grid(row=4, column=3, pady=10)

        columnas = ("id", "nombre", "correo", "telefono", "tipo_servicio")
        self.tabla = ttk.Treeview(frame, columns=columnas, show="headings", height=10)

        for col in columnas:
            self.tabla.heading(col, text=col.capitalize())
            self.tabla.column(col, width=120 if col != "nombre" else 180)

        self.tabla.grid(row=5, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_fila)

    def cargar_datos(self):
        self.tabla.delete(*self.tabla.get_children())
        conn = self.conectar()
        cur = conn.cursor()
        cur.execute("SELECT * FROM clientes")
        for fila in cur.fetchall():
            self.tabla.insert("", tk.END, values=fila)
        conn.close()
        print("Commit: Datos de clientes cargados.")

    def agregar_cliente(self):
        nombre = self.entry_nombre.get().strip()
        correo = self.entry_correo.get().strip()
        telefono = self.entry_telefono.get().strip()
        tipo = self.entry_tipo.get().strip()

        if not nombre:
            messagebox.showwarning("Campo obligatorio", "El campo 'Nombre' es obligatorio.")
            return

        conn = self.conectar()
        cur = conn.cursor()
        cur.execute("INSERT INTO clientes (nombre, correo, telefono, tipo_servicio) VALUES (?, ?, ?, ?)",
                    (nombre, correo, telefono, tipo))
        conn.commit()
        conn.close()
        self.cargar_datos()
        self.limpiar_campos()
        print("Cliente agregado exitosamente.")

    def actualizar_cliente(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona un cliente para actualizar.")
            return

        cliente_id = self.tabla.item(seleccion[0])["values"][0]
        conn = self.conectar()
        cur = conn.cursor()
        cur.execute("UPDATE clientes SET nombre=?, correo=?, telefono=?, tipo_servicio=? WHERE id=?",
                    (self.entry_nombre.get(), self.entry_correo.get(),
                     self.entry_telefono.get(), self.entry_tipo.get(), cliente_id))
        conn.commit()
        conn.close()
        self.cargar_datos()
        print("Cliente actualizado correctamente.")

    def eliminar_cliente(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona un cliente para eliminar.")
            return

        cliente_id = self.tabla.item(seleccion[0])["values"][0]
        if not messagebox.askyesno("Confirmar", "¿Deseas eliminar este cliente?"):
            return

        conn = self.conectar()
        cur = conn.cursor()
        cur.execute("DELETE FROM clientes WHERE id=?", (cliente_id,))
        conn.commit()
        conn.close()
        self.cargar_datos()
        print("Cliente eliminado correctamente.")

    def seleccionar_fila(self, event):
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        valores = self.tabla.item(seleccion[0])["values"]
        self.entry_nombre.delete(0, tk.END)
        self.entry_nombre.insert(0, valores[1])
        self.entry_correo.delete(0, tk.END)
        self.entry_correo.insert(0, valores[2])
        self.entry_telefono.delete(0, tk.END)
        self.entry_telefono.insert(0, valores[3])
        self.entry_tipo.delete(0, tk.END)
        self.entry_tipo.insert(0, valores[4])
        print("Cliente seleccionado para edición.")

    def limpiar_campos(self):
        self.entry_nombre.delete(0, tk.END)
        self.entry_correo.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)
        self.entry_tipo.delete(0, tk.END)