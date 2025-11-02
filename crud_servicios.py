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

    ventana.grid_columnconfigure(1, weight=1)
    ventana.grid_rowconfigure(5, weight=1)

    ANCHO_CAMPOS = 40

    tk.Label(ventana, text="Nombre:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    nombre = tk.Entry(ventana, width=ANCHO_CAMPOS)
    nombre.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    tk.Label(ventana, text="Descripción:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    descripcion = tk.Entry(ventana, width=ANCHO_CAMPOS)
    descripcion.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    tk.Label(ventana, text="Precio:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    precio = tk.Entry(ventana, width=ANCHO_CAMPOS)
    precio.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    cols = ("id", "nombre", "descripcion", "precio")
    tabla = ttk.Treeview(ventana, columns=cols, show="headings", height=10)
    for col in cols:
        tabla.heading(col, text=col.capitalize())
        tabla.column(col, width=150 if col != "descripcion" else 260)
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
        print("Datos de servicios cargados.")

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

        cur.execute("SELECT COUNT(*) FROM servicios WHERE nombre=?", (n,))
        if cur.fetchone()[0] > 0:
            messagebox.showwarning("Duplicado", "Ya existe un servicio con este nombre.")
            conn.close()
            return

        cur.execute("INSERT INTO servicios (nombre, descripcion, precio) VALUES (?, ?, ?)",
                    (n, entry_descripcion.get().strip(), precio_val))
        conn.commit()
        conn.close()
        print("Commit: Servicio agregado.")

        cargar_datos()
        entry_nombre.delete(0, tk.END)
        entry_descripcion.delete(0, tk.END)
        entry_precio.delete(0, tk.END)

    def on_seleccionar(event):
        sel = tabla.selection()
        if not sel:
            return
        valores = tabla.item(sel[0])["values"]
        entry_nombre.delete(0, tk.END)
        entry_nombre.insert(0, valores[1])
        entry_descripcion.delete(0, tk.END)
        entry_descripcion.insert(0, valores[2])
        entry_precio.delete(0, tk.END)
        entry_precio.insert(0, f"{valores[3]:.2f}")
        print("Servicio seleccionado para edición.")

    tabla.bind("<<TreeviewSelect>>", on_seleccionar)

    def actualizar_servicio():
        sel = tabla.selection()
        if not sel:
            messagebox.showwarning("Advertencia", "Selecciona un servicio para actualizar.")
            return
        servicio_id = tabla.item(sel[0])["values"][0]
        try:
            precio_val = float(entry_precio.get().strip()) if entry_precio.get().strip() else 0.0
        except ValueError:
            messagebox.showwarning("Validación", "Precio inválido.")
            return
        conn = conectar()
        cur = conn.cursor()
        cur.execute("UPDATE servicios SET nombre=?, descripcion=?, precio=? WHERE id=?",
                    (entry_nombre.get().strip(), entry_descripcion.get().strip(), precio_val, servicio_id))
        conn.commit()
        conn.close()
        print("Servicio actualizado.")
        cargar_datos()

    def eliminar_servicio():
        sel = tabla.selection()
        if not sel:
            messagebox.showwarning("Advertencia", "Selecciona un servicio para eliminar.")
            return
        servicio_id = tabla.item(sel[0])["values"][0]
        if not messagebox.askyesno("Confirmar", "¿Eliminar servicio seleccionado?"):
            return
        conn = conectar()
        cur = conn.cursor()
        cur.execute("DELETE FROM servicios WHERE id=?", (servicio_id,))
        conn.commit()
        conn.close()
        print("Servicio eliminado.")
        cargar_datos()

    tk.Button(ventana, text="Agregar", bg="#a7c7e7", command=agregar_servicio, relief="groove").grid(row=3, column=0, padx=5, pady=8)
    tk.Button(ventana, text="Actualizar", bg="#a7c7e7", command=actualizar_servicio, relief="groove").grid(row=3, column=1, padx=5, pady=8)
    tk.Button(ventana, text="Eliminar", bg="#a7c7e7", command=eliminar_servicio, relief="groove").grid(row=3, column=2, padx=5, pady=8)
    tk.Button(ventana, text="Cargar", bg="#a7c7e7", command=cargar_datos, relief="groove").grid(row=3, column=3, padx=5, pady=8)

    cargar_datos()

    print("Commit: Módulo crud_servicios inicializado.")