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

    def generar_reporte():
        tabla.delete(*tabla.get_children())
        conn = conectar()
        cur = conn.cursor()
        cur.execute("""
                    SELECT s.nombre AS servicio, COUNT(v.id) AS ventas, SUM(v.total) AS ingresos
                    FROM servicios s
                             LEFT JOIN ventas v ON s.id = v.servicio_id
                    GROUP BY s.id
                    """)
        for fila in cur.fetchall():
            tabla.insert("", tk.END, values=fila)
        conn.close()
        print("Commit: Reporte generado correctamente.")

    tk.Button(ventana, text="Generar reporte", command=generar_reporte, bg="#a8e6cf").pack(pady=10)