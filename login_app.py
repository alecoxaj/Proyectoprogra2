import tkinter as tk
from tkinter import messagebox, PhotoImage
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
    ventana.geometry("400x350")
    ventana.config(bg="#ffa420")

    tk.Label(
        ventana,
        text=f"Bienvenido, rol: {rol}",
        font=("Arial", 14, "bold"),
        bg="#ffa420"
    ).pack(pady=20)

    if rol == "admin":
        opciones = ["Gestión de Usuarios", "Clientes", "Servicios", "Agenda", "Ventas", "Reportes"]
    else:
        opciones = ["Clientes", "Agenda", "Ventas"]


    for opcion in opciones:
        tk.Button(
            ventana,
            text=opcion,
            width=25,
            bg="#fff3cd",
            relief="groove",
            font=("Arial", 10)
        ).pack(pady=5)


    tk.Button(
        ventana,
        text="Cerrar sesión",
        command=ventana.destroy,
        bg="#f8d7da"
    ).pack(pady=20)

    print(f"Menú cargado para el rol '{rol}'.")


def iniciar_sesion():
    usuario = entry_usuario.get()
    contraseña = entry_contraseña.get()

    if not usuario or not contraseña:
        messagebox.showwarning("Campos vacíos", "Por favor ingresa usuario y contraseña.")
        print("Intento de inicio sin datos completos.")
        return

    rol = verificar_login(usuario, contraseña)
    if rol:
        messagebox.showinfo("Acceso concedido", f"Bienvenido al sistema ({rol})")
        ventana_principal(rol)
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")


root = tk.Tk()
root.title("Login - Espacio Creativo")
root.geometry("900x600")
root.config(bg="#faeecb")
root.resizable(False, False)


try:
    logo = PhotoImage(file="Espacio.blanco.png")
    logo = logo.subsample(3)
    tk.Label(root, image=logo, bg="#faeecb").pack(pady=(40, 10))
except Exception as e:
    print("No se pudo cargar el logo:", e)

frame = tk.Frame(root, bg="#ffe08a", bd=0, highlightthickness=4, highlightbackground="#f6b100")
frame.pack(pady=10)
frame.config(width=500, height=300)
frame.pack_propagate(False)


tk.Label(
    frame,
    text="Inicio de sesión",
    font=("Arial", 16, "bold"),
    bg="#ffe08a",
    fg="#333"
).pack(pady=(20, 15))


tk.Label(frame, text="Usuario:", font=("Arial", 12), bg="#ffe08a", fg="#333").pack()
entry_usuario = tk.Entry(frame, font=("Arial", 12), width=30, relief="flat", bd=3, justify="center")
entry_usuario.pack(pady=5)


tk.Label(frame, text="Contraseña:", font=("Arial", 12), bg="#ffe08a", fg="#333").pack()
entry_contraseña = tk.Entry(frame, font=("Arial", 12), width=30, show="*", relief="flat", bd=3, justify="center")
entry_contraseña.pack(pady=5)


tk.Button(
    frame,
    text="Ingresar",
    font=("Arial", 12, "bold"),
    bg="#f6b100",
    fg="white",
    activebackground="#e0a000",
    activeforeground="white",
    relief="flat",
    width=15,
    height=1,
    command=iniciar_sesion
).pack(pady=20)

# Texto inferior
tk.Label(
    frame,
    text="Usuario: admin  |  Contraseña: 1234",
    font=("Arial", 9),
    bg="#ffe08a",
    fg="#7a5900"
).pack()


print("Interfaz de login inicializada.")
root.mainloop()
