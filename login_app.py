import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3

from crud_clientes import ventana_clientes
from crud_servicios import ventana_servicios
from crud_usuarios import ventana_usuarios
from crud_agenda import ventana_agenda
from crud_ventas import ventana_ventas
from crud_reportes import ventana_reportes

DB_PATH = "espacio_creativo.db"

COLOR_FONDO_VENTANA = "#FFF9E6"
COLOR_FONDO_FRAME = "#FFF3C4"
COLOR_BOTON = "#E6B325"
COLOR_TEXTO_OSCURO = "#333333"
COLOR_TEXTO_BLANCO = "#FFFFFF"


def verificar_login(usuario, contraseña):
    try:
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()
        cursor.execute("SELECT rol FROM usuarios WHERE usuario=? AND contraseña=?", (usuario, contraseña))
        resultado = cursor.fetchone()
        conexion.close()
        if resultado:
            print(f"Commit: Usuario '{usuario}' inició sesión como {resultado[0]}.")
            return resultado[0]
        else:
            print(f"Commit: Intento fallido de inicio de sesión con usuario '{usuario}'.")
            return None
    except Exception as e:
        messagebox.showerror("Error de conexión", f"No se pudo acceder a la base de datos:\n{e}")
        return None


def ventana_principal(rol, root):
    menu = tk.Toplevel(root)
    menu.title("Menú Principal - Espacio Creativo")
    menu.geometry("450x400")
    menu.config(bg=COLOR_FONDO_VENTANA)

    tk.Label(menu, text=f"Bienvenido ({rol})",
             font=("Arial", 14, "bold"),
             bg=COLOR_FONDO_VENTANA,
             fg=COLOR_TEXTO_OSCURO
             ).pack(pady=15)

    if rol == "admin":
        opciones = [
            ("Gestión de Usuarios", ventana_usuarios),
            ("Clientes", ventana_clientes),
            ("Servicios", ventana_servicios),
            ("Agenda", ventana_agenda),
            ("Ventas", ventana_ventas),
            ("Reportes", ventana_reportes)
        ]
    else:
        opciones = [
            ("Clientes", ventana_clientes),
            ("Agenda", ventana_agenda),
            ("Ventas", ventana_ventas)
        ]

    for texto, comando in opciones:
        tk.Button(menu, text=texto, width=25, bg=COLOR_BOTON,
                  fg=COLOR_TEXTO_OSCURO, relief="ridge",
                  font=("Arial", 11, "bold"),
                  command=comando).pack(pady=5)

    tk.Button(menu, text="Cerrar sesión",
              command=lambda: [menu.destroy(), root.deiconify()],
              bg=COLOR_BOTON, fg=COLOR_TEXTO_OSCURO,
              font=("Arial", 11, "bold"),
              relief="flat").pack(pady=15)

    print(f"Commit: Menú principal cargado para el rol '{rol}'.")


def iniciar_sesion(root, entry_usuario, entry_contraseña):
    usuario = entry_usuario.get()
    contraseña = entry_contraseña.get()

    if not usuario or not contraseña:
        messagebox.showwarning("Campos vacíos", "Por favor ingresa usuario y contraseña.")
        print("Commit: Intento de inicio sin datos completos.")
        return

    rol = verificar_login(usuario, contraseña)
    if rol:
        messagebox.showinfo("Acceso concedido", f"Bienvenido al sistema ({rol})")
        root.withdraw()  # Oculta la ventana de login sin destruirla
        ventana_principal(rol, root)
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")


def mostrar_login():
    root = tk.Tk()
    root.title("Login - Espacio Creativo")
    root.geometry("800x600")
    root.config(bg=COLOR_FONDO_VENTANA)

    try:
        imagen_logo = Image.open("Espacio.naranja.png").resize((150, 160))
        root.logo = ImageTk.PhotoImage(imagen_logo)
        tk.Label(root, image=root.logo, bg=COLOR_FONDO_VENTANA).pack(pady=(20, 5))
    except Exception as e:
        print("No se pudo cargar el logo:", e)

    login_frame = tk.Frame(root, bg=COLOR_FONDO_FRAME, padx=40, pady=30)
    login_frame.pack(expand=True)

    tk.Label(login_frame, text="Inicio de sesión",
             font=("Arial", 18, "bold"),
             bg=COLOR_FONDO_FRAME,
             fg=COLOR_TEXTO_OSCURO).pack(pady=(0, 20))

    tk.Label(login_frame, text="Usuario:",
             font=("Arial", 11),
             bg=COLOR_FONDO_FRAME,
             fg=COLOR_TEXTO_OSCURO).pack(anchor="w")
    entry_usuario = tk.Entry(login_frame, width=35,
                             font=("Arial", 11),
                             relief="solid", bd=1)
    entry_usuario.pack(pady=(5, 15))

    tk.Label(login_frame, text="Contraseña:",
             font=("Arial", 11),
             bg=COLOR_FONDO_FRAME,
             fg=COLOR_TEXTO_OSCURO).pack(anchor="w")
    entry_contraseña = tk.Entry(login_frame, width=35, show="*",
                                font=("Arial", 11),
                                relief="solid", bd=1)
    entry_contraseña.pack(pady=(5, 20))

    btn_ingresar = tk.Button(login_frame, text="Ingresar",
                             command=lambda: iniciar_sesion(root, entry_usuario, entry_contraseña),
                             bg=COLOR_BOTON,
                             fg=COLOR_TEXTO_OSCURO,
                             font=("Arial", 12, "bold"),
                             relief="flat",
                             padx=30, pady=8,
                             cursor="hand2")
    btn_ingresar.pack(pady=15)

    tk.Label(login_frame, text="Usuario: admin | Contraseña: 1234",
             font=("Arial", 9),
             bg=COLOR_FONDO_FRAME,
             fg=COLOR_TEXTO_OSCURO).pack(pady=(10, 0))

    print("Commit: Interfaz de login inicializada.")
    root.mainloop()


if __name__ == "__main__":
    mostrar_login()
