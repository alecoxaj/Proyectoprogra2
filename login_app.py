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

def iniciar_sesion():
    usuario = entry_usuario.get()
    contraseña = entry_contraseña.get()

    if not usuario or not contraseña:
        messagebox.showwarning("Campos vacíos", "Por favor ingresa usuario y contraseña.")
        print("Commit: Intento de inicio sin datos completos.")
        return

    rol = verificar_login(usuario, contraseña)
    if rol:
        messagebox.showinfo("Acceso concedido", f"Bienvenido al sistema ({rol})")
        ventana_principal(rol)
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")

root = tk.Tk()
root.title("Login - Espacio Creativo")
root.geometry("350x250")
root.config(bg="#dfe3ee")

tk.Label(root, text="Inicio de sesión", font=("Arial", 16, "bold"), bg="#dfe3ee").pack(pady=10)

tk.Label(root, text="Usuario:", bg="#dfe3ee").pack()
entry_usuario = tk.Entry(root, width=30)
entry_usuario.pack()

tk.Label(root, text="Contraseña:", bg="#dfe3ee").pack()
entry_contraseña = tk.Entry(root, width=30, show="*")
entry_contraseña.pack()

tk.Button(root, text="Ingresar", command=iniciar_sesion, bg="#a7c7e7", relief="groove").pack(pady=15)

tk.Label(root, text="Usuario: admin | Contraseña: 1234", font=("Arial", 8), bg="#dfe3ee").pack(side="bottom", pady=10)

print("Commit: Interfaz de login inicializada.")
root.mainloop()