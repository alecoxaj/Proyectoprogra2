import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from core.database import DatabaseManager

COLOR_FONDO_VENTANA = "#FFF9E6"
COLOR_FONDO_FRAME = "#FFF3C4"
COLOR_BOTON = "#E6B325"
COLOR_TEXTO_OSCURO = "#333333"

class VentasView(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Gestión de Ventas - Espacio Creativo")
        self.geometry("700x420")
        self.config(bg=COLOR_FONDO_VENTANA)
        self.db = DatabaseManager()
        self._crear_interfaz()
        self.cargar_datos()
        print("Ventana de Ventas inicializada.")

    def _crear_interfaz(self):
        frame = tk.Frame(self, bg=COLOR_FONDO_FRAME, padx=15, pady=10)
        frame.pack(fill="both", expand=True, pady=10)

        campos = [
            ("Cliente ID:", "cliente_id"),
            ("Servicio ID:", "servicio_id"),
            ("Total:", "total"),
        ]
        self.entries = {}
        for i, (texto, key) in enumerate(campos):
            tk.Label(frame, text=texto, bg=COLOR_FONDO_FRAME, fg=COLOR_TEXTO_OSCURO).grid(row=i, column=0, sticky="e", padx=5, pady=5)
            entry = tk.Entry(frame, width=35)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries[key] = entry

        botones = [
            ("Agregar", self.agregar_venta, COLOR_BOTON),
            ("Eliminar", self.eliminar_venta, "#F4B183"),
            ("Cargar", self.cargar_datos, "#A9D18E")
        ]
        for i, (texto, comando, color) in enumerate(botones):
            tk.Button(frame, text=texto, bg=color, fg=COLOR_TEXTO_OSCURO, relief="flat",
                      command=comando, width=12).grid(row=4, column=i, pady=10, padx=4)

        columnas = ("id", "cliente_id", "servicio_id", "fecha", "total")
        self.tabla = ttk.Treeview(frame, columns=columnas, show="headings", height=10)
        for col in columnas:
            self.tabla.heading(col, text=col.capitalize())
            self.tabla.column(col, width=120)
        self.tabla.grid(row=5, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        self.tabla.bind("<<TreeviewSelect>>", self._seleccionar_fila)

    def cargar_datos(self):
        try:
            self.tabla.delete(*self.tabla.get_children())
            cur = self.db.execute("SELECT * FROM ventas ORDER BY fecha DESC")
            for fila in cur.fetchall():
                self.tabla.insert("", tk.END, values=fila)
            print("Datos de ventas cargados.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los datos.\n{e}")

    def agregar_venta(self):
        cliente = self.entries["cliente_id"].get().strip()
        servicio = self.entries["servicio_id"].get().strip()
        total = self.entries["total"].get().strip()

        if not cliente or not servicio or not total:
            messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios.")
            return

        try:
            total_valor = float(total)
        except ValueError:
            messagebox.showerror("Error", "El campo 'Total' debe ser un número válido.")
            return

        sql = "INSERT INTO ventas (cliente_id, servicio_id, fecha, total) VALUES (?, ?, ?, ?)"
        params = (cliente, servicio, date.today().isoformat(), total_valor)
        self.db.execute(sql, params, commit=True)
        self.cargar_datos()
        self._limpiar_campos()
        print("Venta registrada correctamente.")

    def eliminar_venta(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona una venta para eliminar.")
            return

        venta_id = self.tabla.item(seleccion[0])["values"][0]
        if not messagebox.askyesno("Confirmar", "¿Deseas eliminar esta venta?"):
            return

        sql = "DELETE FROM ventas WHERE id=?"
        self.db.execute(sql, (venta_id,), commit=True)
        self.cargar_datos()
        print("Venta eliminada correctamente.")

    def _seleccionar_fila(self, event):
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        valores = self.tabla.item(seleccion[0])["values"]
        keys = list(self.entries.keys())
        for i, key in enumerate(keys):
            self.entries[key].delete(0, tk.END)
            self.entries[key].insert(0, valores[i + 1])
        print("Venta seleccionada para revisión.")

    def _limpiar_campos(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)