import tkinter as tk
from tkinter import ttk, messagebox
from core.database import DatabaseManager

COLOR_FONDO_VENTANA = "#FFF9E6"
COLOR_FONDO_FRAME = "#FFF3C4"
COLOR_BOTON = "#E6B325"
COLOR_TEXTO_OSCURO = "#333333"

class ReportesView(tk.Toplevel):
    """Módulo de Reportes - Espacio Creativo (POO + SOLID)."""

    def __init__(self, master=None):
        super().__init__(master)
        self.title("Reportes - Espacio Creativo")
        self.geometry("700x420")
        self.config(bg=COLOR_FONDO_VENTANA)

        self.db = DatabaseManager()

        self._crear_interfaz()
        print("Ventana de Reportes inicializada (POO + DatabaseManager).")

    def _crear_interfaz(self):
        frame = tk.Frame(self, bg=COLOR_FONDO_FRAME, padx=15, pady=15)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Label(frame, text="Reportes de Ventas y Servicios",
                 font=("Arial", 16, "bold"),
                 bg=COLOR_FONDO_FRAME,
                 fg=COLOR_TEXTO_OSCURO).pack(pady=(0, 10))

        columnas = ("servicio", "ventas", "ingresos")
        self.tabla = ttk.Treeview(frame, columns=columnas, show="headings", height=12)
        for col in columnas:
            self.tabla.heading(col, text=col.capitalize())
            self.tabla.column(col, width=180 if col == "servicio" else 120)
        self.tabla.pack(fill="both", expand=True, pady=10)

        tk.Button(frame, text="Generar reporte",
                  command=self.generar_reporte,
                  bg=COLOR_BOTON,
                  fg=COLOR_TEXTO_OSCURO,
                  font=("Arial", 12, "bold"),
                  relief="flat",
                  padx=30,
                  pady=6).pack(pady=10)

    def generar_reporte(self):
        """Genera un reporte de ventas agrupadas por servicio."""
        try:
            self.tabla.delete(*self.tabla.get_children())
            sql = """
                SELECT s.nombre AS servicio, 
                       COUNT(v.id) AS ventas, 
                       IFNULL(SUM(v.total), 0) AS ingresos
                FROM servicios s
                         LEFT JOIN ventas v ON s.id = v.servicio_id
                GROUP BY s.id
                ORDER BY ingresos DESC;
            """
            cur = self.db.execute(sql)
            resultados = cur.fetchall()

            if not resultados:
                messagebox.showinfo("Reporte vacío", "No se encontraron datos de ventas.")
                return

            for fila in resultados:
                self.tabla.insert("", tk.END, values=fila)

            print("Reporte generado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el reporte.\n{e}")
            print("Error en generar_reporte:", e)