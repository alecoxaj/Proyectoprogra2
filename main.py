import tkinter as tk
from ui.login_view import LoginView

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Espacio Creativo")
        self.root.geometry("800x600")
        self.root.config(bg="#FFF9E6")
        self.mostrar_login()

        print("Aplicación inicializada correctamente (App principal).")
        self.root.mainloop()

    def mostrar_login(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.login_view = LoginView(self)

    def abrir_menu(self, rol):
        from ui.main_menu_view import MainMenuView

        for widget in self.root.winfo_children():
            widget.destroy()

        MainMenuView(self, rol)
        print(f"Menú principal abierto con rol '{rol}'.")

if __name__ == "__main__":
    App()