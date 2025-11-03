import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

DB_PATH = "espacio_creativo.db"

def conectar():
    return sqlite3.connect(DB_PATH)


def bubble_sort(arr, key=lambda x: x):
    a = arr[:]
    n = len(a)
    for i in range(n):
        for j in range(0, n-i-1):
            if key(a[j]) > key(a[j+1]):
                a[j], a[j+1] = a[j+1], a[j]
    print("Commit: Ordenamiento Bubble Sort ejecutado.")
    return a

def shell_sort(arr, key=lambda x: x):
    a = arr[:]
    n = len(a)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = a[i]
            j = i
            while j >= gap and key(a[j-gap]) > key(temp):
                a[j] = a[j-gap]
                j -= gap
            a[j] = temp
        gap //= 2
    print("Commit: Ordenamiento Shell Sort ejecutado.")
    return a

def quick_sort(arr, key=lambda x: x):
    if len(arr) <= 1:
        return arr[:]
    pivot = arr[len(arr)//2]
    left = [x for x in arr if key(x) < key(pivot)]
    middle = [x for x in arr if key(x) == key(pivot)]
    right = [x for x in arr if key(x) > key(pivot)]
    sorted_arr = quick_sort(left, key) + middle + quick_sort(right, key)
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

import random
def bogo_sort(arr, key=lambda x: x, limit=5000):
    a = arr[:]
    attempts = 0
    def ordered(a):
        return all(key(a[i]) <= key(a[i+1]) for i in range(len(a)-1))
    while not ordered(a) and attempts < limit:
        random.shuffle(a)
        attempts += 1
    print(f"Commit: Bogo sort ejecutado (intentos={attempts}).")
    return a


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
        for r in rows: tabla.insert("", tk.END, values=r)
        conn.close()
        print("Commit: Servicios cargados para reportes.")
        return rows

    def ordenar_y_mostrar(alg):
        rows = cargar_servicios()
        if not rows:
            messagebox.showinfo("Info", "No hay servicios para ordenar.")
            return
        if alg == "bubble":
            sorted_rows = bubble_sort(rows, key=lambda x: x[3])
        elif alg == "shell":
            sorted_rows = shell_sort(rows, key=lambda x: x[3])
        elif alg == "quick":
            sorted_rows = quick_sort(rows, key=lambda x: x[3])
            print("Commit: Ordenamiento Quick Sort (recursivo) ejecutado.")
        elif alg == "bogo":
            sorted_rows = bogo_sort(rows, key=lambda x: x[3], limit=2000)
        else:
            return
        tabla.delete(*tabla.get_children())
        for r in sorted_rows: tabla.insert("", tk.END, values=r)
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

    def hashing_demo():
        rows = cargar_servicios()
        hash_table = {}
        for r in rows:
            hash_table[r[1]] = r
        messagebox.showinfo("Hashing", f"Hash built: {len(hash_table)} elementos (lookup O(1) promedio)")
        print("Commit: Tabla hash de servicios construida.")

    tk.Button(ventana, text="Cargar servicios", command=cargar_servicios, bg="#dbeafe").grid(row=0, column=0, padx=6, pady=6)
    tk.Button(ventana, text="Ordenar (Bubble)", command=lambda: ordenar_y_mostrar("bubble"), bg="#ffe0b2").grid(row=0, column=1)
    tk.Button(ventana, text="Ordenar (Shell)", command=lambda: ordenar_y_mostrar("shell"), bg="#c8e6c9").grid(row=0, column=2)
    tk.Button(ventana, text="Ordenar (Quick)", command=lambda: ordenar_y_mostrar("quick"), bg="#f0f4c3").grid(row=0, column=3)
    tk.Button(ventana, text="Ordenar (Bogo demo)", command=lambda: ordenar_y_mostrar("bogo"), bg="#ffcdd2").grid(row=0, column=4)
    tk.Button(ventana, text="Hashing demo", command=hashing_demo, bg="#e1bee7").grid(row=0, column=5)


    tk.Label(ventana, text="Buscar por precio (binaria):").grid(row=1, column=0, padx=6, pady=6, sticky="e")
    entry_target = tk.Entry(ventana, width=15); entry_target.grid(row=1, column=1)
    tk.Button(ventana, text="Buscar (binaria)", command=buscar_por_precio_binario, bg="#bbdefb").grid(row=1, column=2)


    def buscar_secuencial_nombre():
        key = entry_nombre.get().strip().lower()
        rows = cargar_servicios()
        idx = sequential_search(rows, key, key=lambda x: x[1].lower())
        if idx >= 0:
            messagebox.showinfo("Encontrado", f"Encontrado: {rows[idx]}")
        else:
            messagebox.showinfo("No encontrado", "No existe servicio con ese nombre.")

    tk.Label(ventana, text="Buscar por nombre (secuencial):").grid(row=2, column=0, sticky="e")
    entry_nombre = tk.Entry(ventana, width=20); entry_nombre.grid(row=2, column=1)
    tk.Button(ventana, text="Buscar (secuencial)", command=buscar_secuencial_nombre, bg="#c8e6c9").grid(row=2, column=2)

    print("Commit: Ventana de Reportes inicializada con algoritmos.")
