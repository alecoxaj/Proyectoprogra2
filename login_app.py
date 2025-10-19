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

