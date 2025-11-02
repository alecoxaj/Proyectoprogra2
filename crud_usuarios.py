import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

DB_PATH = "espacio_creativo.db"

def conectar():
    return sqlite3.connect(DB_PATH)

def ventana_usuarios():
    ventana = tk.Toplevel()
    ventana.title("Gestión de Usuarios")
    ventana.geometry("550x400")
    ventana.config(bg="#f9f9f9")

    tk.Label(ventana, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
    nombre = tk.Entry(ventana, width=25)
    nombre.grid(row=0, column=1)

    tk.Label(ventana, text="Usuario:").grid(row=1, column=0, padx=5, pady=5)
    usuario = tk.Entry(ventana, width=25)
    usuario.grid(row=1, column=1)

    tk.Label(ventana, text="Contraseña:").grid(row=2, column=0, padx=5, pady=5)
    contrasena = tk.Entry(ventana, width=25, show="*")
    contrasena.grid(row=2, column=1)

    tk.Label(ventana, text="Rol (admin/usuario):").grid(row=3, column=0, padx=5, pady=5)
    rol = tk.Entry(ventana, width=25)
    rol.grid(row=3, column=1)

    tabla = ttk.Treeview(ventana, columns=("id", "nombre", "usuario", "rol"), show="headings")
    for col in tabla["columns"]:
        tabla.heading(col, text=col.capitalize())
    tabla.grid(row=6, column=0, columnspan=4, padx=10, pady=10)

    def cargar_datos():
        tabla.delete(*tabla.get_children())
        conn = conectar()
        cur = conn.cursor()
        cur.execute("SELECT id, nombre, usuario, rol FROM usuarios")
        for fila in cur.fetchall():
            tabla.insert("", tk.END, values=fila)
        conn.close()
        print("Commit: Usuarios cargados.")


    def agregar_usuario():
        conn = conectar()
        cur = conn.cursor()
        cur.execute("INSERT INTO usuarios (nombre, usuario, contraseña, rol) VALUES (?, ?, ?, ?)",
                    (nombre.get(), usuario.get(), contrasena.get(), rol.get()))
        conn.commit()
        conn.close()
        print("Commit: Nuevo usuario agregado.")
        messagebox.showinfo("Éxito", "Usuario agregado correctamente.")
        cargar_datos()

    def eliminar_usuario():
        seleccionado = tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Advertencia", "Selecciona un usuario.")
            return
        usuario_id = tabla.item(seleccionado)["values"][0]
        conn = conectar()
        cur = conn.cursor()
        cur.execute("DELETE FROM usuarios WHERE id=?", (usuario_id,))
        conn.commit()
        conn.close()
        print("Commit: Usuario eliminado.")
        cargar_datos()
