# facturar.py
import tkinter as tk
import sqlite_db
import styles
import pagos
import estado

def abrir_facturar(root, parent):
    """Interfaz de facturación combinada: venta rápida o por mesas"""
    parent.pack_forget()
    pantalla = tk.Frame(root, bg=styles.FondoPantalla)
    pantalla.pack(fill="both", expand=True)

    # =====================================================
    # IZQUIERDA 30%: Ticket + Botones
    # =====================================================
    frame_izq = tk.Frame(pantalla, bg=styles.FondoPanel, width=300)
    frame_izq.pack(side="left", fill="y")
    frame_izq.pack_propagate(False)

    tk.Label(frame_izq, text="Ticket", font=styles.FuenteTitulo, bg=styles.FondoPanel).pack(pady=10)
    frame_lineas = tk.Frame(frame_izq, bg=styles.FondoPanel)
    frame_lineas.pack(fill="both", expand=True, padx=5, pady=5)
    lbl_total = tk.Label(frame_izq, text="Total: 0.00 €", font=styles.FuenteNormal, bg=styles.FondoPanel)
    lbl_total.pack(anchor="e", padx=10)

    ticket = {}
    mesa_seleccionada = [None]  # mutable para referencia

    # =====================================================
    # Función refrescar ticket
    # =====================================================
    def refrescar():
        for w in frame_lineas.winfo_children():
            w.destroy()
        total = 0
        for info in ticket.values():
            subtotal = info["cantidad"] * info["precio"]
            total += subtotal
            tk.Label(frame_lineas, text=f'{info["cantidad"]} {info["nombre"]} {subtotal:.2f} €',
                     font=styles.FuentePequena, bg=styles.FondoPanel, bd=1, relief="solid",
                     padx=6, pady=4).pack(side="top", fill="x", pady=1)
        lbl_total.config(text=f"Total: {total:.2f} €")

    # =====================================================
    # Selección de mesa
    # =====================================================
    def seleccionar_mesa():
        mesas = sqlite_db.obtener_mesas()
        if not mesas:
            return
        top = tk.Toplevel(root)
        top.title("Seleccionar mesa")
        top.configure(bg=styles.FondoPantalla)
        w, h = 360, 240
        x = (root.winfo_screenwidth() - w) // 2
        y = (root.winfo_screenheight() - h) // 2
        top.geometry(f"{w}x{h}+{x}+{y}")
        top.resizable(False, False)

        sel = tk.IntVar(value=int(mesa_seleccionada[0]) if mesa_seleccionada[0] else 0)

        for m in mesas:
            tk.Radiobutton(top, text=m[1], variable=sel, value=m[0],
                        font=styles.FuenteNormal, bg=styles.FondoPantalla).pack(anchor="w", padx=20, pady=2)

        def confirmar():
            codigo_mesa = sel.get()
            mesa_seleccionada[0] = codigo_mesa if codigo_mesa != 0 else None

            # cargar ticket temporal de la mesa seleccionada
            temp = estado.obtener_ticket(mesa_seleccionada[0])
            ticket.clear()
            ticket.update(temp)
            refrescar()
            top.destroy()

        tk.Button(top, text="Confirmar", width=16, font=styles.FuenteNormal,
                bg=styles.BotonConfirmarColor, fg=styles.BotonConfirmarFG,
                command=confirmar).pack(pady=10)
    # =====================================================
    # Botones inferiores (izquierda)
    # =====================================================
    frame_botones = tk.Frame(frame_izq, bg=styles.FondoPanel)
    frame_botones.pack(fill="x", pady=5)

    # Grid adaptado para ocupar espacio disponible
    frame_botones.columnconfigure((0, 1), weight=1, uniform="col")
    frame_botones.rowconfigure((0, 1), weight=1, uniform="row")

    tk.Button(frame_botones, text="Seleccionar mesa", font=styles.FuenteNormal,
              bg=styles.BotonNeutroColor, fg=styles.BotonNeutroFG,
              command=seleccionar_mesa).grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    tk.Button(frame_botones, text="Generar ticket", font=styles.FuenteNormal,
              bg=styles.BotonSecundarioColor, fg=styles.BotonSecundarioFG,
              command=lambda: pagos.mostrar_ticket(ticket, mesa_seleccionada[0])
              ).grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

    tk.Button(frame_botones, text="Confirmar venta", font=styles.FuenteNormal,
              bg=styles.BotonConfirmarColor, fg=styles.BotonConfirmarFG,
              command=lambda: pagos.confirmar_venta(root, ticket, mesa=mesa_seleccionada[0], refrescar_ui=refrescar)
              ).grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

    tk.Button(frame_botones, text="Volver", font=styles.FuenteNormal,
              bg=styles.BotonCancelarColor, fg=styles.BotonCancelarFG,
              command=lambda: [ticket.clear(), pantalla.destroy(), parent.pack(fill="both", expand=True)]
              ).grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

    # =====================================================
    # DERECHA 70%: Categorías y artículos
    # =====================================================
    frame_der = tk.Frame(pantalla, bg=styles.FondoPantalla)
    frame_der.pack(side="left", fill="both", expand=True)

    frame_art = tk.Frame(frame_der, bg=styles.FondoPantalla)
    frame_art.pack(fill="both", expand=True, padx=10, pady=10)

    # =====================================================
    # Funciones de navegación
    # =====================================================
    def mostrar_articulos(cat):
        for w in frame_art.winfo_children():
            w.destroy()
        for art in sqlite_db.obtener_articulos_categoria(cat):
            def add(a=art):
                ticket.setdefault(a[0], {"nombre": a[2], "precio": float(a[4]), "cantidad": 0})["cantidad"] += 1
                refrescar()
                if mesa_seleccionada[0]:
                    estado.ticketsTemporalesMesa[mesa_seleccionada[0]] = ticket.copy()
            tk.Button(frame_art, text=f"{art[2]} - {float(art[4]):.2f} €", font=styles.FuenteNormal,
                      bg=styles.BotonSecundarioColor, fg=styles.BotonSecundarioFG,
                      command=add).pack(fill="x", padx=10, pady=4)
        tk.Button(frame_art, text="Atrás", font=styles.FuenteNormal,
                  bg=styles.BotonCancelarColor, fg=styles.BotonCancelarFG,
                  command=mostrar_categorias).pack(pady=10)

    def mostrar_categorias():
        for w in frame_art.winfo_children():
            w.destroy()
        for c in sqlite_db.obtener_categorias():
            tk.Button(frame_art, text=c[1], font=styles.FuenteNormal,
                      bg=styles.BotonNeutroColor, fg=styles.BotonNeutroFG,
                      command=lambda cod=c[0]: mostrar_articulos(cod)).pack(fill="x", padx=20, pady=5)

    mostrar_categorias()
