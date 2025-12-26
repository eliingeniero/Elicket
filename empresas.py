import tkinter as tk
from tkinter import messagebox
import sqlite_db
import styles

def abrir_empresas(root, parent=None):
    pantalla_emp = tk.Frame(root, bg=styles.FondoPantalla)
    pantalla_emp.pack(fill="both", expand=True)

    tk.Label(pantalla_emp, text="Gestión de Empresas", font=styles.FuenteTitulo, bg=styles.FondoPantalla).pack(pady=10)

    contenedor = tk.Frame(pantalla_emp, bg=styles.FondoPantalla)
    contenedor.pack(fill="both", expand=True)

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

    def refrescar():
        for w in scroll_frame.winfo_children():
            w.destroy()

        empresas_list = sqlite_db.obtener_empresas()
        header = tk.Frame(scroll_frame, bg=styles.FondoPantalla)
        header.pack(fill="x", pady=2)
        tk.Label(header, text="ID", width=5, anchor="w", bg=styles.FondoPantalla).pack(side="left", padx=5)
        tk.Label(header, text="Nombre", width=25, anchor="w", bg=styles.FondoPantalla).pack(side="left", padx=5)
        tk.Label(header, text="CIF", width=20, anchor="w", bg=styles.FondoPantalla).pack(side="left", padx=5)
        tk.Label(header, text="Dirección", width=40, anchor="w", bg=styles.FondoPantalla).pack(side="left", padx=5)
        tk.Label(header, text="Acciones", width=20, bg=styles.FondoPantalla).pack(side="left", padx=5)

        for emp in empresas_list:
            fila = tk.Frame(scroll_frame, bg=styles.FondoTicket if empresas_list.index(emp)%2==0 else styles.FondoPanel)
            fila.pack(fill="x", pady=1)
            
            tk.Label(fila, text=emp[0], width=5, anchor="w", bg=fila["bg"]).pack(side="left", padx=5)
            tk.Label(fila, text=emp[1], width=25, anchor="w", bg=fila["bg"]).pack(side="left", padx=5)
            tk.Label(fila, text=emp[2], width=20, anchor="w", bg=fila["bg"]).pack(side="left", padx=5)
            tk.Label(fila, text=emp[3], width=40, anchor="w", bg=fila["bg"]).pack(side="left", padx=5)

            def modificar_empresa(emp=emp):
                ventana_empresa(emp, refrescar)

            tk.Button(fila, text="Modificar", command=modificar_empresa, width=10).pack(side="left", padx=2)

            def eliminar_emp(id=emp[0]):
                if messagebox.askyesno("Eliminar", f"Eliminar empresa {emp[1]}?"):
                    if not sqlite_db.eliminar_empresa(id):
                        messagebox.showerror("Error", "No se pudo eliminar la empresa")
                    refrescar()

            tk.Button(fila, text="Eliminar", command=eliminar_emp, width=10).pack(side="left", padx=2)

    def ventana_empresa(emp=None, refrescar_cb=None):
        popup = tk.Toplevel(root)
        popup.title("Modificar Empresa" if emp else "Añadir Empresa")
        popup.configure(bg=styles.FondoPantalla)

        tk.Label(popup, text="Nombre", bg=styles.FondoPantalla).pack()
        nombre_var = tk.StringVar(value=emp[1] if emp else "")
        tk.Entry(popup, textvariable=nombre_var).pack()

        tk.Label(popup, text="CIF", bg=styles.FondoPantalla).pack()
        cif_var = tk.StringVar(value=emp[2] if emp else "")
        tk.Entry(popup, textvariable=cif_var).pack()

        tk.Label(popup, text="Dirección", bg=styles.FondoPantalla).pack()
        dir_var = tk.StringVar(value=emp[3] if emp else "")
        tk.Entry(popup, textvariable=dir_var).pack()

        def guardar():
            nombre = nombre_var.get().strip()
            cif = cif_var.get().strip()
            direccion = dir_var.get().strip()
            if not nombre:
                messagebox.showerror("Error", "El nombre no puede estar vacío")
                return
            if emp:
                exito, msg = sqlite_db.modificar_empresa(emp[0], nombre, cif, direccion)
            else:
                exito, msg = sqlite_db.agregar_empresa(nombre, cif, direccion)
            if not exito:
                messagebox.showerror("Error", msg)
                return
            popup.destroy()
            if refrescar_cb:
                refrescar_cb()

        tk.Button(popup, text="Guardar", command=guardar).pack(side="left", padx=5, pady=5)
        tk.Button(popup, text="Cancelar", command=popup.destroy).pack(side="left", padx=5, pady=5)

    tk.Button(pantalla_emp, text="Añadir Empresa", width=20, command=lambda: ventana_empresa(refrescar_cb=refrescar)).pack(pady=5)
    tk.Button(pantalla_emp, text="Atrás", width=10,
              command=lambda: [pantalla_emp.pack_forget(), parent.pack() if parent else None]).pack(pady=5)

    refrescar()
