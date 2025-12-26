# facturar_rapida.py
import tkinter as tk
import sqlite_db
import styles
import facturar
import imprimir

def abrir_venta_rapida(root, parent):
    parent.pack_forget()
    pantalla = tk.Frame(root, bg=styles.FondoPantalla)
    pantalla.pack(fill="both", expand=True)

    tk.Label(pantalla, text="Venta rápida", font=styles.FuenteTitulo, bg=styles.FondoPantalla).pack(pady=10)

    frame_art = tk.Frame(pantalla, bg=styles.FondoPantalla)
    frame_art.pack(fill="both", expand=True)

    frame_ticket = tk.Frame(pantalla, bg=styles.FondoPanel, bd=2, relief="groove")
    frame_ticket.pack(fill="x", pady=10)

    frame_lineas = tk.Frame(frame_ticket, bg=styles.FondoPanel)
    frame_lineas.pack(fill="x", padx=5, pady=5)

    lbl_total = tk.Label(frame_ticket, text="Total: 0.00 €", font=styles.FuenteNormal, bg=styles.FondoPanel)
    lbl_total.pack(anchor="e", padx=10)

    ticket = {}

    def refrescar():
        for w in frame_lineas.winfo_children():
            w.destroy()
        total = 0
        for info in ticket.values():
            subtotal = info["cantidad"] * info["precio"]
            total += subtotal
            tk.Label(frame_lineas, text=f'{info["cantidad"]} {info["nombre"]} {subtotal:.2f} €',
                     font=styles.FuentePequena, bg=styles.FondoPanel, bd=1, relief="solid",
                     padx=6, pady=4).pack(side="left", padx=4)
        lbl_total.config(text=f"Total: {total:.2f} €")

    def mostrar_articulos(cat):
        for w in frame_art.winfo_children():
            w.destroy()
        for art in sqlite_db.obtener_articulos_categoria(cat):
            def add(a=art):
                ticket.setdefault(a[0], {"nombre": a[2], "precio": float(a[4]), "cantidad": 0})["cantidad"] += 1
                refrescar()
            tk.Button(frame_art, text=f"{art[2]} - {float(art[4]):.2f} €", font=styles.FuenteNormal,
                      bg=styles.BotonSecundarioColor, fg=styles.BotonSecundarioFG, command=add).pack(fill="x", padx=40, pady=4)
        tk.Button(frame_art, text="Atrás", font=styles.FuenteNormal,
                  bg=styles.BotonCancelarColor, fg=styles.BotonCancelarFG,
                  command=mostrar_categorias).pack(pady=10)

    def mostrar_categorias():
        for w in frame_art.winfo_children():
            w.destroy()
        for c in sqlite_db.obtener_categorias():
            tk.Button(frame_art, text=c[1], font=styles.FuenteNormal,
                      bg=styles.BotonNeutroColor, fg=styles.BotonNeutroFG,
                      command=lambda cod=c[0]: mostrar_articulos(cod)).pack(fill="x", padx=60, pady=5)

    mostrar_categorias()

    # =========================
    # Botones de control
    # =========================
    tk.Button(frame_ticket, text="Generar ticket", width=16, font=styles.FuenteNormal,
            bg=styles.BotonSecundarioColor, fg=styles.BotonSecundarioFG,
            command=lambda: facturar.generar_ticket_ui(root, ticket, mesa=None)
            ).pack(side="left", padx=5, pady=5)
   
    tk.Button(frame_ticket, text="Confirmar venta", width=16, font=styles.FuenteNormal,
              bg=styles.BotonConfirmarColor, fg=styles.BotonConfirmarFG,
              command=lambda: facturar.confirmar_venta(root, ticket, mesa=None, refrescar_ui=refrescar)
              ).pack(side="left", padx=5, pady=5)

    tk.Button(frame_ticket, text="Atrás", width=16, font=styles.FuenteNormal,
              bg=styles.BotonCancelarColor, fg=styles.BotonCancelarFG,
              command=lambda: [ticket.clear(), pantalla.destroy(), parent.pack(fill="both", expand=True)]
              ).pack(side="right", padx=5, pady=5)
