import tkinter as tk
from tkinter import ttk, messagebox, font as tkFont
from PIL import Image, ImageTk
import sqlite3

DB_PATH = "espacio_creativo.db"

COLOR_FONDO_VENTANA = "#FFF9E6"
COLOR_FONDO_FRAME = "#FFF3C4"
COLOR_BOTON_AGREGAR = "#A7C7E7"
COLOR_BOTON_ACTUALIZAR = "#E6B325"
COLOR_BOTON_ELIMINAR = "#F8D7DA"
COLOR_BOTON_BUSCAR = "#B6E2A1"
COLOR_TEXTO_OSCURO = "#333333"

def conectar():
    return sqlite3.connect(DB_PATH)

def quick_sort_clientes(lista):
    if len(lista) <= 1:
        return lista
    pivote = lista[len(lista) // 2][1].lower()
    menores = [x for x in lista if x[1].lower() < pivote]
    iguales = [x for x in lista if x[1].lower() == pivote]
    mayores = [x for x in lista if x[1].lower() > pivote]
    return quick_sort_clientes(menores) + iguales + quick_sort_clientes(mayores)

def ventana_clientes():
    ventana = tk.Toplevel()
    ventana.title("Gestión de Clientes - Espacio Creativo")
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

    tk.Label(frame_superior, text="GESTIÓN DE CLIENTES",
             font=font_titulo, bg=COLOR_FONDO_VENTANA,
             fg=COLOR_TEXTO_OSCURO).pack(pady=5)

    def cerrar_clientes():
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
            command=cerrar_clientes
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
            command=cerrar_clientes
        ).place(relx=0.97, rely=0.05, anchor="ne")

    frame_form = tk.Frame(ventana, bg=COLOR_FONDO_FRAME, padx=25, pady=25)
    frame_form.pack(pady=(20, 10), padx=40, fill="x")

    tk.Label(frame_form, text="Nombre:", bg=COLOR_FONDO_FRAME, font=font_label).grid(row=0, column=0, sticky="e", pady=6, padx=8)
    entry_nombre = tk.Entry(frame_form, width=30)
    entry_nombre.grid(row=0, column=1, pady=6, padx=8)

    tk.Label(frame_form, text="Teléfono:", bg=COLOR_FONDO_FRAME, font=font_label).grid(row=1, column=0, sticky="e", pady=6, padx=8)
    entry_telefono = tk.Entry(frame_form, width=30)
    entry_telefono.grid(row=1, column=1, pady=6, padx=8)

    tk.Label(frame_form, text="Correo:", bg=COLOR_FONDO_FRAME, font=font_label).grid(row=2, column=0, sticky="e", pady=6, padx=8)
    entry_correo = tk.Entry(frame_form, width=30)
    entry_correo.grid(row=2, column=1, pady=6, padx=8)

    frame_botones = tk.Frame(ventana, bg=COLOR_FONDO_VENTANA)
    frame_botones.pack(pady=(25, 35), padx=50, anchor="w")

    estilo_boton = {"font": font_boton, "width": 14, "pady": 5, "relief": "flat", "cursor": "hand2"}

    def cargar_datos():
        tabla.delete(*tabla.get_children())
        conn = conectar()
        cur = conn.cursor()
        cur.execute("SELECT * FROM clientes")
        filas = cur.fetchall()
        conn.close()

        filas_ordenadas = quick_sort_clientes(filas)
        for fila in filas_ordenadas:
            tabla.insert("", "end", values=fila)

        print("Commit: Clientes cargados y ordenados por nombre (Quick Sort).")

    def agregar_cliente():
        n, t, c = entry_nombre.get(), entry_telefono.get(), entry_correo.get()
        if not n:
            messagebox.showwarning("Advertencia", "El nombre es obligatorio.")
            return
        conn = conectar()
        cur = conn.cursor()
        cur.execute("INSERT INTO clientes (nombre, telefono, correo) VALUES (?, ?, ?)", (n, t, c))
        conn.commit()
        conn.close()
        print(f"Commit: Cliente '{n}' agregado.")
        cargar_datos()

    def actualizar_cliente():
        sel = tabla.selection()
        if not sel:
            messagebox.showwarning("Selecciona", "Selecciona un cliente.")
            return
        cid = tabla.item(sel)["values"][0]
        n, t, c = entry_nombre.get(), entry_telefono.get(), entry_correo.get()
        conn = conectar()
        cur = conn.cursor()
        cur.execute("UPDATE clientes SET nombre=?, telefono=?, correo=? WHERE id=?", (n, t, c, cid))
        conn.commit()
        conn.close()
        print(f"Commit: Cliente id={cid} actualizado.")
        cargar_datos()

    def eliminar_cliente():
        sel = tabla.selection()
        if not sel:
            messagebox.showwarning("Selecciona", "Selecciona un cliente.")
            return
        cid = tabla.item(sel)["values"][0]
        if messagebox.askyesno("Confirmar", "¿Deseas eliminar este cliente?"):
            conn = conectar()
            cur = conn.cursor()
            cur.execute("DELETE FROM clientes WHERE id=?", (cid,))
            conn.commit()
            conn.close()
            print(f"Commit: Cliente id={cid} eliminado.")
            cargar_datos()

    def buscar_cliente():
        key = entry_buscar.get().strip().lower()
        if not key:
            messagebox.showwarning("Advertencia", "Ingresa un nombre para buscar.")
            return

        encontrado = False
        for child in tabla.get_children():
            valores = tabla.item(child, "values")
            if key in valores[1].lower():
                tabla.selection_set(child)
                tabla.focus(child)
                tabla.see(child)
                encontrado = True
                print(f"Commit: Cliente '{valores[1]}' encontrado (búsqueda secuencial).")
                break

        if not encontrado:
            messagebox.showinfo("No encontrado", "No se encontró el cliente.")
            print("Commit: búsqueda secuencial no encontró resultado.")

    tk.Button(frame_botones, text="Agregar", bg=COLOR_BOTON_AGREGAR, command=agregar_cliente, **estilo_boton).pack(side="left", padx=15)
    tk.Button(frame_botones, text="Actualizar", bg=COLOR_BOTON_ACTUALIZAR, command=actualizar_cliente, **estilo_boton).pack(side="left", padx=15)
    tk.Button(frame_botones, text="Eliminar", bg=COLOR_BOTON_ELIMINAR, command=eliminar_cliente, **estilo_boton).pack(side="left", padx=15)

    entry_buscar = tk.Entry(frame_botones, width=20, font=font_label)
    entry_buscar.pack(side="left", padx=(40, 10))
    tk.Button(frame_botones, text="Buscar", bg=COLOR_BOTON_BUSCAR, command=buscar_cliente, **estilo_boton).pack(side="left")

    columnas = ("id", "nombre", "telefono", "correo")
    tabla = ttk.Treeview(ventana, columns=columnas, show="headings", height=14)
    tabla.pack(fill="both", expand=True, pady=10, padx=20)

    for col in columnas:
        tabla.heading(col, text=col.capitalize())
        tabla.column(col, anchor="center")

    def seleccionar(event):
        sel = tabla.selection()
        if not sel:
            return
        r = tabla.item(sel)["values"]
        entry_nombre.delete(0, tk.END); entry_nombre.insert(0, r[1])
        entry_telefono.delete(0, tk.END); entry_telefono.insert(0, r[2])
        entry_correo.delete(0, tk.END); entry_correo.insert(0, r[3])
    tabla.bind("<<TreeviewSelect>>", seleccionar)

    cargar_datos()
    print("Commit: Ventana de Clientes abierta con diseño mejorado y coherente.")