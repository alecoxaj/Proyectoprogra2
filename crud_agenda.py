import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

DB_PATH = "espacio_creativo.db"

def conectar():
    return sqlite3.connect(DB_PATH)

def ventana_agenda():
    ventana = tk.Toplevel()
    ventana.title("Agenda - Espacio Creativo")
    ventana.geometry("700x400")
    ventana.config(bg="#f7f7f7")

    tk.Label(ventana, text="Cliente ID:").grid(row=0, column=0)
    cliente_id = tk.Entry(ventana)
    cliente_id.grid(row=0, column=1)

    tk.Label(ventana, text="Servicio ID:").grid(row=1, column=0)
    servicio_id = tk.Entry(ventana)
    servicio_id.grid(row=1, column=1)

    tk.Label(ventana, text="Fecha (YYYY-MM-DD):").grid(row=2, column=0)
    fecha = tk.Entry(ventana)
    fecha.grid(row=2, column=1)

    tk.Label(ventana, text="Estado:").grid(row=3, column=0)
    estado = tk.Entry(ventana)
    estado.insert(0, "Pendiente")
    estado.grid(row=3, column=1)

    tabla = ttk.Treeview(ventana, columns=("id", "cliente_id", "servicio_id", "fecha", "estado"), show="headings")
    for col in tabla["columns"]:
        tabla.heading(col, text=col.capitalize())
    tabla.grid(row=6, column=0, columnspan=4, padx=10, pady=10)

    def cargar_datos():
        tabla.delete(*tabla.get_children())
        conn = conectar()
        cur = conn.cursor()
        cur.execute("SELECT * FROM agenda")
        for fila in cur.fetchall():
            tabla.insert("", tk.END, values=fila)
        conn.close()
        print("Commit: Datos de agenda cargados.")