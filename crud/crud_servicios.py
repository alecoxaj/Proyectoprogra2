import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

DB_PATH = "espacio_creativo.db"

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
    ventana.geometry("650x420")
    ventana.config(bg="#fbfdfd")


    tk.Label(ventana, text="Nombre:").grid(row=0, column=0, padx=6, pady=6, sticky="e")
    entry_nombre = tk.Entry(ventana, width=30); entry_nombre.grid(row=0, column=1)
    tk.Label(ventana, text="Descripción:").grid(row=1, column=0, padx=6, pady=6, sticky="e")
    entry_desc = tk.Entry(ventana, width=30); entry_desc.grid(row=1, column=1)
    tk.Label(ventana, text="Precio:").grid(row=2, column=0, padx=6, pady=6, sticky="e")
    entry_precio = tk.Entry(ventana, width=30); entry_precio.grid(row=2, column=1)


    cols = ("id", "nombre", "descripcion", "precio")
    tabla = ttk.Treeview(ventana, columns=cols, show="headings", height=12)
    for c in cols:
        tabla.heading(c, text=c.capitalize())
    tabla.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

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
            tabla.insert("", tk.END, values=fila)

        print("Commit: Servicios cargados en tabla y ordenados por precio (Shell Sort).")

    def agregar_servicio():
        n, d, p = entry_nombre.get(), entry_desc.get(), entry_precio.get()
        if not (n and p):
            messagebox.showwarning("Advertencia", "Nombre y precio son obligatorios.")
            return
        try:
            precio_f = float(p)
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
            precio_f = float(p)
        except:
            messagebox.showerror("Error", "El precio debe ser numérico.")
            return
        conn = conectar(); cur = conn.cursor()
        cur.execute("UPDATE servicios SET nombre=?, descripcion=?, precio=? WHERE id=?", (n, d, precio_f, sid))
        conn.commit(); conn.close()
        print(f"Commit: Servicio id={sid} actualizado.")
        cargar_datos()

    def buscar_servicio():
        key = entry_nombre.get().strip().lower()
        for s in servicios_cache:
            if key in s[1].lower():
                messagebox.showinfo("Resultado", f"Servicio encontrado:\n{s}")
                print(f"Commit: Servicio '{s[1]}' encontrado (búsqueda secuencial).")
                return
        messagebox.showinfo("No encontrado", "No se encontró el servicio.")
        print("Commit: búsqueda secuencial no encontró resultado.")

    def seleccionar(event):
        sel = tabla.selection()
        if not sel: return
        r = tabla.item(sel)["values"]
        entry_nombre.delete(0, tk.END); entry_nombre.insert(0, r[1])
        entry_desc.delete(0, tk.END); entry_desc.insert(0, r[2])
        entry_precio.delete(0, tk.END); entry_precio.insert(0, r[3])

    tabla.bind("<<TreeviewSelect>>", seleccionar)


    tk.Button(ventana, text="Agregar", command=agregar_servicio, bg="#b8f2e6").grid(row=4, column=0, padx=6)
    tk.Button(ventana, text="Actualizar", command=actualizar_servicio, bg="#fff3b0").grid(row=4, column=1, padx=6)
    tk.Button(ventana, text="Eliminar", command=eliminar_servicio, bg="#ffd6d6").grid(row=4, column=2, padx=6)
    tk.Button(ventana, text="Buscar", command=buscar_servicio, bg="#dcedc1").grid(row=4, column=3, padx=6)

    cargar_datos()
    print("Commit: Ventana de Servicios inicializada con Shell Sort.")
