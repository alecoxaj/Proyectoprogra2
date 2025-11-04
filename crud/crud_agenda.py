import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import sqlite3

DB_PATH = "espacio_creativo.db"

COLOR_FONDO_VENTANA = "#FFF9E6"
COLOR_FONDO_FRAME = "#FFF3C4"
COLOR_BOTON_AGREGAR = "#A7C7E7"
COLOR_BOTON_ACTUALIZAR = "#E6B325"
COLOR_BOTON_ELIMINAR = "#F8D7DA"


def ventana_agenda():
    ventana = tk.Toplevel()
    ventana.title("Agenda - Espacio Creativo")
    ventana.geometry("720x480")
    ventana.config(bg=COLOR_FONDO_VENTANA)


    frame_form = tk.Frame(ventana, bg=COLOR_FONDO_FRAME, padx=10, pady=10)
    frame_form.pack(fill="x", pady=10)

    tk.Label(frame_form, text="Cliente ID:", bg=COLOR_FONDO_FRAME).grid(row=0, column=0, sticky="e", pady=5, padx=5)
    entry_cliente = tk.Entry(frame_form, width=20)
    entry_cliente.grid(row=0, column=1, pady=5, padx=5)

    tk.Label(frame_form, text="Servicio ID:", bg=COLOR_FONDO_FRAME).grid(row=1, column=0, sticky="e", pady=5, padx=5)
    entry_servicio = tk.Entry(frame_form, width=20)
    entry_servicio.grid(row=1, column=1, pady=5, padx=5)


    tk.Label(frame_form, text="Fecha:", bg=COLOR_FONDO_FRAME).grid(row=2, column=0, sticky="e", pady=5, padx=5)
    entry_fecha = DateEntry(frame_form, width=18, background="#E6B325", foreground="black",
                            borderwidth=2, date_pattern="yyyy-mm-dd")
    entry_fecha.grid(row=2, column=1, pady=5, padx=5)

    tk.Label(frame_form, text="Estado:", bg=COLOR_FONDO_FRAME).grid(row=3, column=0, sticky="e", pady=5, padx=5)
    entry_estado = tk.Entry(frame_form, width=20)
    entry_estado.grid(row=3, column=1, pady=5, padx=5)



    def cargar_agenda():
        for fila in tabla.get_children():
            tabla.delete(fila)

        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM agenda")
        registros = cursor.fetchall()
        conexion.close()

        for r in registros:
            tabla.insert("", "end", values=r)

    def agregar():
        cliente_id = entry_cliente.get()
        servicio_id = entry_servicio.get()
        fecha = entry_fecha.get()
        estado = entry_estado.get()

        if not cliente_id or not servicio_id or not estado:
            messagebox.showwarning("Campos vacíos", "Por favor completa todos los campos.")
            print("Commit: intento fallido de agregar agenda (campos vacíos).")
            return

        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO agenda (cliente_id, servicio_id, fecha, estado) VALUES (?, ?, ?, ?)",
            (cliente_id, servicio_id, fecha, estado)
        )
        conexion.commit()
        conexion.close()
        cargar_agenda()
        print(f"Commit: Agenda agregada para cliente {cliente_id} en fecha {fecha}.")
        messagebox.showinfo("Éxito", "Registro agregado correctamente.")

    def actualizar():
        seleccionado = tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Sin selección", "Selecciona un registro para actualizar.")
            return

        id_agenda = tabla.item(seleccionado)["values"][0]
        cliente_id = entry_cliente.get()
        servicio_id = entry_servicio.get()
        fecha = entry_fecha.get()
        estado = entry_estado.get()

        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE agenda 
            SET cliente_id=?, servicio_id=?, fecha=?, estado=?
            WHERE id=?
        """, (cliente_id, servicio_id, fecha, estado, id_agenda))
        conexion.commit()
        conexion.close()
        cargar_agenda()
        print(f"Commit: Registro de agenda {id_agenda} actualizado.")
        messagebox.showinfo("Actualización", "Registro actualizado correctamente.")

    def eliminar():
        seleccionado = tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Sin selección", "Selecciona un registro para eliminar.")
            return

        id_agenda = tabla.item(seleccionado)["values"][0]

        if messagebox.askyesno("Confirmar", "¿Deseas eliminar este registro?"):
            conexion = sqlite3.connect(DB_PATH)
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM agenda WHERE id=?", (id_agenda,))
            conexion.commit()
            conexion.close()
            cargar_agenda()
            print(f"Commit: Registro de agenda {id_agenda} eliminado.")
            messagebox.showinfo("Eliminado", "Registro eliminado correctamente.")


    frame_botones = tk.Frame(ventana, bg=COLOR_FONDO_VENTANA)
    frame_botones.pack(fill="x", pady=10)

    tk.Button(frame_botones, text="Agregar", bg=COLOR_BOTON_AGREGAR, width=12, command=agregar).grid(row=0, column=0, padx=10)
    tk.Button(frame_botones, text="Actualizar", bg=COLOR_BOTON_ACTUALIZAR, width=12, command=actualizar).grid(row=0, column=1, padx=10)
    tk.Button(frame_botones, text="Eliminar", bg=COLOR_BOTON_ELIMINAR, width=12, command=eliminar).grid(row=0, column=2, padx=10)


    columnas = ("id", "cliente_id", "servicio_id", "fecha", "estado")
    tabla = ttk.Treeview(ventana, columns=columnas, show="headings", height=12)
    tabla.pack(fill="both", expand=True, pady=10)

    for col in columnas:
        tabla.heading(col, text=col.capitalize())
        tabla.column(col, anchor="center")

    cargar_agenda()

    print("Commit: Ventana Agenda abierta con selector de calendario.")


class AgendaView:
    def __init__(self, master=None):
        ventana_agenda()
