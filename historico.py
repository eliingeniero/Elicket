# historico.py
import tkinter as tk
from tkinter import scrolledtext
import sqlite_db
import imprimir
import styles


def abrir_historico(root, parent):
    parent.pack_forget()

    frame = tk.Frame(root, bg=styles.FondoPantalla)
    frame.pack(fill="both", expand=True)

    tk.Label(
        frame, text="Histórico de Tickets",
        font=styles.FuenteTitulo, bg=styles.FondoPantalla
    ).pack(pady=15)

    cont = tk.Frame(frame, bg=styles.FondoPantalla)
    cont.pack(fill="both", expand=True, padx=10)

    canvas = tk.Canvas(cont, bg=styles.FondoPantalla)
    scroll = tk.Scrollbar(cont, orient="vertical", command=canvas.yview)
    lista = tk.Frame(canvas, bg=styles.FondoPantalla)

    lista.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=lista, anchor="nw")
    canvas.configure(yscrollcommand=scroll.set)

    canvas.pack(side="left", fill="both", expand=True)
    scroll.pack(side="right", fill="y")

    def refrescar():
        for w in lista.winfo_children():
            w.destroy()

        tickets = sqlite_db.obtener_tickets()

        for i, t in enumerate(tickets):
            bg = styles.FondoTicket if i % 2 == 0 else styles.FondoPanel
            fila = tk.Frame(lista, bg=bg, bd=1, relief="solid")
            fila.pack(fill="x", pady=2)

            info = f"#{t[0]} | {t[1]} | Mesa: {t[2] or 'Rápida'} | {t[4]:.2f} €"
            tk.Label(fila, text=info, bg=bg).pack(side="left", padx=5)

            tk.Button(
                fila, text="Ver detalle",
                command=lambda tid=t[0]: mostrar_detalle(tid)
            ).pack(side="right", padx=5)

    def mostrar_detalle(ticket_id):
        detalle = sqlite_db.obtener_detalle_ticket(ticket_id)

        cabecera = next(t for t in sqlite_db.obtener_tickets() if t[0] == ticket_id)
        lineas = [(d[1], None, d[0], d[3]) for d in detalle]

        texto = imprimir.generar_texto_ticket(cabecera, lineas)

        top = tk.Toplevel(root)
        top.title(f"Ticket {ticket_id}")
        top.geometry("450x600")

        area = scrolledtext.ScrolledText(top, font=styles.FuenteTicket)
        area.pack(fill="both", expand=True, padx=10, pady=10)
        area.insert("1.0", texto)
        area.config(state="disabled")

        tk.Button(
            top, text="Reimprimir",
            bg=styles.BotonImprimirColor, fg="white",
            command=lambda: imprimir.intentar_imprimir(texto)
        ).pack(pady=5)

    tk.Button(
        frame, text="Atrás",
        bg=styles.BotonCancelarColor, fg=styles.BotonCancelarFG,
        command=lambda: [frame.destroy(), parent.pack(fill="both", expand=True)]
    ).pack(pady=10)

    refrescar()
