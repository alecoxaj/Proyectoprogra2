import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkFont
from PIL import Image, ImageTk
import sqlite3

class LoginView:
    DB_PATH = "espacio_creativo.db"

    COLOR_FONDO_VENTANA = "#FFF9E6"
    COLOR_FONDO_FRAME = "#FFF3C4"
    COLOR_BOTON = "#E6B325"
    COLOR_TEXTO_OSCURO = "#333333"

    def __init__(self, app):
        self.app = app
        self.root = app.root
        self.FAMILIA_FUENTE = "Montserrat"
        self.font_titulo = tkFont.Font(
            family=self.FAMILIA_FUENTE,
            size=18,
            weight="bold"
        )
        self.font_normal = tkFont.Font(
            family=self.FAMILIA_FUENTE,
            size=11
        )
        self.font_normal_negrita = tkFont.Font(
            family=self.FAMILIA_FUENTE,
            size=11,
            weight="bold"
        )
        self.font_boton = tkFont.Font(
            family=self.FAMILIA_FUENTE,
            size=12,
            weight="bold"
        )

        self.construir_ui()
        print("Interfaz de login inicializada correctamente.")

    def construir_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        try:
            imagen_logo = Image.open("espacio.naranja.png").resize((150, 160))
            self.root.logo = ImageTk.PhotoImage(imagen_logo)
            tk.Label(self.root, image=self.root.logo, bg=self.COLOR_FONDO_VENTANA).pack(pady=(20, 5))
        except Exception as e:
            print("No se pudo cargar el logo:", e)

        login_frame = tk.Frame(self.root, bg=self.COLOR_FONDO_FRAME, padx=40, pady=30)
        login_frame.pack(expand=True)

        tk.Label(login_frame, text="Inicio de sesión",
                 font=self.font_titulo,
                 bg=self.COLOR_FONDO_FRAME,
                 fg=self.COLOR_TEXTO_OSCURO).pack(pady=(0, 20))

        tk.Label(login_frame, text="Usuario:", font=self.font_normal_negrita,
                 bg=self.COLOR_FONDO_FRAME, fg=self.COLOR_TEXTO_OSCURO).pack(anchor="w")
        self.entry_usuario = tk.Entry(login_frame, width=35, font=self.font_normal,
                                      relief="solid", bd=1)
        self.entry_usuario.pack(pady=(5, 15))

        tk.Label(login_frame, text="Contraseña:", font=self.font_normal_negrita,
                 bg=self.COLOR_FONDO_FRAME, fg=self.COLOR_TEXTO_OSCURO).pack(anchor="w")
        self.entry_contraseña = tk.Entry(login_frame, width=35, show="*",
                                         font=self.font_normal, relief="solid", bd=1)
        self.entry_contraseña.pack(pady=(5, 20))

        btn_ingresar = tk.Button(login_frame, text="Ingresar",
                                 command=self.iniciar_sesion,
                                 bg=self.COLOR_BOTON, fg=self.COLOR_TEXTO_OSCURO,
                                 font=self.font_boton,
                                 relief="flat", padx=30, pady=8,
                                 cursor="hand2")
        btn_ingresar.pack(pady=15)

    def verificar_login(self, usuario, contraseña):
        try:
            conexion = sqlite3.connect(self.DB_PATH)
            cursor = conexion.cursor()
            cursor.execute("SELECT rol FROM usuarios WHERE usuario=? AND contraseña=?", (usuario, contraseña))
            resultado = cursor.fetchone()
            conexion.close()

            if resultado:
                print(f"Usuario '{usuario}' inició sesión como {resultado[0]}.")
                return resultado[0]
            else:
                print(f"Intento fallido de inicio con usuario '{usuario}'.")
                return None
        except Exception as e:
            messagebox.showerror("Error de conexión", f"No se pudo acceder a la base de datos:\n{e}")
            return None

    def iniciar_sesion(self):
        usuario = self.entry_usuario.get().strip()
        contraseña = self.entry_contraseña.get().strip()

        if not usuario or not contraseña:
            messagebox.showwarning("Campos vacíos", "Por favor ingresa usuario y contraseña.")
            print("Intento de inicio sin datos completos.")
            return

        rol = self.verificar_login(usuario, contraseña)
        if rol:
            messagebox.showinfo("Acceso concedido", f"Bienvenido al sistema ({rol})")
            self.app.abrir_menu(rol)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")