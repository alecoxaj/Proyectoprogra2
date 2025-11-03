import tkinter as tk
from tkinter import ttk, messagebox
from core.database import DatabaseManager

COLOR_FONDO_VENTANA = "#FFF9E6"
COLOR_FONDO_FRAME = "#FFF3C4"
COLOR_BOTON = "#E6B325"
COLOR_TEXTO_OSCURO = "#333333"

class ClientesView(tk.Toplevel):
    """Gestión de Clientes - Aplicación Espacio Creativo (versión POO + SOLID)."""

    def __init__(self, master=None):
        super().__init__(master)
        self.title("Gestión de Clientes - Espacio Creativo")
        self.geometry("700x420")
        self.config(bg=COLOR_FONDO_VENTANA)
        self.db = DatabaseManager()
        self._crear_interfaz()
        self.cargar_datos()
        print("Ventana de clientes inicializada con POO y DatabaseManager.")

    def _crear_interfaz(self):
        frame = tk.Frame(self, bg=COLOR_FONDO_FRAME, padx=15, pady=10)
        frame.pack(fill="both", expand=True, pady=10)

        labels = ["Nombre:", "Correo:", "Teléfono:", "Tipo de servicio:"]
        self.entries = {}
        for i, label_text in enumerate(labels):
            tk.Label(frame, text=label_text, bg=COLOR_FONDO_FRAME, fg=COLOR_TEXTO_OSCURO).grid(row=i, column=0, sticky="e", padx=5, pady=5)
            entry = tk.Entry(frame, width=40)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries[label_text] = entry

        botones = [
            ("Agregar", COLOR_BOTON, self.agregar_cliente),
            ("Actualizar", "#FFD966", self.actualizar_cliente),
            ("Eliminar", "#F4B183", self.eliminar_cliente),
            ("Cargar", "#A9D18E", self.cargar_datos)
        ]
        for i, (texto, color, comando) in enumerate(botones):
            tk.Button(frame, text=texto, bg=color, fg=COLOR_TEXTO_OSCURO,
                      relief="flat", command=comando, width=12).grid(row=4, column=i, pady=10, padx=5)

        columnas = ("id", "nombre", "correo", "telefono", "tipo_servicio")
        self.tabla = ttk.Treeview(frame, columns=columnas, show="headings", height=10)
        for col in columnas:
            self.tabla.heading(col, text=col.capitalize())
            self.tabla.column(col, width=120 if col != "nombre" else 180)
        self.tabla.grid(row=5, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        self.tabla.bind("<<TreeviewSelect>>", self._on_seleccionar)

    def cargar_datos(self):
        """Carga los datos de clientes desde la base de datos."""
        self.tabla.delete(*self.tabla.get_children())
        cur = self.db.execute("SELECT * FROM clientes")
        for fila in cur.fetchall():
            self.tabla.insert("", tk.END, values=fila)
        print("Datos de clientes cargados correctamente.")

    def agregar_cliente(self):
        """Agrega un nuevo cliente."""
        nombre = self.entries["Nombre:"].get().strip()
        correo = self.entries["Correo:"].get().strip()
        telefono = self.entries["Teléfono:"].get().strip()
        tipo = self.entries["Tipo de servicio:"].get().strip()

        if not nombre:
            messagebox.showwarning("Campo obligatorio", "El campo 'Nombre' es obligatorio.")
            return

        sql = "INSERT INTO clientes (nombre, correo, telefono, tipo_servicio) VALUES (?, ?, ?, ?)"
        self.db.execute(sql, (nombre, correo, telefono, tipo), commit=True)
        self.cargar_datos()
        self._limpiar_campos()
        messagebox.showinfo("Éxito", "Cliente agregado correctamente.")
        print("Cliente agregado a la base de datos.")

    def actualizar_cliente(self):
        """Actualiza la información del cliente seleccionado."""
        sel = self.tabla.selection()
        if not sel:
            messagebox.showwarning("Advertencia", "Selecciona un cliente para actualizar.")
            return
        cliente_id = self.tabla.item(sel[0])["values"][0]

        sql = """UPDATE clientes 
                 SET nombre=?, correo=?, telefono=?, tipo_servicio=? 
                 WHERE id=?"""
        self.db.execute(sql, (
            self.entries["Nombre:"].get().strip(),
            self.entries["Correo:"].get().strip(),
            self.entries["Teléfono:"].get().strip(),
            self.entries["Tipo de servicio:"].get().strip(),
            cliente_id
        ), commit=True)
        self.cargar_datos()
        messagebox.showinfo("Éxito", "Cliente actualizado correctamente.")
        print(f"Cliente con ID {cliente_id} actualizado.")

    def eliminar_cliente(self):
        """Elimina el cliente seleccionado."""
        sel = self.tabla.selection()
        if not sel:
            messagebox.showwarning("Advertencia", "Selecciona un cliente para eliminar.")
            return
        cliente_id = self.tabla.item(sel[0])["values"][0]
        if not messagebox.askyesno("Confirmar", "¿Deseas eliminar este cliente?"):
            return

        self.db.execute("DELETE FROM clientes WHERE id=?", (cliente_id,), commit=True)
        self.cargar_datos()
        messagebox.showinfo("Éxito", "Cliente eliminado correctamente.")
        print(f"Cliente con ID {cliente_id} eliminado.")

    def _on_seleccionar(self, event):
        """Rellena los campos al seleccionar un cliente."""
        sel = self.tabla.selection()
        if not sel:
            return
        valores = self.tabla.item(sel[0])["values"]
        for (key, entry), value in zip(self.entries.items(), valores[1:]):
            entry.delete(0, tk.END)
            entry.insert(0, value)
        print(f"Cliente seleccionado (ID {valores[0]}).")

    def _limpiar_campos(self):
        """Limpia los campos de entrada."""
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        print("Campos del formulario limpiados.")