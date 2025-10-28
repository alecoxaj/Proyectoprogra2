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