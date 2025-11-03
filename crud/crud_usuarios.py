import tkinter as tk
from tkinter import ttk, messagebox
from core.database import DatabaseManager

COLOR_FONDO_VENTANA = "#FFF9E6"
COLOR_FONDO_FRAME = "#FFF3C4"
COLOR_BOTON = "#E6B325"
COLOR_TEXTO_OSCURO = "#333333"

class UsuariosView(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Gestión de Usuarios - Espacio Creativo")
        self.geometry("650x420")
        self.config(bg=COLOR_FONDO_VENTANA)
        self.db = DatabaseManager()
        self._crear_interfaz()
        self.cargar_datos()
        print("Ventana de Usuarios inicializada.")

    def _crear_interfaz(self):
        frame = tk.Frame(self, bg=COLOR_FONDO_FRAME, padx=15, pady=10)
        frame.pack(fill="both", expand=True, pady=10)

        campos = [
            ("Nombre:", "nombre"),
            ("Usuario:", "usuario"),
            ("Contraseña:", "contraseña"),
            ("Rol (admin/usuario):", "rol"),
        ]
        self.entries = {}
        for i, (label_text, key) in enumerate(campos):
            tk.Label(frame, text=label_text, bg=COLOR_FONDO_FRAME, fg=COLOR_TEXTO_OSCURO).grid(row=i, column=0, sticky="e", padx=5, pady=5)
            entry = tk.Entry(frame, width=35, show="*" if key == "contraseña" else "")
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries[key] = entry

        botones = [
            ("Agregar", self.agregar_usuario, COLOR_BOTON),
            ("Actualizar", self.actualizar_usuario, "#FFD966"),
            ("Eliminar", self.eliminar_usuario, "#F4B183"),
            ("Cargar", self.cargar_datos, "#A9D18E"),
        ]

        for i, (texto, comando, color) in enumerate(botones):
            tk.Button(frame, text=texto, bg=color, fg=COLOR_TEXTO_OSCURO, relief="flat",
                      command=comando, width=12).grid(row=5, column=i, pady=10, padx=4)

        columnas = ("id", "nombre", "usuario", "rol")
        self.tabla = ttk.Treeview(frame, columns=columnas, show="headings", height=10)
        for col in columnas:
            self.tabla.heading(col, text=col.capitalize())
            self.tabla.column(col, width=150)
        self.tabla.grid(row=6, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
        self.tabla.bind("<<TreeviewSelect>>", self._seleccionar_fila)

    def cargar_datos(self):
        self.tabla.delete(*self.tabla.get_children())
        try:
            cur = self.db.execute("SELECT id, nombre, usuario, rol FROM usuarios")
            for fila in cur.fetchall():
                self.tabla.insert("", tk.END, values=fila)
            print("Usuarios cargados correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los usuarios.\n{e}")

    def agregar_usuario(self):
        nombre = self.entries["nombre"].get().strip()
        usuario = self.entries["usuario"].get().strip()
        contrasena = self.entries["contraseña"].get().strip()
        rol = self.entries["rol"].get().strip()

        if not nombre or not usuario or not contrasena:
            messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios.")
            return

        sql = "INSERT INTO usuarios (nombre, usuario, contraseña, rol) VALUES (?, ?, ?, ?)"
        self.db.execute(sql, (nombre, usuario, contrasena, rol), commit=True)
        self.cargar_datos()
        self._limpiar_campos()
        print("Usuario agregado exitosamente.")

    def actualizar_usuario(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona un usuario para actualizar.")
            return

        usuario_id = self.tabla.item(seleccion[0])["values"][0]
        sql = "UPDATE usuarios SET nombre=?, usuario=?, contraseña=?, rol=? WHERE id=?"
        params = (
            self.entries["nombre"].get(),
            self.entries["usuario"].get(),
            self.entries["contraseña"].get(),
            self.entries["rol"].get(),
            usuario_id,
        )
        self.db.execute(sql, params, commit=True)
        self.cargar_datos()
        print("Usuario actualizado correctamente.")

    def eliminar_usuario(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona un usuario para eliminar.")
            return

        usuario_id = self.tabla.item(seleccion[0])["values"][0]
        if not messagebox.askyesno("Confirmar", "¿Deseas eliminar este usuario?"):
            return

        sql = "DELETE FROM usuarios WHERE id=?"
        self.db.execute(sql, (usuario_id,), commit=True)
        self.cargar_datos()
        print("Usuario eliminado correctamente.")

    def _seleccionar_fila(self, event):
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        valores = self.tabla.item(seleccion[0])["values"]
        keys = list(self.entries.keys())
        for i, key in enumerate(keys):
            self.entries[key].delete(0, tk.END)
            self.entries[key].insert(0, valores[i + 1])
        print("Usuario seleccionado para edición.")

    def _limpiar_campos(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)