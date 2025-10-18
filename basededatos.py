import sqlite3

def crear_base_datos():
    conexion = sqlite3.connect('espacio_creativo.db')
    cursor = conexion.cursor()

    cursor.execute("PRAGMA foreign_keys = ON")

