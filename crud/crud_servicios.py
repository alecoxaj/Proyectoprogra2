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
COLOR_BOTON_BUSCAR = "#DCEEDC"
COLOR_TEXTO_OSCURO = "#333333"

def conectar():
    return sqlite3.connect(DB_PATH)

def shell_sort_servicios(lista, key=lambda x: x):
    a = lista[:]
    n = len(a)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = a[i]
            j = i
            while j >= gap and key(a[j - gap]) > key(temp):
                a[j] = a[j - gap]
                j -= gap
            a[j] = temp
        gap //= 2
    print("Commit: Ordenamiento Shell Sort ejecutado.")
    return a

def ventana_servicios():
    ventana = tk.Toplevel()
    ventana.title("Gestión de Servicios - Espacio Creativo")
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

    tk.Label(frame_superior, text="GESTIÓN DE SERVICIOS",
             font=font_titulo, bg=COLOR_FONDO_VENTANA,
             fg=COLOR_TEXTO_OSCURO).pack(pady=5)

    def cerrar_servicios():
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
            command=cerrar_servicios
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
            command=cerrar_servicios
        ).place(relx=0.97, rely=0.05, anchor="ne")

    frame_form = tk.Frame(ventana, bg=COLOR_FONDO_FRAME, padx=20, pady=20)
    frame_form.pack(pady=15, padx=40, fill="x")

    tk.Label(frame_form, text="Nombre:", bg=COLOR_FONDO_FRAME, font=font_label, fg=COLOR_TEXTO_OSCURO).grid(row=0, column=0, sticky="e", pady=6, padx=8)
    entry_nombre = tk.Entry(frame_form, width=25)
    entry_nombre.grid(row=0, column=1, pady=6, padx=8)

    tk.Label(frame_form, text="Descripción:", bg=COLOR_FONDO_FRAME, font=font_label, fg=COLOR_TEXTO_OSCURO).grid(row=1, column=0, sticky="e", pady=6, padx=8)
    entry_desc = tk.Entry(frame_form, width=25)
    entry_desc.grid(row=1, column=1, pady=6, padx=8)

    tk.Label(frame_form, text="Precio:", bg=COLOR_FONDO_FRAME, font=font_label, fg=COLOR_TEXTO_OSCURO).grid(row=2, column=0, sticky="e", pady=6, padx=8)
    entry_precio = tk.Entry(frame_form, width=25)
    entry_precio.grid(row=2, column=1, pady=6, padx=8)

    frame_botones = tk.Frame(ventana, bg=COLOR_FONDO_VENTANA)
    frame_botones.pack(pady=(25, 35), padx=50, anchor="w")

    estilo_boton = {
        "font": font_boton,
        "width": 14,
        "pady": 5,
        "relief": "flat",
        "cursor": "hand2"
    }

    tk.Button(frame_botones, text="Agregar", bg=COLOR_BOTON_AGREGAR, fg=COLOR_TEXTO_OSCURO, command=lambda: agregar_servicio(), **estilo_boton).pack(side="left", padx=15)
    tk.Button(frame_botones, text="Actualizar", bg=COLOR_BOTON_ACTUALIZAR, fg=COLOR_TEXTO_OSCURO, command=lambda: actualizar_servicio(), **estilo_boton).pack(side="left", padx=15)
    tk.Button(frame_botones, text="Eliminar", bg=COLOR_BOTON_ELIMINAR, fg=COLOR_TEXTO_OSCURO, command=lambda: eliminar_servicio(), **estilo_boton).pack(side="left", padx=15)

    frame_busqueda = tk.Frame(ventana, bg=COLOR_FONDO_VENTANA)
    frame_busqueda.pack(pady=(0, 15), padx=50, anchor="w")

    tk.Label(frame_busqueda, text="Buscar por nombre:", bg=COLOR_FONDO_VENTANA, font=font_label, fg=COLOR_TEXTO_OSCURO).pack(side="left", padx=(0, 10))
    entry_buscar = tk.Entry(frame_busqueda, width=20)
    entry_buscar.pack(side="left", padx=(0, 10))
    tk.Button(frame_busqueda, text="Buscar (Secuencial)", bg=COLOR_BOTON_BUSCAR, fg=COLOR_TEXTO_OSCURO, font=font_boton, relief="flat", cursor="hand2", command=lambda: buscar_servicio(entry_buscar.get())).pack(side="left")

    cols = ("id", "nombre", "descripcion", "precio")
    tabla = ttk.Treeview(ventana, columns=cols, show="headings", height=14)
    for c in cols:
        tabla.heading(c, text=c.capitalize())
        tabla.column(c, anchor="center")
    tabla.pack(fill="both", expand=True, pady=(10, 25), padx=30)

    servicios_cache = []

    def cargar_datos():
        tabla.delete(*tabla.get_children())
        conn = conectar()
        cur = conn.cursor()
        cur.execute("SELECT * FROM servicios")
        servicios_cache.clear()
        for fila in cur.fetchall():
            servicios_cache.append(fila)
        conn.close()

        servicios_ordenados = shell_sort_servicios(servicios_cache, key=lambda x: x[3])

        for fila in servicios_ordenados:
            tabla.insert("", tk.END, values=(fila[0], fila[1], fila[2], f"Q. {float(fila[3]):.2f}"))

        print("Commit: Servicios cargados en tabla y ordenados por precio (Shell Sort).")

    def agregar_servicio():
        n, d, p = entry_nombre.get(), entry_desc.get(), entry_precio.get()
        if not (n and p):
            messagebox.showwarning("Advertencia", "Nombre y precio son obligatorios.")
            return
        try:
            precio_f = float(str(p).replace("Q", "").replace("Q.", "").strip())
        except:
            messagebox.showerror("Error", "El precio debe ser numérico.")
            return
        conn = conectar(); cur = conn.cursor()
        cur.execute("INSERT INTO servicios (nombre, descripcion, precio) VALUES (?, ?, ?)", (n, d, precio_f))
        conn.commit(); conn.close()
        print(f"Commit: Servicio '{n}' agregado.")
        cargar_datos()

    def eliminar_servicio():
        sel = tabla.selection()
        if not sel:
            messagebox.showwarning("Selecciona", "Selecciona un servicio.")
            return
        sid = tabla.item(sel)["values"][0]
        if messagebox.askyesno("Confirmar", "¿Deseas eliminar este registro?"):
            conn = conectar(); cur = conn.cursor()
            cur.execute("DELETE FROM servicios WHERE id=?", (sid,))
            conn.commit(); conn.close()
            messagebox.showinfo("Eliminación de servicio", "Servicio eliminado")
            print(f"Commit: Servicio id={sid} eliminado.")
            cargar_datos()

    def actualizar_servicio():
        sel = tabla.selection()
        if not sel:
            messagebox.showwarning("Selecciona", "Selecciona un servicio.")
            return
        sid = tabla.item(sel)["values"][0]
        n, d, p = entry_nombre.get(), entry_desc.get(), entry_precio.get()
        try:
            precio_f = float(str(p).replace("Q", "").replace("Q.", "").strip())
        except:
            messagebox.showerror("Error", "El precio debe ser numérico.")
            return
        conn = conectar(); cur = conn.cursor()
        cur.execute("UPDATE servicios SET nombre=?, descripcion=?, precio=? WHERE id=?", (n, d, precio_f, sid))
        conn.commit(); conn.close()
        print(f"Commit: Servicio id={sid} actualizado.")
        cargar_datos()

    def buscar_servicio(termino):
        key = termino.strip().lower()
        if not key:
            messagebox.showwarning("Búsqueda", "Por favor ingresa un nombre para buscar.")
            return

        for s in servicios_cache:
            if key in s[1].lower():
                print(f"Commit: Servicio '{s[1]}' encontrado (búsqueda secuencial).")

                for item in tabla.get_children():
                    if tabla.item(item)["values"][0] == s[0]:
                        tabla.selection_set(item)
                        tabla.see(item)
                        break
                return

        messagebox.showinfo("No encontrado", "No se encontró el servicio.")
        print("Commit: búsqueda secuencial no encontró resultado.")

    def seleccionar(event):
        sel = tabla.selection()
        if not sel: return
        r = tabla.item(sel)["values"]
        entry_nombre.delete(0, tk.END)
        entry_nombre.insert(0, r[1])
        entry_desc.delete(0, tk.END)
        entry_desc.insert(0, r[2])
        entry_precio.delete(0, tk.END)
        entry_precio.insert(0, r[3])

    tabla.bind("<<TreeviewSelect>>", seleccionar)

    cargar_datos()
    print("Commit: Ventana de Servicios inicializada con estilo unificado, maximizada y Shell Sort.")