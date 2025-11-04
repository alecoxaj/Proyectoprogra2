import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

DB_PATH = "espacio_creativo.db"

def conectar():
    return sqlite3.connect(DB_PATH)

def quick_sort(arr, key=lambda x: x):
    if len(arr) <= 1:
        return arr[:]
    pivot = arr[len(arr)//2]
    left = [x for x in arr if key(x) < key(pivot)]
    middle = [x for x in arr if key(x) == key(pivot)]
    right = [x for x in arr if key(x) > key(pivot)]
    sorted_arr = quick_sort(left, key) + middle + quick_sort(right, key)
    print("Commit: Ordenamiento Quick Sort ejecutado (recursivo).")
    return sorted_arr

def binary_search(sorted_list, target, key=lambda x: x):
    lo, hi = 0, len(sorted_list)-1
    while lo <= hi:
        mid = (lo+hi)//2
        if key(sorted_list[mid]) == target:
            print("Commit: Búsqueda binaria encontró el objetivo.")
            return mid
        elif key(sorted_list[mid]) < target:
            lo = mid + 1
        else:
            hi = mid - 1
    print("Commit: Búsqueda binaria no encontró el objetivo.")
    return -1

def sequential_search(lst, target, key=lambda x: x):
    for i, item in enumerate(lst):
        if key(item) == target:
            print("Commit: Búsqueda secuencial encontró el objetivo.")
            return i
    print("Commit: Búsqueda secuencial no encontró el objetivo.")
    return -1

def ventana_reportes():
    ventana = tk.Toplevel()
    ventana.title("Reportes - Espacio Creativo")
    ventana.geometry("760x480")
    ventana.config(bg="#ffffff")


    cols = ("id","nombre","descripcion","precio")
    tabla = ttk.Treeview(ventana, columns=cols, show="headings", height=12)
    for c in cols: tabla.heading(c, text=c.capitalize())
    tabla.grid(row=3, column=0, columnspan=6, padx=10, pady=10)

    def cargar_servicios():
        tabla.delete(*tabla.get_children())
        conn = conectar(); cur = conn.cursor()
        cur.execute("SELECT id, nombre, descripcion, precio FROM servicios")
        rows = cur.fetchall()
        for r in rows:
            tabla.insert("", tk.END, values=r)
        conn.close()
        print("Commit: Servicios cargados para reportes.")
        return rows

    def ordenar_y_mostrar(alg):
        rows = cargar_servicios()
        if not rows:
            messagebox.showinfo("Info", "No hay servicios para ordenar.")
            return
        sorted_rows = quick_sort(rows, key=lambda x: x[3])
        tabla.delete(*tabla.get_children())
        print("Commit: Ordenamiento Quick Sort (recursivo) ejecutado.")
        for r in sorted_rows:
            tabla.insert("", tk.END, values=r)
        messagebox.showinfo("Ordenamiento", f"Ordenamiento {alg} aplicado.")

    def buscar_por_precio_binario():
        target_txt = entry_target.get().strip()
        if not target_txt:
            messagebox.showwarning("Entrada", "Ingresa precio a buscar.")
            return
        try:
            target = float(target_txt)
        except:
            messagebox.showerror("Error", "Precio inválido.")
            return
        rows = cargar_servicios()
        sorted_rows = quick_sort(rows, key=lambda x: x[3])
        idx = binary_search(sorted_rows, target, key=lambda x: x[3])
        if idx >= 0:
            messagebox.showinfo("Encontrado", f"Encontrado: {sorted_rows[idx]}")
        else:
            messagebox.showinfo("No encontrado", "No existe servicio con ese precio.")

    def buscar_secuencial_nombre():
        key = entry_nombre.get().strip().lower()
        rows = cargar_servicios()
        idx = sequential_search(rows, key, key=lambda x: x[1].lower())
        if idx >= 0:
            messagebox.showinfo("Encontrado", f"Encontrado: {rows[idx]}")
        else:
            messagebox.showinfo("No encontrado", "No existe servicio con ese nombre.")

    def hashing_demo():
        rows = cargar_servicios()
        hash_table = {r[1]: r for r in rows}
        messagebox.showinfo("Hashing", f"Tabla hash creada con {len(hash_table)} servicios.")
        print("Commit: Hash table de servicios creada correctamente.")

    tk.Button(ventana, text="Cargar servicios", command=cargar_servicios, bg="#dbeafe").grid(row=0, column=0, padx=6, pady=6)
    tk.Button(ventana, text="Ordenar (Quick Sort)", command=ordenar_y_mostrar, bg="#f0f4c3").grid(row=0, column=1)
    tk.Button(ventana, text="Hashing demo", command=hashing_demo, bg="#e1bee7").grid(row=0, column=2)


    tk.Label(ventana, text="Buscar por precio (binaria):").grid(row=1, column=0, padx=6, pady=6, sticky="e")
    entry_target = tk.Entry(ventana, width=15)
    entry_target.grid(row=1, column=1)
    tk.Button(ventana, text="Buscar (binaria)", command=buscar_por_precio_binario, bg="#bbdefb").grid(row=1, column=2)



    tk.Label(ventana, text="Buscar por nombre (secuencial):").grid(row=2, column=0, sticky="e")
    entry_nombre = tk.Entry(ventana, width=20)
    entry_nombre.grid(row=2, column=1)
    tk.Button(ventana, text="Buscar (secuencial)", command=buscar_secuencial_nombre, bg="#c8e6c9").grid(row=2, column=2)

    print("Commit: Ventana de Reportes inicializada con Quick Sort, búsquedas y hashing.")
