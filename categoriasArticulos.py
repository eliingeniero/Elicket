# categoriasArticulos.py
import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite_db
import styles
import configuracion

# =======================
# FUNCIONES CATEGORÍAS
# =======================
def abrir_categorias(root, parent_config):
    parent_config.pack_forget()  # oculta la configuración

    pantalla_cat = tk.Frame(root, bg=styles.FondoPantalla)
    pantalla_cat.pack(fill="both", expand=True)

    tk.Label(pantalla_cat, text="Categorías", font=styles.FuenteTitulo, bg=styles.FondoPantalla).pack(pady=15)

    contenedor = tk.Frame(pantalla_cat, bg=styles.FondoPantalla)
    contenedor.pack(fill="both", expand=True, padx=10, pady=5)

    canvas = tk.Canvas(contenedor, bg=styles.FondoPantalla)
    scrollbar = tk.Scrollbar(contenedor, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg=styles.FondoPantalla)

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0,0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def refrescar():
        for w in scroll_frame.winfo_children():
            w.destroy()
        categorias = sqlite_db.obtener_categorias()
        for i, c in enumerate(categorias):
            color_fila = styles.FondoTicket if i % 2 == 0 else styles.FondoPanel
            fila = tk.Frame(scroll_frame, bg=color_fila, bd=1, relief="solid", padx=5, pady=5)
            fila.pack(fill="x", pady=2)

            tk.Label(fila, text=c[0], width=10, anchor="w", bg=color_fila, font=styles.FuenteNormal).pack(side="left", padx=5)
            tk.Label(fila, text=c[1], width=25, anchor="w", bg=color_fila, font=styles.FuenteNormal).pack(side="left", padx=5)
            tk.Label(fila, text=c[2], width=40, anchor="w", bg=color_fila, font=styles.FuenteNormal).pack(side="left", padx=5)

            tk.Button(fila, text="Modificar", font=styles.FuentePequena,
                      bg=styles.BotonFacturasColor, fg=styles.BotonConfirmarFG,
                      command=lambda cat=c: modificar_categoria(cat)).pack(side="left", padx=5)
            tk.Button(fila, text="Eliminar", font=styles.FuentePequena,
                      bg=styles.BotonCancelarColor, fg=styles.BotonCancelarFG,
                      command=lambda cod=c[0]: eliminar_categoria(cod)).pack(side="left", padx=5)

    def eliminar_categoria(codigo):
        if not sqlite_db.eliminar_categoria(codigo):
            messagebox.showwarning("Aviso", "No se puede eliminar, la categoría tiene artículos")
        refrescar()

    def modificar_categoria(cat):
        popup = tk.Toplevel()
        popup.title("Modificar categoría")
        popup.configure(bg=styles.FondoPantalla)

        tk.Label(popup, text="Código (no editable)", bg=styles.FondoPantalla, font=styles.FuenteNormal).pack()
        tk.Entry(popup, state="disabled", disabledforeground="black", justify="left",
                 textvariable=tk.StringVar(value=str(cat[0]))).pack()

        tk.Label(popup, text="Nombre", bg=styles.FondoPantalla, font=styles.FuenteNormal).pack()
        nombre_var = tk.StringVar(value=cat[1])
        tk.Entry(popup, textvariable=nombre_var).pack()

        tk.Label(popup, text="Descripción", bg=styles.FondoPantalla, font=styles.FuenteNormal).pack()
        desc_var = tk.StringVar(value=cat[2])
        tk.Entry(popup, textvariable=desc_var).pack()

        def guardar():
            nombre = nombre_var.get().strip()
            descripcion = desc_var.get().strip()
            if not nombre:
                messagebox.showerror("Error", "El nombre no puede estar vacío")
                return
            exito, msg = sqlite_db.modificar_categoria(cat[0], nombre, descripcion)
            if not exito:
                messagebox.showerror("Error al modificar", msg)
                return
            popup.destroy()
            refrescar()

        tk.Button(popup, text="Guardar", font=styles.FuenteNormal,
                  bg=styles.BotonConfirmarColor, fg=styles.BotonConfirmarFG, command=guardar).pack(side="left", padx=5, pady=5)
        tk.Button(popup, text="Cancelar", font=styles.FuenteNormal,
                  bg=styles.BotonCancelarColor, fg=styles.BotonCancelarFG, command=popup.destroy).pack(side="left", padx=5, pady=5)

    def añadir_categoria():
        popup = tk.Toplevel()
        popup.title("Añadir categoría")
        popup.configure(bg=styles.FondoPantalla)

        tk.Label(popup, text="Código (número entero)", bg=styles.FondoPantalla, font=styles.FuenteNormal).pack()
        codigo_var = tk.StringVar()
        tk.Entry(popup, textvariable=codigo_var).pack()

        tk.Label(popup, text="Nombre", bg=styles.FondoPantalla, font=styles.FuenteNormal).pack()
        nombre_var = tk.StringVar()
        tk.Entry(popup, textvariable=nombre_var).pack()

        tk.Label(popup, text="Descripción", bg=styles.FondoPantalla, font=styles.FuenteNormal).pack()
        desc_var = tk.StringVar()
        tk.Entry(popup, textvariable=desc_var).pack()

        def guardar():
            codigo = codigo_var.get().strip()
            nombre = nombre_var.get().strip()
            descripcion = desc_var.get().strip()
            if not codigo or not nombre:
                messagebox.showerror("Error", "Código y Nombre son obligatorios")
                return
            try:
                codigo_int = int(codigo)
            except ValueError:
                messagebox.showerror("Error", "El código debe ser un número entero")
                return
            exito, msg = sqlite_db.agregar_categoria(codigo_int, nombre, descripcion)
            if not exito:
                messagebox.showerror("Error al añadir categoría", msg)
                return
            popup.destroy()
            refrescar()

        tk.Button(popup, text="Guardar", font=styles.FuenteNormal,
                  bg=styles.BotonConfirmarColor, fg=styles.BotonConfirmarFG, command=guardar).pack(side="left", padx=5, pady=5)
        tk.Button(popup, text="Cancelar", font=styles.FuenteNormal,
                  bg=styles.BotonCancelarColor, fg=styles.BotonCancelarFG, command=popup.destroy).pack(side="left", padx=5, pady=5)

    tk.Button(pantalla_cat, text="Añadir categoría", font=styles.FuenteNormal,
              bg=styles.BotonNeutroColor, fg=styles.BotonNeutroFG, command=añadir_categoria).pack(pady=10)

    tk.Button(pantalla_cat, text="Atrás", font=styles.FuenteNormal,
              bg=styles.BotonCancelarColor, fg=styles.BotonCancelarFG,
              command=lambda: [pantalla_cat.pack_forget(), parent_config.pack()]).pack(pady=10)

    refrescar()


# =======================
# FUNCIONES ARTÍCULOS
# =======================
def abrir_articulos(root, parent_config):
    parent_config.pack_forget()  # oculta la configuración

    pantalla_art = tk.Frame(root, bg=styles.FondoPantalla)
    pantalla_art.pack(fill="both", expand=True)

    tk.Label(pantalla_art, text="Gestión de Artículos", font=styles.FuenteTitulo, bg=styles.FondoPantalla).pack(pady=15)

    contenedor = tk.Frame(pantalla_art, bg=styles.FondoPantalla)
    contenedor.pack(fill="both", expand=True, padx=10, pady=5)

    canvas = tk.Canvas(contenedor, bg=styles.FondoPantalla)
    scrollbar_v = tk.Scrollbar(contenedor, orient="vertical", command=canvas.yview)
    scrollbar_h = tk.Scrollbar(contenedor, orient="horizontal", command=canvas.xview)
    canvas.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)

    scroll_frame = tk.Frame(canvas, bg=styles.FondoPantalla)
    canvas.create_window((0,0), window=scroll_frame, anchor="nw")

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    canvas.grid(row=0, column=0, sticky="nsew")
    scrollbar_v.grid(row=0, column=1, sticky="ns")
    scrollbar_h.grid(row=1, column=0, sticky="ew")
    contenedor.grid_rowconfigure(0, weight=1)
    contenedor.grid_columnconfigure(0, weight=1)

    def refrescar_articulos(orden="codigo"):
        for w in scroll_frame.winfo_children():
            w.destroy()

        header = tk.Frame(scroll_frame, bg=styles.FondoPantalla)
        header.pack(fill="x", pady=2)
        tk.Button(header, text="Código", width=15, font=styles.FuentePequena, command=lambda: refrescar_articulos("codigo")).pack(side="left")
        tk.Button(header, text="Categoría", width=20, font=styles.FuentePequena, command=lambda: refrescar_articulos("categoria")).pack(side="left")
        tk.Button(header, text="Nombre", width=20, font=styles.FuentePequena, command=lambda: refrescar_articulos("nombre")).pack(side="left")
        tk.Label(header, text="Descripción", width=40, anchor="w", bg=styles.FondoPantalla, font=styles.FuentePequena).pack(side="left")
        tk.Label(header, text="Precio", width=10, anchor="e", bg=styles.FondoPantalla, font=styles.FuentePequena).pack(side="left")
        tk.Label(header, text="Acciones", width=20, bg=styles.FondoPantalla, font=styles.FuentePequena).pack(side="left")

        articulos = sqlite_db.obtener_articulos()
        if orden == "codigo":
            articulos.sort(key=lambda x: x[0])
        elif orden == "categoria":
            articulos.sort(key=lambda x: x[1])
        elif orden == "nombre":
            articulos.sort(key=lambda x: x[2])

        for i, a in enumerate(articulos):
            color_fila = styles.FondoTicket if i % 2 == 0 else styles.FondoPanel
            fila = tk.Frame(scroll_frame, bg=color_fila, bd=1, relief="solid", padx=5, pady=5)
            fila.pack(fill="x", pady=1)

            tk.Label(fila, text=a[0], width=15, anchor="w", bg=color_fila, font=styles.FuenteNormal).pack(side="left")
            tk.Label(fila, text=a[1], width=20, anchor="w", bg=color_fila, font=styles.FuenteNormal).pack(side="left")
            tk.Label(fila, text=a[2], width=20, anchor="w", bg=color_fila, font=styles.FuenteNormal).pack(side="left")
            tk.Label(fila, text=a[3], width=40, anchor="w", bg=color_fila, font=styles.FuenteNormal).pack(side="left")
            tk.Label(fila, text=f"{a[4]:.2f}", width=10, anchor="e", bg=color_fila, font=styles.FuenteNormal).pack(side="left")

            def modificar_art(art=a):
                new_nombre = simpledialog.askstring("Modificar", "Nombre:", initialvalue=art[2], parent=root)
                new_desc = simpledialog.askstring("Modificar", "Descripción:", initialvalue=art[3], parent=root)
                new_precio = simpledialog.askstring("Modificar", "Precio:", initialvalue=str(art[4]), parent=root)
                if new_nombre is None or new_precio is None:
                    return
                try:
                    new_precio_f = float(new_precio)
                except ValueError:
                    messagebox.showerror("Error", "Precio debe ser un número")
                    return
                sqlite_db.eliminar_articulo(art[0])
                sqlite_db.agregar_articulo(art[0], art[1], new_nombre, new_desc or "", new_precio_f)
                refrescar_articulos(orden)

            tk.Button(fila, text="Modificar", width=10, bg=styles.BotonFacturasColor,
                      fg=styles.BotonConfirmarFG, font=styles.FuentePequena, command=modificar_art).pack(side="left", padx=2)

            def eliminar_art(art=a):
                if messagebox.askyesno("Eliminar", f"Eliminar artículo {art[2]}?"):
                    sqlite_db.eliminar_articulo(art[0])
                    refrescar_articulos(orden)

            tk.Button(fila, text="Eliminar", width=10, bg=styles.BotonCancelarColor,
                      fg=styles.BotonCancelarFG, font=styles.FuentePequena, command=eliminar_art).pack(side="left", padx=2)

    def añadir_articulo():
        popup = tk.Toplevel()
        popup.title("Añadir Artículo")
        popup.configure(bg=styles.FondoPantalla)

        tk.Label(popup, text="Código (número entero)", bg=styles.FondoPantalla, font=styles.FuenteNormal).pack()
        codigo_var = tk.StringVar()
        tk.Entry(popup, textvariable=codigo_var).pack()

        tk.Label(popup, text="Categoría", bg=styles.FondoPantalla, font=styles.FuenteNormal).pack()
        categorias = sqlite_db.obtener_categorias()
        if not categorias:
            messagebox.showerror("Error", "No hay categorías")
            popup.destroy()
            return

        nombres = [c[1] for c in categorias]
        codigos = {c[1]: c[0] for c in categorias}
        categoria_var = tk.StringVar(value=nombres[0])
        tk.OptionMenu(popup, categoria_var, *nombres).pack()

        tk.Label(popup, text="Nombre", bg=styles.FondoPantalla, font=styles.FuenteNormal).pack()
        nombre_var = tk.StringVar()
        tk.Entry(popup, textvariable=nombre_var).pack()

        tk.Label(popup, text="Descripción", bg=styles.FondoPantalla, font=styles.FuenteNormal).pack()
        desc_var = tk.StringVar()
        tk.Entry(popup, textvariable=desc_var).pack()

        tk.Label(popup, text="Precio", bg=styles.FondoPantalla, font=styles.FuenteNormal).pack()
        precio_var = tk.StringVar()
        tk.Entry(popup, textvariable=precio_var).pack()

        def guardar():
            codigo = codigo_var.get().strip()
            categoria_nombre = categoria_var.get()
            categoria_codigo = codigos[categoria_nombre]
            nombre = nombre_var.get().strip()
            descripcion = desc_var.get().strip()
            precio_texto = precio_var.get().strip()
            if not codigo or not nombre:
                messagebox.showerror("Error", "Código y Nombre son obligatorios")
                return
            try:
                codigo_int = int(codigo)
            except ValueError:
                messagebox.showerror("Error", "Código debe ser un número entero")
                return
            try:
                precio_f = float(precio_texto)
            except ValueError:
                messagebox.showerror("Error", "Precio debe ser un número")
                return
            exist = [a[0] for a in sqlite_db.obtener_articulos()]
            if codigo_int in exist:
                messagebox.showerror("Error", "Código de artículo ya existe")
                return
            exito, msg = sqlite_db.agregar_articulo(codigo_int, categoria_codigo, nombre, descripcion, precio_f)
            if not exito:
                messagebox.showerror("Error al añadir artículo", msg)
                return
            popup.destroy()
            refrescar_articulos()

        tk.Button(popup, text="Guardar", font=styles.FuenteNormal,
                  bg=styles.BotonConfirmarColor, fg=styles.BotonConfirmarFG, command=guardar).pack(side="left", padx=5, pady=5)
        tk.Button(popup, text="Cancelar", font=styles.FuenteNormal,
                  bg=styles.BotonCancelarColor, fg=styles.BotonCancelarFG, command=popup.destroy).pack(side="left", padx=5, pady=5)

    tk.Button(pantalla_art, text="Añadir Artículo", font=styles.FuenteNormal,
              bg=styles.BotonNeutroColor, fg=styles.BotonNeutroFG, command=añadir_articulo).pack(pady=10)
    tk.Button(pantalla_art, text="Atrás", font=styles.FuenteNormal,
                bg=styles.BotonCancelarColor, fg=styles.BotonCancelarFG,
                command=lambda: [pantalla_art.pack_forget(), parent_config.pack()]).pack

    refrescar_articulos()
