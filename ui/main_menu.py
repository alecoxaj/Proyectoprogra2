import tkinter as tk
from tkinter import messagebox
from crud.crud_clientes import ClientesView
from crud.crud_servicios import ServiciosView

COLOR_FONDO_VENTANA = "#FFF9E6"
COLOR_FONDO_FRAME = "#FFF3C4"
COLOR_BOTON = "#E6B325"
COLOR_TEXTO_OSCURO = "#333333"
COLOR_BOTON_SALIR = "#f8d7da"

class MainMenuView:
    def __init__(self, root, rol):
        self.root = root
        self.rol = rol

        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.config(bg=COLOR_FONDO_VENTANA)
        self.construir_menu_ui()
        print(f"Commit: MainMenuView cargado para rol '{rol}'.")

    def construir_menu_ui(self):
        tk.Label(self.root, text="MENÚ PRINCIPAL",
                 font=("Arial", 20, "bold"),
                 bg=COLOR_FONDO_VENTANA,
                 fg=COLOR_TEXTO_OSCURO).pack(pady=(30, 10))

        tk.Label(self.root, text=f"Bienvenido ({self.rol})",
                 font=("Arial", 14),
                 bg=COLOR_FONDO_VENTANA,
                 fg=COLOR_TEXTO_OSCURO).pack(pady=(0, 30))

        frame_menu = tk.Frame(self.root, bg=COLOR_FONDO_FRAME, padx=20, pady=20)

        if self.rol == "admin":
            opciones = ["Gestión de Usuarios", "Clientes", "Servicios", "Agenda", "Ventas", "Reportes"]
        else:
            opciones = ["Clientes", "Agenda", "Ventas"]

        estilo_boton = {
            "width": 25,
            "bg": COLOR_BOTON,
            "fg": COLOR_TEXTO_OSCURO,
            "font": ("Arial", 11, "bold"),
            "relief": "flat",
            "borderwidth": 0,
            "pady": 6,
            "cursor": "hand2"
        }

        for opcion in opciones:
            comando = None

            if opcion == "Clientes":
                comando = lambda: ClientesView(self.root)
            elif opcion == "Servicios":
                comando = lambda: ServiciosView(self.root)
            elif opcion == "Gestión de Usuarios":
                comando = lambda: messagebox.showinfo("En construcción", "Gestión de usuarios aún no disponible.")
            elif opcion == "Agenda":
                comando = lambda: messagebox.showinfo("En construcción", "Módulo de Agenda aún no disponible.")
            elif opcion == "Ventas":
                comando = lambda: messagebox.showinfo("En construcción", "Módulo de Ventas aún no disponible.")
            elif opcion == "Reportes":
                comando = lambda: messagebox.showinfo("En construcción", "Módulo de Reportes aún no disponible.")

            tk.Button(frame_menu, text=opcion, command=comando, **estilo_boton).pack(pady=5)

        tk.Button(self.root, text="Cerrar sesión",
                  bg=COLOR_BOTON_SALIR,
                  fg=COLOR_TEXTO_OSCURO,
                  font=("Arial", 11, "bold"),
                  relief="flat",
                  borderwidth=0,
                  padx=10,
                  pady=6,
                  cursor="hand2",
                  command=self.volver_login
                  ).pack(pady=30)

    def volver_login(self):
        from ui.login_view import LoginView
        for widget in self.root.winfo_children():
            widget.destroy()
        LoginView(self)
        print("Commit: Sesión cerrada, regreso al login.")