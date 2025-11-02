import tkinter as tk
from tkinter import ttk
import sqlite3

DB_PATH = "espacio_creativo.db"

def conectar():
    return sqlite3.connect(DB_PATH)

def ventana_reportes():
    ventana = tk.Toplevel()
    ventana.title("Reportes - Espacio Creativo")
    ventana.geometry("600x400")

    tabla = ttk.Treeview(ventana, columns=("servicio", "ventas", "ingresos"), show="headings")
    for col in tabla["columns"]:
        tabla.heading(col, text=col.capitalize())
    tabla.pack(padx=10, pady=10, fill="both", expand=True)