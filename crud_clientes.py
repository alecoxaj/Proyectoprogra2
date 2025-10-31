import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

DB_PATH = "espacio_creativo.db"




def conectar():
    return sqlite3.connect(DB_PATH)

def ventana_clientes():
    ventana = tk.Toplevel()
    ventana.title("Gestión de Clientes - Espacio Creativo")
    ventana.geometry("600x400")
    ventana.config(bg="#f0f0f0")

    tk.Label(ventana, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
    nombre = tk.Entry(ventana, width=30)
    nombre.grid(row=0, column=1)

    tk.Label(ventana, text="Correo:").grid(row=1, column=0, padx=5, pady=5)
    correo = tk.Entry(ventana, width=30)
    correo.grid(row=1, column=1)

    tk.Label(ventana, text="Teléfono:").grid(row=2, column=0, padx=5, pady=5)
    telefono = tk.Entry(ventana, width=30)
    telefono.grid(row=2, column=1)

    tk.Label(ventana, text="Tipo de servicio:").grid(row=3, column=0, padx=5, pady=5)
    tipo = tk.Entry(ventana, width=30)
    tipo.grid(row=3, column=1)

    tabla = ttk.Treeview(ventana, columns=("id", "nombre", "correo", "telefono", "tipo_servicio"), show="headings")
    for col in tabla["columns"]:
        tabla.heading(col, text=col.capitalize())
    tabla.grid(row=6, column=0, columnspan=4, padx=10, pady=10)


    def cargar_datos():
        tabla.delete(*tabla.get_children())
        conn = conectar()
        cur = conn.cursor()
        cur.execute("SELECT * FROM clientes")
        for fila in cur.fetchall():
            tabla.insert("", tk.END, values=fila)
        conn.close()

    def agregar_cliente():
        conn = conectar()
        cur = conn.cursor()
        cur.execute("INSERT INTO clientes (nombre, correo, telefono, tipo_servicio) VALUES (?, ?, ?, ?)",
                    (nombre.get(), correo.get(), telefono.get(), tipo.get()))
        conn.commit()
        conn.close()
        messagebox.showinfo("Éxito", "Cliente agregado correctamente")
        cargar_datos()

    def eliminar_cliente():
        seleccionado = tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Advertencia", "Selecciona un cliente para eliminar.")
            return
        cliente_id = tabla.item(seleccionado)["values"][0]
        conn = conectar()
        cur = conn.cursor()
        cur.execute("DELETE FROM clientes WHERE id=?", (cliente_id,))
        conn.commit()
        conn.close()
        cargar_datos()

    def actualizar_cliente():
        seleccionado = tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Advertencia", "Selecciona un cliente para actualizar.")
            return
        cliente_id = tabla.item(seleccionado)["values"][0]
        conn = conectar()
        cur = conn.cursor()
        cur.execute("""
            UPDATE clientes SET nombre=?, correo=?, telefono=?, tipo_servicio=? WHERE id=?
        """, (nombre.get(), correo.get(), telefono.get(), tipo.get(), cliente_id))
        conn.commit()
        conn.close()
        cargar_datos()

    tk.Button(ventana, text="Agregar", bg="#a8e6cf", command=agregar_cliente).grid(row=4, column=0, padx=5, pady=5)
    tk.Button(ventana, text="Actualizar", bg="#ffd3b6", command=actualizar_cliente).grid(row=4, column=1, padx=5, pady=5)
    tk.Button(ventana, text="Eliminar", bg="#ffaaa5", command=eliminar_cliente).grid(row=4, column=2, padx=5, pady=5)
    tk.Button(ventana, text="Cargar", bg="#dcedc1", command=cargar_datos).grid(row=4, column=3, padx=5, pady=5)

    cargar_datos()