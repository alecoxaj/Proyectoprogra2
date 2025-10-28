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