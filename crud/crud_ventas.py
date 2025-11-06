import tkinter as tk
from tkinter import ttk, messagebox, font as tkFont
from PIL import Image, ImageTk
import sqlite3
from collections import deque
from datetime import datetime

DB_PATH = "espacio_creativo.db"

COLOR_FONDO_VENTANA = "#FFF9E6"
COLOR_FONDO_FRAME = "#FFF3C4"
COLOR_BOTON_AGREGAR = "#A7C7E7"
COLOR_BOTON_ACTUALIZAR = "#E6B325"
COLOR_BOTON_ELIMINAR = "#F8D7DA"
COLOR_BOTON_BUSCAR = "#DCEEDC"
COLOR_BOTON_CARGAR = "#DBEAFE"
COLOR_BOTON_ORDENAR = "#FFF3B0"
COLOR_BOTON_PROCESAR = "#D1F7C4"
COLOR_BOTON_ENCOLAR = "#BCE0FF"
COLOR_TEXTO_OSCURO = "#333333"

def conectar():
    return sqlite3.connect(DB_PATH)

ventas_queue = deque()

def bubble_sort_ventas(lista, key=lambda x: x):
    a = lista[:]
    n = len(a)
    for i in range(n):
        for j in range(0, n - i - 1):
            if key(a[j]) > key(a[j + 1]):
                a[j], a[j + 1] = a[j + 1], a[j]
    return a

def ventana_ventas():
    ventana = tk.Toplevel()
    ventana.title("Ventas - Espacio Creativo")
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

    tk.Label(frame_superior, text="GESTIÓN DE VENTAS",
             font=font_titulo, bg=COLOR_FONDO_VENTANA,
             fg=COLOR_TEXTO_OSCURO).pack(pady=5)

    def cerrar_ventas():
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
            command=cerrar_ventas
        )
        boton_salir.image = icono_salir
        boton_salir.place(relx=0.98, rely=0.05, anchor="ne")
    except Exception as e:
        tk.Button(
            frame_superior,
            text="Salir",
            bg=COLOR_BOTON_ELIMINAR,
            fg=COLOR_TEXTO_OSCURO,
            font=font_boton,
            relief="flat",
            cursor="hand2",
            command=cerrar_ventas
        ).place(relx=0.97, rely=0.05, anchor="ne")

    frame_form = tk.Frame(ventana, bg=COLOR_FONDO_FRAME, padx=20, pady=20)
    frame_form.pack(pady=15, padx=40, fill="x")

    tk.Label(frame_form, text="Cliente ID:", bg=COLOR_FONDO_FRAME, font=font_label, fg=COLOR_TEXTO_OSCURO).grid(row=0, column=0, sticky="e", pady=6, padx=8)
    entry_cliente = tk.Entry(frame_form, width=25)
    entry_cliente.grid(row=0, column=1, pady=6, padx=8)

    tk.Label(frame_form, text="Servicio ID:", bg=COLOR_FONDO_FRAME, font=font_label, fg=COLOR_TEXTO_OSCURO).grid(row=1, column=0, sticky="e", pady=6, padx=8)
    entry_servicio = tk.Entry(frame_form, width=25)
    entry_servicio.grid(row=1, column=1, pady=6, padx=8)

    tk.Label(frame_form, text="Total:", bg=COLOR_FONDO_FRAME, font=font_label, fg=COLOR_TEXTO_OSCURO).grid(row=2, column=0, sticky="e", pady=6, padx=8)
    entry_total = tk.Entry(frame_form, width=25)
    entry_total.grid(row=2, column=1, pady=6, padx=8)

    frame_botones = tk.Frame(ventana, bg=COLOR_FONDO_VENTANA)
    frame_botones.pack(pady=(25, 35), padx=50, anchor="w")

    estilo_boton = {
        "font": font_boton,
        "width": 16,
        "pady": 5,
        "relief": "flat",
        "cursor": "hand2"
    }

    tk.Button(frame_botones, text="Encolar venta", bg=COLOR_BOTON_ENCOLAR, fg=COLOR_TEXTO_OSCURO, command=lambda: encolar_venta(), **estilo_boton).pack(side="left", padx=15)
    tk.Button(frame_botones, text="Procesar siguiente venta", bg=COLOR_BOTON_PROCESAR, fg=COLOR_TEXTO_OSCURO, command=lambda: procesar_venta(), **estilo_boton).pack(side="left", padx=15)
    tk.Button(frame_botones, text="Eliminar venta (BD)", bg=COLOR_BOTON_ELIMINAR, fg=COLOR_TEXTO_OSCURO, command=lambda: eliminar_venta_bd(), **estilo_boton).pack(side="left", padx=15)
    tk.Button(frame_botones, text="Cargar ventas", bg=COLOR_BOTON_CARGAR, fg=COLOR_TEXTO_OSCURO, command=lambda: cargar_datos(False), **estilo_boton).pack(side="left", padx=15)
    tk.Button(frame_botones, text="Ordenar por total", bg=COLOR_BOTON_ORDENAR, fg=COLOR_TEXTO_OSCURO, command=lambda: cargar_datos(True), **estilo_boton).pack(side="left", padx=15)

    cols = ("id", "cliente_id", "servicio_id", "fecha", "total")
    tabla = ttk.Treeview(ventana, columns=cols, show="headings", height=14)
    for c in cols:
        tabla.heading(c, text=c.capitalize())
        tabla.column(c, anchor="center")
    tabla.pack(fill="both", expand=True, pady=(10, 25), padx=30)

    def cargar_datos(ordenar=False):
        tabla.delete(*tabla.get_children())
        conn = conectar(); cur = conn.cursor()
        cur.execute("SELECT * FROM ventas")
        ventas = cur.fetchall()
        conn.close()

        if ordenar:
            ventas = bubble_sort_ventas(ventas, key=lambda x: x[4])

        for f in ventas:
            id_, cliente_id, servicio_id, fecha, total = f
            total_formateado = f"Q. {float(total):.2f}"
            tabla.insert("", tk.END, values=(id_, cliente_id, servicio_id, fecha, total_formateado))

    def encolar_venta():
        try:
            cid = int(entry_cliente.get().strip())
            sid = int(entry_servicio.get().strip())
            total = float(entry_total.get().strip())
        except:
            messagebox.showerror("Error", "Datos inválidos.")
            return
        venta = {"cliente_id": cid, "servicio_id": sid, "total": total, "fecha": datetime.now().isoformat()}
        ventas_queue.append(venta)
        messagebox.showinfo("Cola", f"Venta en cola. Posición: {len(ventas_queue)}")

    def procesar_venta():
        if not ventas_queue:
            messagebox.showinfo("Cola", "No hay ventas en cola.")
            return
        v = ventas_queue.popleft()
        conn = conectar(); cur = conn.cursor()
        cur.execute("INSERT INTO ventas (cliente_id, servicio_id, fecha, total) VALUES (?,?,?,?)",
                    (v["cliente_id"], v["servicio_id"], v["fecha"], v["total"]))
        conn.commit(); conn.close()
        cargar_datos()

    def eliminar_venta_bd():
        sel = tabla.selection()
        if not sel:
            messagebox.showwarning("Selecciona", "Selecciona una venta para eliminar.")
            return
        vid = tabla.item(sel)["values"][0]
        if messagebox.askyesno("Confirmar", "¿Deseas eliminar este registro?"):
            conn = conectar(); cur = conn.cursor()
            cur.execute("DELETE FROM ventas WHERE id=?", (vid,))
            conn.commit(); conn.close()
            messagebox.showinfo("Eliminado", "Venta eliminada correctamente.")
            cargar_datos()

    cargar_datos()