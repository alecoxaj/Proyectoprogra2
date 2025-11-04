import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

DB_PATH = "espacio_creativo.db"

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
    ventana.geometry("650x420")
    ventana.config(bg="#fdfcfb")

    tk.Label(ventana, text="Nombre:").grid(row=0, column=0, padx=6, pady=6, sticky="e")
    entry_nombre = tk.Entry(ventana, width=30)
    entry_nombre.grid(row=0, column=1)

    tk.Label(ventana, text="Teléfono:").grid(row=1, column=0, padx=6, pady=6, sticky="e")
    entry_telefono = tk.Entry(ventana, width=30)
    entry_telefono.grid(row=1, column=1)

    tk.Label(ventana, text="Correo:").grid(row=2, column=0, padx=6, pady=6, sticky="e")
    entry_correo = tk.Entry(ventana, width=30)
    entry_correo.grid(row=2, column=1)


    cols = ("id", "nombre", "telefono", "correo")
    tabla = ttk.Treeview(ventana, columns=cols, show="headings", height=12)
    for c in cols:
        tabla.heading(c, text=c.capitalize())
    tabla.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

    clientes_cache = []

    def cargar_datos():
        tabla.delete(*tabla.get_children())
        conn = conectar()
        cur = conn.cursor()
        cur.execute("SELECT * FROM clientes")
        clientes_cache.clear()
        for fila in cur.fetchall():
            clientes_cache.append(fila)
            tabla.insert("", tk.END, values=fila)
        conn.close()

        clientes_ordenados = quick_sort_clientes(clientes_cache)
        for fila in clientes_ordenados:
            tabla.insert("", tk.END, values=fila)

        print("Commit: Clientes cargados en tabla y ordenados por nombre (Quick Sort).")


    def agregar_cliente():
        n, t, c = entry_nombre.get(), entry_telefono.get(), entry_correo.get()
        if not n:
            messagebox.showwarning("Advertencia", "El nombre es obligatorio.")
            return
        conn = conectar()
        cur = conn.cursor()
        cur.execute("INSERT INTO clientes (nombre, telefono, correo) VALUES (?,?,?)", (n, t, c))
        conn.commit()
        conn.close()
        print(f"Commit: Cliente '{n}' agregado.")
        cargar_datos()

    def eliminar_cliente():
        sel = tabla.selection()
        if not sel:
            messagebox.showwarning("Selecciona", "Selecciona un cliente.")
            return
        cid = tabla.item(sel)["values"][0]
        conn = conectar()
        cur = conn.cursor()
        cur.execute("DELETE FROM clientes WHERE id=?", (cid,))
        conn.commit()
        conn.close()
        print(f"Commit: Cliente id={cid} eliminado.")
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

    def buscar_cliente():
        key = entry_nombre.get().strip().lower()
        for c in clientes_cache:
            if key in c[1].lower():
                messagebox.showinfo("Resultado", f"Cliente encontrado:\n{c}")
                print(f"Commit: Cliente '{c[1]}' encontrado (búsqueda secuencial).")
                return
        messagebox.showinfo("No encontrado", "No se encontró el cliente.")
        print("Commit: búsqueda secuencial no encontró resultado.")

    def seleccionar(event):
        sel = tabla.selection()
        if not sel: return
        r = tabla.item(sel)["values"]
        entry_nombre.delete(0, tk.END); entry_nombre.insert(0, r[1])
        entry_telefono.delete(0, tk.END); entry_telefono.insert(0, r[2])
        entry_correo.delete(0, tk.END); entry_correo.insert(0, r[3])

    tabla.bind("<<TreeviewSelect>>", seleccionar)

    tk.Button(ventana, text="Agregar", command=agregar_cliente, bg="#b8f2e6").grid(row=4, column=0, padx=6)
    tk.Button(ventana, text="Actualizar", command=actualizar_cliente, bg="#fff3b0").grid(row=4, column=1, padx=6)
    tk.Button(ventana, text="Eliminar", command=eliminar_cliente, bg="#ffd6d6").grid(row=4, column=2, padx=6)
    tk.Button(ventana, text="Buscar", command=buscar_cliente, bg="#dcedc1").grid(row=4, column=3, padx=6)

    cargar_datos()
    print("Commit: Ventana de Clientes inicializada con Quick Sort.")
