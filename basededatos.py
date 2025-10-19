import sqlite3

def crear_base_datos():
    conexion = sqlite3.connect("espacio_creativo.db")
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

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        correo TEXT,
        telefono TEXT,
        tipo_servicio TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS servicios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        descripcion TEXT,
        precio REAL NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS agenda (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER NOT NULL,
        servicio_id INTEGER NOT NULL,
        fecha TEXT NOT NULL,
        estado TEXT DEFAULT 'Pendiente',
        FOREIGN KEY (cliente_id) REFERENCES clientes(id),
        FOREIGN KEY (servicio_id) REFERENCES servicios(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ventas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER NOT NULL,
        servicio_id INTEGER NOT NULL,
        fecha TEXT NOT NULL,
        total REAL NOT NULL,
        FOREIGN KEY (cliente_id) REFERENCES clientes(id),
        FOREIGN KEY (servicio_id) REFERENCES servicios(id)
    )
    """)

    cursor.execute("""
    INSERT OR IGNORE INTO usuarios (nombre, usuario, contraseña, rol)
    VALUES ('Administrador', 'admin', '1234', 'admin')
    """)

    conexion.commit()
    conexion.close()
    print("Base de datos creada correctamente (espacio_creativo.db)")

if __name__ == "__main__":
    crear_base_datos()