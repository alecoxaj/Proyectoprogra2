import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import date

DB_PATH = "espacio_creativo.db"

def conectar():
    return sqlite3.connect(DB_PATH)

def ventana_ventas():
    ventana = tk.Toplevel()
    ventana.title("Ventas - Espacio Creativo")
    ventana.geometry("600x400")
    ventana.config(bg="#f7f7f7")

    tk.Label(ventana, text="Cliente ID:").grid(row=0, column=0)
    cliente = tk.Entry(ventana)
    cliente.grid(row=0, column=1)

    tk.Label(ventana, text="Servicio ID:").grid(row=1, column=0)
    servicio = tk.Entry(ventana)
    servicio.grid(row=1, column=1)

    tk.Label(ventana, text="Total:").grid(row=2, column=0)
    total = tk.Entry(ventana)
    total.grid(row=2, column=1)

    tabla = ttk.Treeview(ventana, columns=("id", "cliente_id", "servicio_id", "fecha", "total"), show="headings")
    for col in tabla["columns"]:
        tabla.heading(col, text=col.capitalize())
    tabla.grid(row=5, column=0, columnspan=4, padx=10, pady=10)