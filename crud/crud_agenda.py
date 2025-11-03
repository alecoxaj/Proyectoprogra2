import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from core.database import DatabaseManager

class AgendaView(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Agenda - Espacio Creativo")
        self.geometry("700x400")
        self.config(bg="#f7f7f7")

        self.db = DatabaseManager()
        self.ANCHO_CAMPOS = 30

        self._construir_ui()
        self.cargar_datos()
        print("Ventana de agenda inicializada.")

    def _construir_ui(self):
        tk.Label(self, text="Cliente ID:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.cliente_id = tk.Entry(self, width=self.ANCHO_CAMPOS)
        self.cliente_id.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        tk.Label(self, text="Servicio ID:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.servicio_id = tk.Entry(self, width=self.ANCHO_CAMPOS)
        self.servicio_id.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        tk.Label(self, text="Fecha:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.fecha = DateEntry(
            self,
            width=self.ANCHO_CAMPOS - 2,
            background="#E6B325",
            foreground="black",
            borderwidth=1,
            relief="solid",
            date_pattern="yyyy-mm-dd",
            font=("Arial", 10)
        )
        self.fecha.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        tk.Label(self, text="Estado:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.estado = tk.Entry(self, width=self.ANCHO_CAMPOS)
        self.estado.insert(0, "Pendiente")
        self.estado.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # Tabla de datos
        self.tabla = ttk.Treeview(
            self,
            columns=("id", "cliente_id", "servicio_id", "fecha", "estado"),
            show="headings",
            height=10
        )
        for col in self.tabla["columns"]:
            self.tabla.heading(col, text=col.capitalize())
            self.tabla.column(col, width=130)
        self.tabla.grid(row=6, column=0, columnspan=4, padx=10, pady=10)

        tk.Button(self, text="Agregar", command=self.agregar_evento, bg="#a8e6cf").grid(row=4, column=0, padx=5, pady=5)
        tk.Button(self, text="Actualizar", command=self.actualizar_evento, bg="#ffd3b6").grid(row=4, column=1, padx=5, pady=5)
        tk.Button(self, text="Eliminar", command=self.eliminar_evento, bg="#ffaaa5").grid(row=4, column=2, padx=5, pady=5)
        tk.Button(self, text="Cargar", command=self.cargar_datos, bg="#dcedc1").grid(row=4, column=3, padx=5, pady=5)

        self.tabla.bind("<<TreeviewSelect>>", self.on_seleccionar)

    def cargar_datos(self):
        self.tabla.delete(*self.tabla.get_children())
        cur = self.db.execute("SELECT * FROM agenda")
        for fila in cur.fetchall():
            self.tabla.insert("", tk.END, values=fila)
        print("Datos de agenda cargados.")

    def agregar_evento(self):
        cliente = self.cliente_id.get().strip()
        servicio = self.servicio_id.get().strip()
        fecha = self.fecha.get()
        estado = self.estado.get().strip()

        if not cliente or not servicio:
            messagebox.showwarning("Validación", "Cliente y Servicio ID son obligatorios.")
            return

        sql = "INSERT INTO agenda (cliente_id, servicio_id, fecha, estado) VALUES (?, ?, ?, ?)"
        self.db.execute(sql, (cliente, servicio, fecha, estado), commit=True)
        self.cargar_datos()
        print("Nuevo evento agregado.")
        messagebox.showinfo("Éxito", "Evento agregado correctamente.")
        self.limpiar_campos()

    def actualizar_evento(self):
        sel = self.tabla.selection()
        if not sel:
            messagebox.showwarning("Advertencia", "Selecciona un evento para actualizar.")
            return
        evento_id = self.tabla.item(sel[0])["values"][0]

        sql = """UPDATE agenda 
                 SET cliente_id=?, servicio_id=?, fecha=?, estado=? 
                 WHERE id=?"""
        self.db.execute(sql, (
            self.cliente_id.get().strip(),
            self.servicio_id.get().strip(),
            self.fecha.get(),
            self.estado.get().strip(),
            evento_id
        ), commit=True)

        self.cargar_datos()
        print("Evento actualizado.")
        messagebox.showinfo("Éxito", "Evento actualizado correctamente.")
        self.limpiar_campos()

    def eliminar_evento(self):
        sel = self.tabla.selection()
        if not sel:
            messagebox.showwarning("Advertencia", "Selecciona un evento para eliminar.")
            return
        evento_id = self.tabla.item(sel[0])["values"][0]

        if not messagebox.askyesno("Confirmar", "¿Eliminar evento seleccionado?"):
            return

        self.db.execute("DELETE FROM agenda WHERE id=?", (evento_id,), commit=True)
        self.cargar_datos()
        print("Evento eliminado.")
        messagebox.showinfo("Éxito", "Evento eliminado correctamente.")
        self.limpiar_campos()

    def on_seleccionar(self, event):
        sel = self.tabla.selection()
        if not sel:
            return
        valores = self.tabla.item(sel[0])["values"]
        self.cliente_id.delete(0, tk.END)
        self.servicio_id.delete(0, tk.END)
        self.estado.delete(0, tk.END)
        self.cliente_id.insert(0, valores[1])
        self.servicio_id.insert(0, valores[2])
        self.fecha.set_date(valores[3])
        self.estado.insert(0, valores[4])
        print("Evento seleccionado para edición.")

    def limpiar_campos(self):
        self.cliente_id.delete(0, tk.END)
        self.servicio_id.delete(0, tk.END)
        self.estado.delete(0, tk.END)
        self.estado.insert(0, "Pendiente")