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
    contraseña = tk.Entry(ventana, width=25, show="*")
    contraseña.grid(row=2, column=1)

    tk.Label(ventana, text="Rol (admin/usuario):").grid(row=3, column=0, padx=5, pady=5)
    rol = tk.Entry(ventana, width=25)
    rol.grid(row=3, column=1)

    tabla = ttk.Treeview(ventana, columns=("id", "nombre", "usuario", "rol"), show="headings")
    for col in tabla["columns"]:
        tabla.heading(col, text=col.capitalize())
    tabla.grid(row=6, column=0, columnspan=4, padx=10, pady=10)

