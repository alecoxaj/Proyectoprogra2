import tkinter as tk
from tkinter import ttk, messagebox, font as tkFont
import sqlite3
from PIL import Image, ImageTk

DB_PATH = "espacio_creativo.db"

COLOR_FONDO_VENTANA = "#FFF9E6"
COLOR_FONDO_FRAME = "#FFF3C4"
COLOR_BOTON_CARGAR = "#A7C7E7"
COLOR_BOTON_ORDENAR = "#F0C987"
COLOR_BOTON_HASHING = "#E1BEE7"
COLOR_BOTON_BUSCAR = "#B6E2A1"
COLOR_TEXTO_OSCURO = "#333333"

def conectar():
    return sqlite3.connect(DB_PATH)

def quick_sort(lista, key=lambda x: x):
    if len(lista) <= 1:
        return lista[:]
    pivote = lista[len(lista)//2]
    menores = [x for x in lista if key(x) < key(pivote)]
    iguales = [x for x in lista if key(x) == key(pivote)]
    mayores = [x for x in lista if key(x) > key(pivote)]
    return quick_sort(menores, key) + iguales + quick_sort(mayores, key)

def binary_search(lista, target, key=lambda x: x):
    lo, hi = 0, len(lista) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if key(lista[mid]) == target:
            return mid
        elif key(lista[mid]) < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1

def sequential_search(lista, target, key=lambda x: x):
    for i, item in enumerate(lista):
        if key(item) == target:
            return i
    return -1

def ventana_reportes():
    ventana = tk.Toplevel()
    ventana.title("Reportes - Espacio Creativo")
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

    tk.Label(frame_superior, text="REPORTES DE SERVICIOS",
             font=font_titulo, bg=COLOR_FONDO_VENTANA,
             fg=COLOR_TEXTO_OSCURO).pack(pady=5)

    def cerrar_reportes():
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
            command=cerrar_reportes
        )
        boton_salir.image = icono_salir
        boton_salir.place(relx=0.98, rely=0.05, anchor="ne")
    except Exception as e:
        print(f"No se pudo cargar el icono salir: {e}")
        tk.Button(frame_superior, text="Salir",
                  bg="#F8D7DA", fg=COLOR_TEXTO_OSCURO,
                  font=font_boton, relief="flat",
                  cursor="hand2", command=cerrar_reportes
                  ).place(relx=0.97, rely=0.05, anchor="ne")

    frame_botones = tk.Frame(ventana, bg=COLOR_FONDO_FRAME, padx=25, pady=25)
    frame_botones.pack(pady=(20, 10), padx=40, fill="x")

    estilo_boton = {"font": font_boton, "width": 18, "pady": 6, "relief": "flat", "cursor": "hand2"}

    def cargar_servicios():
        tabla.delete(*tabla.get_children())
        conn = conectar(); cur = conn.cursor()
        cur.execute("SELECT id, nombre, descripcion, precio FROM servicios")
        filas = cur.fetchall()
        conn.close()

        for f in filas:
            tabla.insert("", "end", values=(f[0], f[1], f[2], f"Q {f[3]:,.2f}"))
        print("Commit: Servicios cargados correctamente.")
        return filas

    def ordenar_servicios():
        filas = cargar_servicios()
        if not filas:
            messagebox.showinfo("Vacío", "No hay servicios para ordenar.")
            return
        ordenados = quick_sort(filas, key=lambda x: x[3])
        tabla.delete(*tabla.get_children())
        for f in ordenados:
            tabla.insert("", "end", values=(f[0], f[1], f[2], f"Q {f[3]:,.2f}"))
        messagebox.showinfo("Ordenamiento", "Servicios ordenados por precio (Quick Sort).")
        print("Commit: Ordenamiento Quick Sort aplicado en Reportes.")

    def buscar_binario():
        target_txt = entry_precio.get().strip()
        if not target_txt:
            messagebox.showwarning("Advertencia", "Ingresa un precio para buscar.")
            return
        try:
            target = float(target_txt)
        except ValueError:
            messagebox.showerror("Error", "El precio ingresado no es válido.")
            return

        filas = cargar_servicios()
        ordenadas = quick_sort(filas, key=lambda x: x[3])
        idx = binary_search(ordenadas, target, key=lambda x: x[3])

        if idx != -1:
            item = tabla.get_children()[idx]
            tabla.selection_set(item)
            tabla.focus(item)
            tabla.see(item)
            messagebox.showinfo("Resultado", f"Servicio con precio Q {target:.2f} encontrado.")
            print(f"Commit: Servicio con precio {target} encontrado (Búsqueda Binaria).")
        else:
            messagebox.showinfo("No encontrado", "No existe servicio con ese precio.")
            print("Commit: Búsqueda binaria sin resultados.")

    def buscar_secuencial():
        key = entry_nombre.get().strip().lower()
        if not key:
            messagebox.showwarning("Advertencia", "Ingresa un nombre para buscar.")
            return

        filas = cargar_servicios()
        idx = sequential_search(filas, key, key=lambda x: x[1].lower())

        if idx != -1:
            item = tabla.get_children()[idx]
            tabla.selection_set(item)
            tabla.focus(item)
            tabla.see(item)
            print(f"Commit: Servicio '{key}' encontrado (Búsqueda Secuencial).")
        else:
            messagebox.showinfo("No encontrado", "No existe servicio con ese nombre.")
            print("Commit: Búsqueda secuencial sin resultados.")

    def hashing_demo():
        filas = cargar_servicios()
        tabla_hash = {f[1]: f for f in filas}
        messagebox.showinfo("Hashing", f"Tabla hash creada con {len(tabla_hash)} servicios.")
        print("Commit: Hash Table de servicios creada exitosamente.")

    tk.Button(frame_botones, text="Cargar Servicios", bg=COLOR_BOTON_CARGAR,
              command=cargar_servicios, **estilo_boton).pack(side="left", padx=10)
    tk.Button(frame_botones, text="Ordenar (Quick Sort)", bg=COLOR_BOTON_ORDENAR,
              command=ordenar_servicios, **estilo_boton).pack(side="left", padx=10)
    tk.Button(frame_botones, text="Hashing Demo", bg=COLOR_BOTON_HASHING,
              command=hashing_demo, **estilo_boton).pack(side="left", padx=10)

    frame_buscar = tk.Frame(ventana, bg=COLOR_FONDO_VENTANA)
    frame_buscar.pack(pady=(10, 20))

    tk.Label(frame_buscar, text="Buscar por Precio:", bg=COLOR_FONDO_VENTANA, font=font_label).grid(row=0, column=0, padx=10)
    entry_precio = tk.Entry(frame_buscar, width=15, font=font_label)
    entry_precio.grid(row=0, column=1, padx=10)
    tk.Button(frame_buscar, text="Buscar (Binaria)", bg=COLOR_BOTON_BUSCAR,
              command=buscar_binario, **estilo_boton).grid(row=0, column=2, padx=10)

    tk.Label(frame_buscar, text="Buscar por Nombre:", bg=COLOR_FONDO_VENTANA, font=font_label).grid(row=1, column=0, padx=10, pady=10)
    entry_nombre = tk.Entry(frame_buscar, width=20, font=font_label)
    entry_nombre.grid(row=1, column=1, padx=10)
    tk.Button(frame_buscar, text="Buscar (Secuencial)", bg=COLOR_BOTON_BUSCAR,
              command=buscar_secuencial, **estilo_boton).grid(row=1, column=2, padx=10)

    columnas = ("id", "nombre", "descripcion", "precio")
    tabla = ttk.Treeview(ventana, columns=columnas, show="headings", height=14)
    tabla.pack(fill="both", expand=True, pady=10, padx=20)

    for col in columnas:
        tabla.heading(col, text=col.capitalize())
        tabla.column(col, anchor="center")

    cargar_servicios()
    print("Commit: Ventana de Reportes abierta con interfaz moderna y coherente.")