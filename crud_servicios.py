import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

DB_PATH = "espacio_creativo.db"

def conectar():
    return sqlite3.connect(DB_PATH)

def ventana_servicios():
    ventana = tk.Toplevel()
    ventana.title("Gestión de Servicios - Espacio Creativo")
    ventana.geometry("650x420")
    ventana.config(bg="#f0f0f0")

    tk.Label(ventana, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entry_nombre = tk.Entry(ventana, width=45)
    entry_nombre.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(ventana, text="Descripción:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    entry_descripcion = tk.Entry(ventana, width=45)
    entry_descripcion.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(ventana, text="Precio:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    entry_precio = tk.Entry(ventana, width=20)
    entry_precio.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    cols = ("id", "nombre", "descripcion", "precio")
    tabla = ttk.Treeview(ventana, columns=cols, show="headings", height=10)
    for col in cols:
        tabla.heading(col, text=col.capitalize())
        tabla.column(col, width=150 if col!="descripcion" else 260)
    tabla.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

    scrollbar = ttk.Scrollbar(ventana, orient="vertical", command=tabla.yview)
    tabla.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=5, column=3, sticky="ns", pady=10)

    def cargar_datos():
        tabla.delete(*tabla.get_children())
        conn = conectar()
        cur = conn.cursor()
        cur.execute("SELECT * FROM servicios")
        for fila in cur.fetchall():
            tabla.insert("", tk.END, values=fila)
        conn.close()
        print("Commit: Datos de servicios cargados.")

    def agregar_servicio():
        n = entry_nombre.get().strip()
        p = entry_precio.get().strip()
        if not n:
            messagebox.showwarning("Validación", "El nombre es obligatorio.")
            return
        try:
            precio_val = float(p) if p else 0.0
        except ValueError:
            messagebox.showwarning("Validación", "Precio inválido.")
            return
        conn = conectar()
        cur = conn.cursor()
        cur.execute("INSERT INTO servicios (nombre, descripcion, precio) VALUES (?, ?, ?)",
                    (n, entry_descripcion.get().strip(), precio_val))
        conn.commit()
        conn.close()
        print("Commit: Servicio agregado.")
        cargar_datos()
        entry_nombre.delete(0, tk.END)
        entry_descripcion.delete(0, tk.END)
        entry_precio.delete(0, tk.END)

    tk.Button(ventana, text="Agregar", bg="#a8e6cf", command=agregar_servicio).grid(row=3, column=0, padx=5, pady=8)