import tkinter as tk
from tkinter import ttk, messagebox, font as tkFont
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import sqlite3

DB_PATH = "espacio_creativo.db"

COLOR_FONDO_VENTANA = "#FFF9E6"
COLOR_FONDO_FRAME = "#FFF3C4"
COLOR_BOTON_AGREGAR = "#A7C7E7"
COLOR_BOTON_ACTUALIZAR = "#E6B325"
COLOR_BOTON_ELIMINAR = "#F8D7DA"
COLOR_TEXTO_OSCURO = "#333333"

def selection_sort_agenda(lista):
    n = len(lista)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if lista[j][3] < lista[min_idx][3]:
                min_idx = j
        lista[i], lista[min_idx] = lista[min_idx], lista[i]
    return lista

def ventana_agenda():
    ventana = tk.Toplevel()
    ventana.title("Agenda - Espacio Creativo")
    ventana.config(bg=COLOR_FONDO_VENTANA)

    try:
        ventana.state('zoomed')
    except tk.TclError:
        ventana.geometry("1200x800")

    FAMILIA_FUENTE = "Montserrat"
    font_titulo = tkFont.Font(family=FAMILIA_FUENTE, size=18, weight="bold")
    font_label = tkFont.Font(family=FAMILIA_FUENTE, size=11)
    font_boton = tkFont.Font(family=FAMILIA_FUENTE, size=10, weight="bold")

    frame_superior = tk.Frame(ventana, bg=COLOR_FONDO_VENTANA)
    frame_superior.pack(fill="x", pady=(15, 10))

    tk.Label(frame_superior, text="GESTIÓN DE AGENDA",
             font=font_titulo, bg=COLOR_FONDO_VENTANA,
             fg=COLOR_TEXTO_OSCURO).pack(pady=5)

    def cerrar_agenda():
        ventana.destroy()

    try:
        imagen_salir = Image.open("logo.salir.png").resize((40, 40))
        icono_salir = ImageTk.PhotoImage(imagen_salir)
        boton_salir = tk.Button(
            frame_superior,
            image=icono_salir,
            bg=COLOR_FONDO_VENTANA,
            borderwidth=0,
            cursor="hand2",
            command=cerrar_agenda
        )
        boton_salir.image = icono_salir
        boton_salir.place(relx=0.98, rely=0.05, anchor="ne")
    except Exception as e:
        print(f"No se pudo cargar el icono salir: {e}")
        tk.Button(
            frame_superior,
            text="Salir",
            bg=COLOR_BOTON_ELIMINAR,
            fg=COLOR_TEXTO_OSCURO,
            font=font_boton,
            relief="flat",
            cursor="hand2",
            command=cerrar_agenda
        ).place(relx=0.97, rely=0.05, anchor="ne")

    frame_form = tk.Frame(ventana, bg=COLOR_FONDO_FRAME, padx=20, pady=20)
    frame_form.pack(pady=15, padx=40, fill="x")

    tk.Label(frame_form, text="Cliente ID:", bg=COLOR_FONDO_FRAME, font=font_label).grid(row=0, column=0, sticky="e", pady=6, padx=8)
    entry_cliente = tk.Entry(frame_form, width=25)
    entry_cliente.grid(row=0, column=1, pady=6, padx=8)

    tk.Label(frame_form, text="Servicio ID:", bg=COLOR_FONDO_FRAME, font=font_label).grid(row=1, column=0, sticky="e", pady=6, padx=8)
    entry_servicio = tk.Entry(frame_form, width=25)
    entry_servicio.grid(row=1, column=1, pady=6, padx=8)

    tk.Label(frame_form, text="Fecha:", bg=COLOR_FONDO_FRAME, font=font_label).grid(row=2, column=0, sticky="e", pady=6, padx=8)
    entry_fecha = DateEntry(frame_form, width=23, background="#E6B325", foreground="black",
                            borderwidth=2, date_pattern="yyyy-mm-dd")
    entry_fecha.grid(row=2, column=1, pady=6, padx=8)

    tk.Label(frame_form, text="Estado:", bg=COLOR_FONDO_FRAME, font=font_label).grid(row=3, column=0, sticky="e", pady=6, padx=8)
    entry_estado = tk.Entry(frame_form, width=25)
    entry_estado.grid(row=3, column=1, pady=6, padx=8)

    frame_botones = tk.Frame(ventana, bg=COLOR_FONDO_VENTANA)
    frame_botones.pack(pady=(25, 35), padx=50, anchor="w")  # antes no tenía anchor

    estilo_boton = {
        "font": font_boton,
        "width": 14,
        "pady": 5,
        "relief": "flat",
        "cursor": "hand2"
    }

    tk.Button(frame_botones, text="Agregar", bg=COLOR_BOTON_AGREGAR, command=lambda: agregar(), **estilo_boton).pack(
        side="left", padx=15)
    tk.Button(frame_botones, text="Actualizar", bg=COLOR_BOTON_ACTUALIZAR, command=lambda: actualizar(),
              **estilo_boton).pack(side="left", padx=15)
    tk.Button(frame_botones, text="Eliminar", bg=COLOR_BOTON_ELIMINAR, command=lambda: eliminar(), **estilo_boton).pack(
        side="left", padx=15)

    columnas = ("id", "cliente_id", "servicio_id", "fecha", "estado")
    tabla = ttk.Treeview(ventana, columns=columnas, show="headings", height=14)
    tabla.pack(fill="both", expand=True, pady=(10, 25), padx=30)

    for col in columnas:
        tabla.heading(col, text=col.capitalize())
        tabla.column(col, anchor="center")

    registros_cache = []

    def cargar_agenda():
        for fila in tabla.get_children():
            tabla.delete(fila)
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM agenda")
        registros = cursor.fetchall()
        conexion.close()
        registros_ordenados = selection_sort_agenda(registros)
        registros_cache.clear()
        registros_cache.extend(registros_ordenados)
        for r in registros_ordenados:
            tabla.insert("", "end", values=r)
        print("Commit: Agenda cargada y ordenada por fecha (Selection Sort).")

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
        messagebox.showinfo("Éxito", "Registro agregado correctamente")
        print(f"Commit: Agenda agregada para cliente {cliente_id} en fecha {fecha}.")

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
            WHERE id=?""",
            (cliente_id, servicio_id, fecha, estado, id_agenda))
        conexion.commit()
        conexion.close()
        cargar_agenda()
        messagebox.showinfo("Actualización", "Registro actualizado correctamente.")
        print(f"Commit: Registro de agenda {id_agenda} actualizado.")

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
            messagebox.showinfo("Eliminado", "Registro eliminado correctamente.")
            print(f"Commit: Registro de agenda {id_agenda} eliminado.")

    cargar_agenda()
    print("Commit: Ventana Agenda abierta con estilo unificado y maximizada.")

class AgendaView:
    def __init__(self, master=None):
        ventana_agenda()