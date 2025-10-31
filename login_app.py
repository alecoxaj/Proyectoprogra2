import tkinter as tk
from tkinter import messagebox
import sqlite3

from crud_clientes import ventana_clientes
from crud_servicios import ventana_servicios

DB_PATH = "espacio_creativo.db"

COLOR_FONDO_VENTANA = "#FFF9E6"
COLOR_FONDO_FRAME = "#FFF3C4"
COLOR_BOTON = "#E6B325"
COLOR_TEXTO_OSCURO = "#333333"
COLOR_TEXTO_BLANCO = "#FFFFFF"
COLOR_BOTON_SALIR = "#f8d7da"

def verificar_login(usuario, contraseña):
    try:
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
    except sqlite3.OperationalError as e:
        print(f"Error de base de datos: {e}")
        messagebox.showerror("Error de Base de Datos",
                             "No se pudo conectar o encontrar la tabla 'usuarios'. Asegúrate de que la base de datos exista.")
        return None

def ventana_principal(rol):
    ventana = tk.Toplevel()
    ventana.title("Menú Principal - Espacio Creativo")
    ventana.geometry("400x350")
    ventana.config(bg=COLOR_FONDO_VENTANA)

    tk.Label(ventana, text=f"Bienvenido, rol: {rol}",
             font=("Arial", 14, "bold"),
             bg=COLOR_FONDO_VENTANA,
             fg=COLOR_TEXTO_OSCURO).pack(pady=20)

    if rol == "admin":
        opciones = ["Gestión de Usuarios", "Clientes", "Servicios", "Agenda", "Ventas", "Reportes"]
    else:
        opciones = ["Clientes", "Agenda", "Ventas"]

    frame_menu = tk.Frame(ventana, bg=COLOR_FONDO_VENTANA)
    frame_menu.pack()

    estilo_boton_menu = {
        "width": 25,
        "bg": COLOR_BOTON,
        "fg": COLOR_TEXTO_OSCURO,
        "font": ("Arial", 10, "bold"),
        "relief": "flat",
        "borderwidth": 0,
        "pady": 5
    }

    for opcion in opciones:
        comando = None
        if opcion == "Clientes":
            comando = ventana_clientes
        elif opcion == "Servicios":
            comando = ventana_servicios

        if comando is None:
            comando = lambda op=opcion: messagebox.showinfo("En construcción", f"Módulo '{op}' no implementado.")

        tk.Button(frame_menu, text=opcion, command=comando, **estilo_boton_menu).pack(pady=4)

    tk.Button(ventana, text="Cerrar sesión",
              command=ventana.destroy,
              bg=COLOR_BOTON_SALIR,
              fg=COLOR_TEXTO_OSCURO,
              relief="flat",
              borderwidth=0,
              font=("Arial", 10, "bold"),
              pady=5,
              padx=10
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
        root.withdraw()
        ventana_principal(rol)
        root.deiconify()
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")

root = tk.Tk()
root.title("Login - Espacio Creativo")
root.geometry("800x600")
root.config(bg=COLOR_FONDO_VENTANA)

tk.Label(root, text="ESPACIO",
         font=("Arial", 22, "bold"),
         bg=COLOR_FONDO_VENTANA,
         fg=COLOR_TEXTO_OSCURO).pack(pady=(40, 0), side="top")
tk.Label(root, text="CREATIVO",
         font=("Arial", 22),
         bg=COLOR_FONDO_VENTANA,
         fg=COLOR_TEXTO_OSCURO).pack(side="top")

login_frame = tk.Frame(root, bg=COLOR_FONDO_FRAME, padx=40, pady=30)
login_frame.pack(expand=True)

tk.Label(login_frame, text="Inicio de sesión",
         font=("Arial", 18, "bold"),
         bg=COLOR_FONDO_FRAME,
         fg=COLOR_TEXTO_OSCURO
         ).pack(pady=(0, 20))

tk.Label(login_frame, text="Usuario:",
         font=("Arial", 11),
         bg=COLOR_FONDO_FRAME,
         fg=COLOR_TEXTO_OSCURO
         ).pack(anchor="w")
entry_usuario = tk.Entry(login_frame, width=35,
                         font=("Arial", 11),
                         relief="solid",
                         bd=1)
entry_usuario.pack(pady=(5, 15))

tk.Label(login_frame, text="Contraseña:",
         font=("Arial", 11),
         bg=COLOR_FONDO_FRAME,
         fg=COLOR_TEXTO_OSCURO
         ).pack(anchor="w")
entry_contraseña = tk.Entry(login_frame, width=35, show="*",
                            font=("Arial", 11),
                            relief="solid",
                            bd=1)
entry_contraseña.pack(pady=(5, 20))

btn_ingresar = tk.Button(login_frame, text="Ingresar",
                         command=iniciar_sesion,
                         bg=COLOR_BOTON,
                         fg=COLOR_TEXTO_OSCURO,
                         font=("Arial", 12, "bold"),
                         relief="flat",
                         borderwidth=0,
                         padx=30,
                         pady=8,
                         cursor="hand2"
                         )
btn_ingresar.pack(pady=15)

tk.Label(login_frame, text="Usuario: admin | Contraseña: 1234",
         font=("Arial", 9),
         bg=COLOR_FONDO_FRAME,
         fg=COLOR_TEXTO_OSCURO
         ).pack(pady=(10, 0))

print("Interfaz de login inicializada.")
root.mainloop()