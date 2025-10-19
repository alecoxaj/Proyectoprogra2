import tkinter as tk
from tkinter import messagebox
import sqlite3

DB_PATH = "espacio_creativo.db"

def verificar_login(usuario, contraseña):
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()
    cursor.execute("SELECT rol FROM usuarios WHERE usuario=? AND contraseña=?", (usuario, contraseña))
    resultado = cursor.fetchone()
    conexion.close()
    if resultado:
        print(f"Usuario '{usuario}' inició sesión como {resultado[0]}.")
        return resultado[0]
    else:
        print(f"Intento fallido de inicio de sesión con usuario '{usuario}'.")
        return None

def ventana_principal(rol):
    ventana = tk.Toplevel()
    ventana.title("Menú Principal - Espacio Creativo")
    ventana.geometry("400x250")
    ventana.config(bg="#f4f4f4")

    tk.Label(ventana, text=f"Bienvenido, rol: {rol}", font=("Arial", 14, "bold"), bg="#f4f4f4").pack(pady=20)

    if rol == "admin":
        opciones = ["Gestión de Usuarios", "Clientes", "Servicios", "Agenda", "Ventas", "Reportes"]
    else:
        opciones = ["Clientes", "Agenda", "Ventas"]

    for opcion in opciones:
        tk.Button(ventana, text=opcion, width=25, bg="#cfe2f3", relief="groove").pack(pady=5)

    tk.Button(ventana, text="Cerrar sesión", command=ventana.destroy, bg="#f8d7da").pack(pady=20)
    print(f"Commit: Menú cargado para el rol '{rol}'.")

