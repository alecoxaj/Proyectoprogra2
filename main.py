from ui.login_view import LoginView
import tkinter as tk

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Espacio Creativo")
        self.root.geometry("800x600")
        self.root.config(bg="#FFF9E6")

        self.login_view = LoginView(self)
        print("Aplicación inicializada correctamente (App principal).")

        self.root.mainloop()

    def abrir_menu(self, rol):
        """Llamado desde LoginView tras login exitoso"""
        from ui.main_menu import MainMenuView
        self.login_view.frame.destroy()
        MainMenuView(self.root, rol)

if __name__ == "__main__":
    LoginView()