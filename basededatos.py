import sqlite3

def crear_base_datos():
    conexion = sqlite3.connect('espacio_creativo.db')
    cursor = conexion.cursor()

    cursor.execute("PRAGMA foreign_keys = ON")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            usuario TEXT UNIQUE NOT NULL,
            contraseña TEXT NOT NULL,
            rol TEXT CHECK(rol IN ('admin', 'usuario')) NOT NULL
        )
        """)

