import sqlite3

def verificar_conexion():
    try:
        conexion = sqlite3.connect('espacio_creativo.db')
        cursor = conexion.cursor()

        print("Conexión establecida con la base de datos.")

