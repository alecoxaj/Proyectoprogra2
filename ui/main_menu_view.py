import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkFont
from PIL import Image, ImageTk

from crud.crud_clientes import ventana_clientes
from crud.crud_servicios import ventana_servicios
from crud.crud_usuarios import ventana_usuarios
from crud.crud_agenda import ventana_agenda
from crud.crud_ventas import ventana_ventas
from crud.crud_reportes import ventana_reportes

COLOR_FONDO_VENTANA = "#FFF9E6"
COLOR_FONDO_FRAME = "#FFF3C4"
COLOR_BOTON = "#E6B325"
COLOR_TEXTO_OSCURO = "#333333"
COLOR_BOTON_SALIR = "#f8d7da"

class MainMenuView:
    def __init__(self, app, rol):
        self.app = app
        self.root = app.root
        self.rol = rol
        self.FAMILIA_FUENTE = "Montserrat"
        self.font_titulo_menu = tkFont.Font(
            family=self.FAMILIA_FUENTE, size=20, weight="bold"
        )
        self.font_subtitulo_menu = tkFont.Font(
            family=self.FAMILIA_FUENTE, size=14
        )
        self.font_boton_menu = tkFont.Font(
            family=self.FAMILIA_FUENTE, size=11, weight="bold"
        )

        for widget in self.root.winfo_children():
            widget.destroy()
        try:
            self.root.state('zoomed')
        except tk.TclError:
            self.root.geometry("1200x800")

        self.root.config(bg=COLOR_FONDO_VENTANA)
        self.root.logo_menu = None
        self.root.logo_salir = None
        self.construir_menu_ui()
        print(f"MainMenuView inicializado para rol '{rol}'.")

    def construir_menu_ui(self):
        frame_superior = tk.Frame(self.root, bg=COLOR_FONDO_VENTANA)
        frame_superior.pack(pady=(20, 10), fill='x')

        try:
            imagen_logo = Image.open("espacio.naranja.png").resize((120, 120))
            self.root.logo_menu = ImageTk.PhotoImage(imagen_logo)
            tk.Label(frame_superior, image=self.root.logo_menu, bg=COLOR_FONDO_VENTANA).pack(pady=10)
        except Exception as e:
            print(f"No se pudo cargar el logo en el menú: {e}")
            tk.Label(frame_superior, text="[LOGO]", bg=COLOR_FONDO_VENTANA).pack(pady=10)

        tk.Label(frame_superior, text="MENÚ PRINCIPAL",
                 font=self.font_titulo_menu,
                 bg=COLOR_FONDO_VENTANA,
                 fg=COLOR_TEXTO_OSCURO).pack(pady=(10, 5))

        tk.Label(frame_superior, text=f"Bienvenido ({self.rol})",
                 font=self.font_subtitulo_menu,
                 bg=COLOR_FONDO_VENTANA,
                 fg=COLOR_TEXTO_OSCURO).pack(pady=(0, 20))

        contenedor_central = tk.Frame(self.root, bg=COLOR_FONDO_VENTANA)
        contenedor_central.pack(expand=True, fill="both")

        frame_menu = tk.Frame(contenedor_central, bg=COLOR_FONDO_FRAME, padx=60, pady=40)
        frame_menu.place(relx=0.5, rely=0.50, anchor="center")

        if self.rol == "admin":
            opciones = [
                ("Gestión de Usuarios", lambda: ventana_usuarios()),
                ("Clientes", lambda: ventana_clientes()),
                ("Servicios", lambda: ventana_servicios()),
                ("Agenda", lambda: ventana_agenda()),
                ("Ventas", lambda: ventana_ventas()),
                ("Reportes", lambda: ventana_reportes())
            ]
        else:
            opciones = [
                ("Clientes", lambda: ventana_clientes()),
                ("Agenda", lambda: ventana_agenda()),
                ("Ventas", lambda: ventana_ventas())
            ]

        estilo_boton = {
            "width": 25,
            "bg": COLOR_BOTON,
            "fg": COLOR_TEXTO_OSCURO,
            "font": self.font_boton_menu,
            "relief": "flat",
            "borderwidth": 0,
            "pady": 8,
            "cursor": "hand2"
        }

        for texto, comando in opciones:
            tk.Button(frame_menu, text=texto, command=comando, **estilo_boton).pack(pady=8)

        frame_inferior = tk.Frame(self.root, bg=COLOR_FONDO_VENTANA)
        frame_inferior.pack(side="bottom", fill="x", pady=20)

        try:
            imagen_salir = Image.open("logo.salir.png").resize((45, 45))
            self.root.logo_salir = ImageTk.PhotoImage(imagen_salir)
            boton_salir = tk.Button(
                frame_inferior,
                image=self.root.logo_salir,
                bg=COLOR_FONDO_VENTANA,
                borderwidth=0,
                cursor="hand2",
                command=self.volver_login
            )
            boton_salir.pack(side="right", anchor="se", padx=30)
        except Exception as e:
            print(f"No se pudo cargar la imagen del botón salir: {e}")
            tk.Button(
                frame_inferior,
                text="Salir",
                bg=COLOR_BOTON_SALIR,
                fg=COLOR_TEXTO_OSCURO,
                font=self.font_boton_menu,
                relief="flat",
                borderwidth=0,
                padx=20,
                pady=8,
                cursor="hand2",
                command=self.volver_login
            ).pack(side="right", anchor="se", padx=30)

    def volver_login(self):
        try:
            from ui.login_view import LoginView
        except ImportError:
            messagebox.showerror("Error Crítico", "No se pudo encontrar 'ui.login_view'.")
            return

        self.root.state('normal')
        for widget in self.root.winfo_children():
            widget.destroy()
        LoginView(self.app)
        print("Sesión cerrada. Retorno al login.")