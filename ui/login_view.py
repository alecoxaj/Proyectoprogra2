import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3

from ui.main_menu_view import MainMenuView

class LoginView:
    DB_PATH = "espacio_creativo.db"

    COLOR_FONDO_VENTANA = "#FFF9E6"
    COLOR_FONDO_FRAME = "#FFF3C4"
    COLOR_BOTON = "#E6B325"
    COLOR_TEXTO_OSCURO = "#333333"

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Login - Espacio Creativo")
        self.root.geometry("800x600")
        self.root.config(bg=self.COLOR_FONDO_VENTANA)
        self._construir_ui()
        print("Interfaz de login inicializada correctamente.")
        self.root.mainloop()

    def _construir_ui(self):
        try:
            imagen_logo = Image.open("Espacio.naranja.png").resize((150, 160))
            self.root.logo = ImageTk.PhotoImage(imagen_logo)
            tk.Label(self.root, image=self.root.logo, bg=self.COLOR_FONDO_VENTANA).pack(pady=(20, 5))
        except Exception as e:
            print("No se pudo cargar el logo:", e)

        login_frame = tk.Frame(self.root, bg=self.COLOR_FONDO_FRAME, padx=40, pady=30)
        login_frame.pack(expand=True)

        tk.Label(login_frame, text="Inicio de sesión",
                 font=("Arial", 18, "bold"),
                 bg=self.COLOR_FONDO_FRAME,
                 fg=self.COLOR_TEXTO_OSCURO).pack(pady=(0, 20))

        tk.Label(login_frame, text="Usuario:", font=("Arial", 11),
                 bg=self.COLOR_FONDO_FRAME, fg=self.COLOR_TEXTO_OSCURO).pack(anchor="w")
        self.entry_usuario = tk.Entry(login_frame, width=35, font=("Arial", 11),
                                      relief="solid", bd=1)
        self.entry_usuario.pack(pady=(5, 15))

        tk.Label(login_frame, text="Contraseña:", font=("Arial", 11),
                 bg=self.COLOR_FONDO_FRAME, fg=self.COLOR_TEXTO_OSCURO).pack(anchor="w")
        self.entry_contraseña = tk.Entry(login_frame, width=35, show="*",
                                         font=("Arial", 11), relief="solid", bd=1)
        self.entry_contraseña.pack(pady=(5, 20))

        btn_ingresar = tk.Button(login_frame, text="Ingresar",
                                 command=self.iniciar_sesion,
                                 bg=self.COLOR_BOTON, fg=self.COLOR_TEXTO_OSCURO,
                                 font=("Arial", 12, "bold"),
                                 relief="flat", padx=30, pady=8,
                                 cursor="hand2")
        btn_ingresar.pack(pady=15)

        tk.Label(login_frame, text="Usuario: admin | Contraseña: 1234",
                 font=("Arial", 9), bg=self.COLOR_FONDO_FRAME,
                 fg=self.COLOR_TEXTO_OSCURO).pack(pady=(10, 0))

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
                print(f"Intento fallido de inicio de sesión con usuario '{usuario}'.")
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
            self.root.withdraw()
            self.abrir_menu_principal(rol)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def abrir_menu_principal(self, rol):
        ventana_menu = tk.Toplevel(self.root)
        MainMenuView(ventana_menu, rol)
        print(f"Menú principal abierto para el rol '{rol}'.")