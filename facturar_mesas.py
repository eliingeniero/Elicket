# facturar_mesas.py
import tkinter as tk
import sqlite_db
import styles
import facturar
import imprimir

def abrir_facturar_mesas(root, parent):
    parent.pack_forget()
    pantalla = tk.Frame(root, bg=styles.FondoPantalla)
    pantalla.pack(fill="both", expand=True)

    tk.Label(pantalla, text="Venta por mesas", font=styles.FuenteTitulo, bg=styles.FondoPantalla).pack(pady=10)

    frame_mesas = tk.Frame(pantalla, bg=styles.FondoPantalla)
    frame_mesas.pack(fill="both", expand=True)

    frame_ticket = tk.Frame(pantalla, bg=styles.FondoPanel, bd=2, relief="groove")
    frame_ticket.pack(fill="x", pady=10)

    frame_lineas = tk.Frame(frame_ticket, bg=styles.FondoPanel)
    frame_lineas.pack(fill="x", padx=5, pady=5)

    lbl_total = tk.Label(frame_ticket, text="Total: 0.00 €", font=styles.FuenteNormal, bg=styles.FondoPanel)
    lbl_total.pack(anchor="e", padx=10)

    ticket = {}
    mesa_seleccionada = tk.StringVar(value="")

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

    # Selección de mesa
    for m in sqlite_db.obtener_mesas():
        tk.Radiobutton(frame_mesas, text=m[1], variable=mesa_seleccionada, value=m[0],
                       font=styles.FuenteNormal, bg=styles.FondoPantalla).pack(anchor="w", padx=20)

    # Funciones de botones
    tk.Button(frame_ticket, text="Generar ticket", width=16, font=styles.FuenteNormal,
            bg=styles.BotonSecundarioColor, fg=styles.BotonSecundarioFG,
            command=lambda: facturar.generar_ticket_ui(root, ticket, mesa=mesa_seleccionada.get())
            ).pack(side="left", padx=5, pady=5)
    tk.Button(frame_ticket, text="Confirmar venta", width=16, font=styles.FuenteNormal,
              bg=styles.BotonConfirmarColor, fg=styles.BotonConfirmarFG,
              command=lambda: facturar.confirmar_venta(root, ticket, mesa=mesa_seleccionada.get(), refrescar_ui=refrescar)
              ).pack(side="left", padx=5, pady=5)

    tk.Button(frame_ticket, text="Atrás", width=16, font=styles.FuenteNormal,
              bg=styles.BotonCancelarColor, fg=styles.BotonCancelarFG,
              command=lambda: [ticket.clear(), pantalla.destroy(), parent.pack(fill="both", expand=True)]
              ).pack(side="right", padx=5, pady=5)
