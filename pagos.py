# pagos.py
import tkinter as tk
from tkinter import messagebox
import datetime
import sqlite_db
import estado
import imprimir
import styles
import os

plantilla_path = os.path.join(os.path.dirname(__file__), "ticket_58mm.txt")


# ==========================
# Previsualización rápida
# ==========================
def mostrar_ticket(ticket, mesa=None):
    if not ticket:
        messagebox.showinfo("Info", "No hay artículos en el ticket")
        return

    total = sum(info["cantidad"] * info["precio"] for info in ticket.values())
    fecha = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

    lineas = [
        (info["cantidad"], None, info["nombre"], info["cantidad"] * info["precio"])
        for info in ticket.values()
    ]

    cabecera = (None, fecha, mesa or "Rápida", "Previsualización", total)
    plantilla = imprimir.cargar_plantilla(plantilla_path)
    texto = imprimir.generar_texto_ticket(cabecera, lineas, plantilla)

    top = tk.Toplevel()
    top.title("Previsualización ticket")
    top.configure(bg=styles.FondoPantalla)
    top.geometry("420x560")
    top.resizable(False, False)

    txt = tk.Text(top, font=styles.FuenteTicket)
    txt.pack(fill="both", expand=True, padx=10, pady=10)
    txt.insert("1.0", texto)
    txt.config(state="disabled")

    frame = tk.Frame(top, bg=styles.FondoPantalla)
    frame.pack(pady=10)

    def imprimir_ticket():
        imprimir.intentar_imprimir(texto)
        top.destroy()

    tk.Button(
        frame, text="Imprimir ticket", width=18,
        bg=styles.BotonImprimirColor, fg="white",
        command=imprimir_ticket
    ).pack(side="left", padx=5)

    tk.Button(
        frame, text="Cancelar", width=18,
        bg=styles.BotonNoImpresoColor, fg="white",
        command=top.destroy
    ).pack(side="left", padx=5)


# ==========================
# Confirmar venta
# ==========================
def confirmar_venta(root, ticket, mesa=None, refrescar_ui=None):
    if not ticket:
        messagebox.showinfo("Info", "No hay artículos en el ticket")
        return

    total = sum(info["cantidad"] * info["precio"] for info in ticket.values())
    pago = seleccionar_pago(root, total)
    if pago is None:
        return

    forma_pago, entregado, cambio = pago
    fecha = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

    cabecera = (None, fecha, mesa or "Rápida", forma_pago, total)

    lineas_ticket = [
        (info["cantidad"], None, info["nombre"], info["cantidad"] * info["precio"])
        for info in ticket.values()
    ]

    plantilla = imprimir.cargar_plantilla(plantilla_path)

    if forma_pago == "Efectivo":
        texto = imprimir.generar_texto_ticket_efectivo(
            cabecera, lineas_ticket, entregado, cambio, plantilla
        )
    else:
        texto = imprimir.generar_texto_ticket(cabecera, lineas_ticket, plantilla)

    top = tk.Toplevel(root)
    top.title("Ticket final")
    top.configure(bg=styles.FondoPantalla)
    top.geometry("420x560")
    top.resizable(False, False)

    txt = tk.Text(top, font=styles.FuenteTicket)
    txt.pack(fill="both", expand=True, padx=10, pady=10)
    txt.insert("1.0", texto)
    txt.config(state="disabled")

    frame = tk.Frame(top, bg=styles.FondoPantalla)
    frame.pack(pady=10)

    def guardar_bd():
        sqlite_db.registrar_ticket(ticket, mesa, forma_pago)
        if mesa:
            estado.borrar_ticket(mesa)
        if refrescar_ui:
            refrescar_ui()

    def imprimir_guardar():
        imprimir.intentar_imprimir(texto)
        guardar_bd()
        top.destroy()

    def guardar_sin_imprimir():
        guardar_bd()
        top.destroy()

    tk.Button(
        frame, text="Imprimir y guardar", width=18,
        bg=styles.BotonImprimirColor, fg="white",
        command=imprimir_guardar
    ).pack(side="left", padx=5)

    tk.Button(
        frame, text="Guardar sin imprimir", width=18,
        bg=styles.BotonGuardarColor, fg="white",
        command=guardar_sin_imprimir
    ).pack(side="left", padx=5)

    tk.Button(
        frame, text="Cancelar", width=18,
        bg=styles.BotonNoImpresoColor, fg="white",
        command=top.destroy
    ).pack(side="left", padx=5)


# ==========================
# Selector de pago
# ==========================
def seleccionar_pago(root, total):
    resultado = {"valor": None}

    top = tk.Toplevel(root)
    top.title("Forma de pago")
    top.transient(root)
    top.grab_set()
    top.configure(bg=styles.FondoPantalla)
    top.geometry("360x160")
    top.resizable(False, False)

    tk.Label(
        top, text="Seleccione método de pago",
        font=styles.FuenteNormal, bg=styles.FondoPantalla
    ).pack(pady=20)

    frame = tk.Frame(top, bg=styles.FondoPantalla)
    frame.pack(pady=10)

    def tarjeta():
        resultado["valor"] = ("Tarjeta", None, None)
        top.destroy()

    def efectivo():
        top.destroy()
        resultado["valor"] = pago_efectivo(root, total)

    tk.Button(
        frame, text="Efectivo", width=14,
        bg=styles.BotonConfirmarColor, fg=styles.BotonConfirmarFG,
        command=efectivo
    ).pack(side="left", padx=10)

    tk.Button(
        frame, text="Tarjeta", width=14,
        bg=styles.BotonSecundarioColor, fg=styles.BotonSecundarioFG,
        command=tarjeta
    ).pack(side="right", padx=10)

    root.wait_window(top)
    return resultado["valor"]


# ==========================
# Pago en efectivo
# ==========================
def pago_efectivo(root, total):
    resultado = {"valor": None}

    top = tk.Toplevel(root)
    top.title("Pago en efectivo")
    top.transient(root)
    top.grab_set()
    top.configure(bg=styles.FondoPantalla)
    top.geometry("480x320")
    top.resizable(False, False)

    tk.Label(
        top, text=f"Total a pagar: {total:.2f} €",
        font=styles.FuenteNormal, bg=styles.FondoPantalla
    ).pack(pady=10)

    acumulado = tk.DoubleVar(value=0.0)

    lbl_pagado = tk.Label(top, text="Pagado: 0.00 €", bg=styles.FondoPantalla)
    lbl_pagado.pack()

    lbl_cambio = tk.Label(top, text="Cambio: 0.00 €", bg=styles.FondoPantalla)
    lbl_cambio.pack()

    def actualizar():
        pagado = acumulado.get()
        lbl_pagado.config(text=f"Pagado: {pagado:.2f} €")
        lbl_cambio.config(text=f"Cambio: {pagado - total:.2f} €")

    frame = tk.Frame(top, bg=styles.FondoPantalla)
    frame.pack(pady=10)

    for v in [0.5, 1, 2, 5, 10, 20, 50]:
        tk.Button(
            frame, text=f"{v:.2f} €", width=6,
            command=lambda x=v: [acumulado.set(acumulado.get() + x), actualizar()]
        ).pack(side="left", padx=3)

    def confirmar():
        pagado = acumulado.get()
        if pagado < total:
            messagebox.showerror("Error", "Cantidad insuficiente")
            return
        resultado["valor"] = ("Efectivo", pagado, pagado - total)
        top.destroy()

    tk.Button(top, text="Confirmar", command=confirmar).pack(pady=10)
    tk.Button(top, text="Cancelar", command=top.destroy).pack()

    root.wait_window(top)
    return resultado["valor"]
