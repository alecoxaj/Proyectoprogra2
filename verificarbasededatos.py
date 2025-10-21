import sqlite3

def verificar_conexion():
    try:
        conexion = sqlite3.connect('espacio_creativo.db')
        cursor = conexion.cursor()

        print("Conexión establecida con la base de datos.")

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tablas = cursor.fetchall()

        print("\nTablas encontradas:")
        for t in tablas:
            print(" -", t[0])



