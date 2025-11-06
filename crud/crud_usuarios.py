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
COLOR_BOTON_CARGAR = "#DBEAFE"
COLOR_TEXTO_OSCURO = "#333333"

def conectar():
    return sqlite3.connect(DB_PATH)

def bubble_sort_usuarios(lista):
    n = len(lista)
    for i in range(n):
        for j in range(0, n - i - 1):
            if lista[j][1].lower() > lista[j + 1][1].lower():
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
    return lista

def ventana_usuarios():
    ventana = tk.Toplevel()
    ventana.title("Gestión de Usuarios - Espacio Creativo")
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

    tk.Label(frame_superior, text="GESTIÓN DE USUARIOS",
             font=font_titulo, bg=COLOR_FONDO_VENTANA,
             fg=COLOR_TEXTO_OSCURO).pack(pady=5)

    def cerrar_usuarios():
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
            command=cerrar_usuarios
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
            command=cerrar_usuarios
        ).place(relx=0.97, rely=0.05, anchor="ne")

    frame_form = tk.Frame(ventana, bg=COLOR_FONDO_FRAME, padx=20, pady=20)
    frame_form.pack(pady=15, padx=40, fill="x")

    tk.Label(frame_form, text="Nombre:", bg=COLOR_FONDO_FRAME, font=font_label, fg=COLOR_TEXTO_OSCURO).grid(row=0, column=0, sticky="e", pady=6, padx=8)
    entry_nombre = tk.Entry(frame_form, width=25)
    entry_nombre.grid(row=0, column=1, pady=6, padx=8)

    tk.Label(frame_form, text="Usuario:", bg=COLOR_FONDO_FRAME, font=font_label, fg=COLOR_TEXTO_OSCURO).grid(row=1, column=0, sticky="e", pady=6, padx=8)
    entry_usuario = tk.Entry(frame_form, width=25)
    entry_usuario.grid(row=1, column=1, pady=6, padx=8)

    tk.Label(frame_form, text="Contraseña:", bg=COLOR_FONDO_FRAME, font=font_label, fg=COLOR_TEXTO_OSCURO).grid(row=2, column=0, sticky="e", pady=6, padx=8)
    entry_contr = tk.Entry(frame_form, width=25, show="*")
    entry_contr.grid(row=2, column=1, pady=6, padx=8)

    tk.Label(frame_form, text="Rol (admin/usuario):", bg=COLOR_FONDO_FRAME, font=font_label, fg=COLOR_TEXTO_OSCURO).grid(row=3, column=0, sticky="e", pady=6, padx=8)
    entry_rol = tk.Entry(frame_form, width=25)
    entry_rol.grid(row=3, column=1, pady=6, padx=8)

    frame_botones = tk.Frame(ventana, bg=COLOR_FONDO_VENTANA)
    frame_botones.pack(pady=(25, 35), padx=50, anchor="w")

    estilo_boton = {
        "font": font_boton,
        "width": 14,
        "pady": 5,
        "relief": "flat",
        "cursor": "hand2"
    }

    tk.Button(frame_botones, text="Agregar", bg=COLOR_BOTON_AGREGAR, fg=COLOR_TEXTO_OSCURO, command=lambda: agregar_usuario(), **estilo_boton).pack(side="left", padx=15)
    tk.Button(frame_botones, text="Actualizar", bg=COLOR_BOTON_ACTUALIZAR, fg=COLOR_TEXTO_OSCURO, command=lambda: actualizar_usuario(), **estilo_boton).pack(side="left", padx=15)
    tk.Button(frame_botones, text="Eliminar", bg=COLOR_BOTON_ELIMINAR, fg=COLOR_TEXTO_OSCURO, command=lambda: eliminar_usuario(), **estilo_boton).pack(side="left", padx=15)
    tk.Button(frame_botones, text="Cargar", bg=COLOR_BOTON_CARGAR, fg=COLOR_TEXTO_OSCURO, command=lambda: cargar_datos(), **estilo_boton).pack(side="left", padx=15)

    frame_busqueda = tk.Frame(ventana, bg=COLOR_FONDO_VENTANA)
    frame_busqueda.pack(pady=(0, 15), padx=50, anchor="w")

    tk.Label(frame_busqueda, text="Buscar por nombre:", bg=COLOR_FONDO_VENTANA, font=font_label, fg=COLOR_TEXTO_OSCURO).grid(row=0, column=0, sticky="e", padx=(0, 10))
    entry_buscar_nombre = tk.Entry(frame_busqueda, width=20)
    entry_buscar_nombre.grid(row=0, column=1, padx=(0, 10))
    tk.Button(frame_busqueda, text="Buscar (secuencial)", bg=COLOR_BOTON_BUSCAR, fg=COLOR_TEXTO_OSCURO, font=font_boton, relief="flat", cursor="hand2", command=lambda: busqueda_secuencial(entry_buscar_nombre.get())).grid(row=0, column=2, padx=(0, 20))

    tk.Label(frame_busqueda, text="Buscar por usuario:", bg=COLOR_FONDO_VENTANA, font=font_label, fg=COLOR_TEXTO_OSCURO).grid(row=1, column=0, sticky="e", padx=(0, 10))
    entry_buscar_usuario = tk.Entry(frame_busqueda, width=20)
    entry_buscar_usuario.grid(row=1, column=1, padx=(0, 10))
    tk.Button(frame_busqueda, text="Buscar (hash)", bg=COLOR_BOTON_BUSCAR, fg=COLOR_TEXTO_OSCURO, font=font_boton, relief="flat", cursor="hand2", command=lambda: buscar_por_hash(entry_buscar_usuario.get())).grid(row=1, column=2)

    cols = ("id", "nombre", "usuario", "rol")
    tabla = ttk.Treeview(ventana, columns=cols, show="headings", height=14)
    for c in cols:
        tabla.heading(c, text=c.capitalize())
        tabla.column(c, anchor="center")
    tabla.pack(fill="both", expand=True, pady=(10, 25), padx=30)

    usuarios_cache = []
    usuarios_hash = {}

    def cargar_datos():
        tabla.delete(*tabla.get_children())
        usuarios_cache.clear()
        usuarios_hash.clear()
        conn = conectar(); cur = conn.cursor()
        cur.execute("SELECT id, nombre, usuario, rol FROM usuarios")
        filas = cur.fetchall()
        conn.close()

        filas_ordenadas = bubble_sort_usuarios(filas)

        for f in filas_ordenadas:
            tabla.insert("", tk.END, values=f)
            usuarios_cache.append(f)
            usuarios_hash[f[2]] = f
        print("Commit: Usuarios cargados en tabla, ordenados por Bubble Sort y almacenados en cache/hash.")

    def agregar_usuario():
        n = entry_nombre.get().strip()
        u = entry_usuario.get().strip()
        p = entry_contr.get().strip()
        r = entry_rol.get().strip() or "usuario"
        if not (n and u and p):
            messagebox.showwarning("Datos", "Llena nombre, usuario y contraseña.")
            print("Commit: Intento de agregar usuario sin datos completos.")
            return
        conn = conectar();
        cur = conn.cursor()
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
        if messagebox.askyesno("Confirmar", "¿Deseas eliminar este registro?"):
            conn = conectar(); cur = conn.cursor()
            cur.execute("DELETE FROM usuarios WHERE id=?", (user_id,))
            conn.commit(); conn.close()
            messagebox.showinfo("Eliminado", "Usuario eliminado correctamente.")
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
        messagebox.showinfo("Actualización", "Usuario actualizado correctamente.")
        print(f"Commit: Usuario id={uid} actualizado.")
        cargar_datos()

    def busqueda_secuencial(nombre):
        key = nombre.strip().lower()
        for item in tabla.get_children():
            tabla.selection_remove(item)

        for item in tabla.get_children():
            valores = tabla.item(item, "values")
            if valores and valores[1].lower() == key:
                tabla.selection_set(item)
                tabla.focus(item)
                tabla.see(item)
                print(f"Commit: búsqueda secuencial encontró {key}.")
                return
        messagebox.showinfo("No encontrado", "No se encontró el usuario.")
        print(f"Commit: búsqueda secuencial no encontró {key}.")

    def buscar_por_hash(usuario):
        key = usuario.strip()
        res = usuarios_hash.get(key)
        for item in tabla.get_children():
            tabla.selection_remove(item)

        if res:
            for item in tabla.get_children():
                valores = tabla.item(item, "values")
                if valores and valores[2] == key:
                    tabla.selection_set(item)
                    tabla.focus(item)
                    tabla.see(item)
                    break
            print(f"Commit: búsqueda por hash encontró {key}.")
        else:
            messagebox.showinfo("No encontrado", "No se encontró el usuario (hash).")
            print(f"Commit: búsqueda por hash no encontró {key}.")

    def seleccionar(event):
        sel = tabla.selection()
        if not sel: return
        r = tabla.item(sel)["values"]
        entry_nombre.delete(0, tk.END)
        entry_nombre.insert(0, r[1])
        entry_usuario.delete(0, tk.END)
        entry_usuario.insert(0, r[2])
        entry_rol.delete(0, tk.END)
        entry_rol.insert(0, r[3])

    tabla.bind("<<TreeviewSelect>>", seleccionar)

    cargar_datos()
    print("Commit: Ventana de gestión de usuarios inicializada con estilo unificado y maximizada.")