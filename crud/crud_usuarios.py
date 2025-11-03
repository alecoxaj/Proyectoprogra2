import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

DB_PATH = "espacio_creativo.db"

def conectar():
    return sqlite3.connect(DB_PATH)

def ventana_usuarios():
    ventana = tk.Toplevel()
    ventana.title("Gestión de Usuarios - Espacio Creativo")
    ventana.geometry("620x420")
    ventana.config(bg="#f8fafc")

    tk.Label(ventana, text="Nombre:").grid(row=0, column=0, padx=6, pady=6, sticky="e")
    entry_nombre = tk.Entry(ventana, width=30); entry_nombre.grid(row=0, column=1)

    tk.Label(ventana, text="Usuario:").grid(row=1, column=0, padx=6, pady=6, sticky="e")
    entry_usuario = tk.Entry(ventana, width=30); entry_usuario.grid(row=1, column=1)

    tk.Label(ventana, text="Contraseña:").grid(row=2, column=0, padx=6, pady=6, sticky="e")
    entry_contr = tk.Entry(ventana, width=30, show="*"); entry_contr.grid(row=2, column=1)

    tk.Label(ventana, text="Rol (admin/usuario):").grid(row=3, column=0, padx=6, pady=6, sticky="e")
    entry_rol = tk.Entry(ventana, width=30); entry_rol.grid(row=3, column=1)

    cols = ("id", "nombre", "usuario", "rol")
    tabla = ttk.Treeview(ventana, columns=cols, show="headings", height=10)
    for c in cols: tabla.heading(c, text=c.capitalize())
    tabla.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

    usuarios_cache = []
    usuarios_hash = {}


    def cargar_datos():
        tabla.delete(*tabla.get_children())
        usuarios_cache.clear()
        usuarios_hash.clear()
        conn = conectar(); cur = conn.cursor()
        cur.execute("SELECT id, nombre, usuario, rol FROM usuarios")
        filas = cur.fetchall()
        for f in filas:
            tabla.insert("", tk.END, values=f)
            usuarios_cache.append(f)
            usuarios_hash[f[2]] = f
        conn.close()
        print("Commit: Usuarios cargados en tabla, cache y hash.")

    def agregar_usuario():
        n = entry_nombre.get().strip()
        u = entry_usuario.get().strip()
        p = entry_contr.get().strip()
        r = entry_rol.get().strip() or "usuario"
        if not (n and u and p):
            messagebox.showwarning("Datos", "Llena nombre, usuario y contraseña.")
            print("Commit: Intento de agregar usuario sin datos completos.")
            return
        conn = conectar(); cur = conn.cursor()
        try:
            cur.execute("INSERT INTO usuarios (nombre, usuario, contraseña, rol) VALUES (?,?,?,?)",
                        (n, u, p, r))
            conn.commit()
            messagebox.showinfo("Éxito", "Usuario agregado.")
            print(f"Commit: Usuario '{u}' agregado.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "El nombre de usuario ya existe.")
            print(f"Commit: Error al agregar usuario '{u}' (ya existe).")
        finally:
            conn.close()
        cargar_datos()

    def eliminar_usuario():
        sel = tabla.selection()
        if not sel:
            messagebox.showwarning("Selecciona", "Selecciona un usuario para eliminar.")
            return
        user_id = tabla.item(sel)["values"][0]
        conn = conectar(); cur = conn.cursor()
        cur.execute("DELETE FROM usuarios WHERE id=?", (user_id,))
        conn.commit(); conn.close()
        print(f"Commit: Usuario id={user_id} eliminado.")
        cargar_datos()

    def actualizar_usuario():
        sel = tabla.selection()
        if not sel:
            messagebox.showwarning("Selecciona", "Selecciona un usuario para actualizar.")
            return
        uid = tabla.item(sel)["values"][0]
        n = entry_nombre.get().strip(); u = entry_usuario.get().strip()
        p = entry_contr.get().strip(); r = entry_rol.get().strip() or "usuario"
        conn = conectar(); cur = conn.cursor()
        cur.execute("UPDATE usuarios SET nombre=?, usuario=?, contraseña=?, rol=? WHERE id=?",
                    (n, u, p, r, uid))
        conn.commit(); conn.close()
        print(f"Commit: Usuario id={uid} actualizado.")
        cargar_datos()

    def busqueda_secuencial():
        key = entry_nombre.get().strip().lower()
        for u in usuarios_cache:
            if u[1].lower() == key:
                messagebox.showinfo("Encontrado", f"Usuario: {u}")
                print(f"Commit: búsqueda secuencial encontró {key}.")
                return
        messagebox.showinfo("No encontrado", "No se encontró el usuario.")
        print(f"Commit: búsqueda secuencial no encontró {key}.")

    def buscar_por_hash():
        key = entry_usuario.get().strip()
        res = usuarios_hash.get(key)
        if res:
            messagebox.showinfo("Encontrado (hash)", f"Usuario: {res}")
            print(f"Commit: búsqueda por hash encontró {key}.")
        else:
            messagebox.showinfo("No encontrado", "No se encontró el usuario (hash).")
            print(f"Commit: búsqueda por hash no encontró {key}.")

    def seleccionar(event):
        sel = tabla.selection()
        if not sel: return
        r = tabla.item(sel)["values"]
        entry_nombre.delete(0, tk.END); entry_nombre.insert(0, r[1])
        entry_usuario.delete(0, tk.END); entry_usuario.insert(0, r[2])
        entry_rol.delete(0, tk.END); entry_rol.insert(0, r[3])

    tabla.bind("<<TreeviewSelect>>", seleccionar)

    tk.Button(ventana, text="Agregar", command=agregar_usuario, bg="#b8f2e6").grid(row=4, column=0, padx=6, pady=6)
    tk.Button(ventana, text="Actualizar", command=actualizar_usuario, bg="#fff3b0").grid(row=4, column=1, padx=6, pady=6)
    tk.Button(ventana, text="Eliminar", command=eliminar_usuario, bg="#ffd6d6").grid(row=4, column=2, padx=6, pady=6)
    tk.Button(ventana, text="Cargar", command=cargar_datos, bg="#dbeafe").grid(row=4, column=3, padx=6, pady=6)

    tk.Button(ventana, text="Buscar (secuencial por nombre)", command=busqueda_secuencial).grid(row=2, column=2, padx=6)
    tk.Button(ventana, text="Buscar (hash por usuario)", command=buscar_por_hash).grid(row=3, column=2, padx=6)

    cargar_datos()
    print("Commit: Ventana de gestión de usuarios inicializada.")
