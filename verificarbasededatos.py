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

        print("\nUsuarios registrados:")
        cursor.execute("SELECT id, nombre, usuario, rol FROM usuarios;")
        usuarios = cursor.fetchall()
        if usuarios:
            for u in usuarios:
                print(f"   ID: {u[0]} | Nombre: {u[1]} | Usuario: {u[2]} | Rol: {u[3]}")
        else:
            print("No hay usuarios registrados.")

        conexion.close()
        print("\nConexión cerrada correctamente.")

    except sqlite3.Error as e:
        print("Error al conectar con la base de datos:", e)

if __name__ == "__main__":
    verificar_conexion()



