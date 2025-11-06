import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from collections import deque
from datetime import datetime

DB_PATH = "espacio_creativo.db"

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
    print("Commit: Ordenamiento Bubble Sort ejecutado en ventas.")
    return a

def ventana_ventas():
    ventana = tk.Toplevel()
    ventana.title("Ventas - Espacio Creativo")
    ventana.geometry("700x420")
    ventana.config(bg="#fbfbff")

    tk.Label(ventana, text="Cliente ID:").grid(row=0, column=0, padx=6, pady=6)
    entry_cliente = tk.Entry(ventana, width=20); entry_cliente.grid(row=0, column=1)
    tk.Label(ventana, text="Servicio ID:").grid(row=1, column=0, padx=6, pady=6)
    entry_servicio = tk.Entry(ventana, width=20); entry_servicio.grid(row=1, column=1)
    tk.Label(ventana, text="Total:").grid(row=2, column=0, padx=6, pady=6)
    entry_total = tk.Entry(ventana, width=15); entry_total.grid(row=2, column=1)

    cols = ("id","cliente_id","servicio_id","fecha","total")
    tabla = ttk.Treeview(ventana, columns=cols, show="headings", height=12)
    for c in cols: tabla.heading(c, text=c.capitalize())
    tabla.grid(row=6, column=0, columnspan=6, padx=10, pady=10)

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

        print("Commit: Ventas cargadas (ordenadas por total)." if ordenar else "Commit: Ventas cargadas desde BD.")

    def encolar_venta():
        try:
            cid = int(entry_cliente.get().strip())
            sid = int(entry_servicio.get().strip())
            total = float(entry_total.get().strip())
        except:
            messagebox.showerror("Error", "Datos inválidos.")
            print("Commit: Error al encolar venta (datos inválidos).")
            return
        venta = {"cliente_id": cid, "servicio_id": sid, "total": total, "fecha": datetime.now().isoformat()}
        ventas_queue.append(venta)
        print("Commit: Venta encolada (cola FIFO).")
        messagebox.showinfo("Cola", f"Venta en cola. Posición: {len(ventas_queue)}")

    def procesar_venta():
        if not ventas_queue:
            messagebox.showinfo("Cola", "No hay ventas en cola.")
            print("Commit: Intento de procesar cola vacía.")
            return
        v = ventas_queue.popleft()
        conn = conectar(); cur = conn.cursor()
        cur.execute("INSERT INTO ventas (cliente_id, servicio_id, fecha, total) VALUES (?,?,?,?)",
                    (v["cliente_id"], v["servicio_id"], v["fecha"], v["total"]))
        conn.commit(); conn.close()
        print(f"Commit: Venta procesada e insertada en BD (total={v['total']}).")
        cargar_datos()

    def eliminar_venta_bd():
        sel = tabla.selection()
        if not sel:
            messagebox.showwarning("Selecciona", "Selecciona una venta para eliminar.")
            return
        vid = tabla.item(sel)["values"][0]
        conn = conectar(); cur = conn.cursor()
        cur.execute("DELETE FROM ventas WHERE id=?", (vid,))
        conn.commit(); conn.close()
        print(f"Commit: Venta id={vid} eliminada de BD.")
        cargar_datos()

    tk.Button(ventana, text="Encolar venta", command=encolar_venta, bg="#bce0ff").grid(row=4, column=0, padx=6)
    tk.Button(ventana, text="Procesar siguiente venta", command=procesar_venta, bg="#d1f7c4").grid(row=4, column=1,                                                                              padx=6)
    tk.Button(ventana, text="Eliminar venta (BD)", command=eliminar_venta_bd, bg="#ffd6d6").grid(row=4, column=2,                                                                                          padx=6)
    tk.Button(ventana, text="Cargar ventas", command=lambda: cargar_datos(False), bg="#e7e7ff").grid(row=4, column=3,                                                                                                padx=6)
    tk.Button(ventana, text="Ordenar por total", command=lambda: cargar_datos(True), bg="#fff3b0").grid(row=4, column=4,
                                                                                                        padx=6)
    cargar_datos()
    print("Commit: Ventana de Ventas inicializada con cola FIFO y ordenamiento Bubble Sort.")
