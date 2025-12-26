import os
import sys
import tempfile
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

# ==========================
# WINDOWS / PYWIN32
# ==========================
if sys.platform.startswith("win"):
    try:
        import win32print
        import win32api
    except ImportError:
        win32print = None
        win32api = None

# ==========================
# PREVIEW
# ==========================
def mostrar_preview(texto, titulo="Previsualización ticket"):
    top = tk.Toplevel()
    top.title(titulo)
    top.geometry("420x560")
    top.resizable(False, False)

    txt = ScrolledText(top, font=("Courier", 10))
    txt.pack(fill="both", expand=True, padx=10, pady=10)
    txt.insert("1.0", texto)
    txt.config(state="disabled")

    tk.Button(
        top,
        text="Cerrar",
        width=18,
        bg="#F44336",
        fg="white",
        command=top.destroy
    ).pack(pady=10)

# ==========================
# IMPRESIÓN REAL
# ==========================
def hay_impresora():
    if not sys.platform.startswith("win") or not win32print:
        return False
    try:
        printers = win32print.EnumPrinters(
            win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS
        )
        return bool(printers)
    except Exception:
        return False

def imprimir_texto(texto):
    """
    Imprime texto plano en Windows.
    Devuelve True si se envía a impresora.
    """
    if not hay_impresora():
        return False

    try:
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".txt",
            mode="w",
            encoding="utf-8"
        ) as f:
            f.write(texto)
            ruta = f.name

        win32api.ShellExecute(
            0,
            "print",
            ruta,
            None,
            ".",
            0
        )
        return True
    except Exception:
        return False

def mostrar_ticket_no_impreso(texto):
    """
    Muestra ventana tipo previsualización indicando que no se pudo imprimir.
    """
    mostrar_preview(texto, titulo="TICKET NO IMPRESO")

def intentar_imprimir(texto):
    """
    Intenta imprimir; si falla, muestra ventana 'TICKET NO IMPRESO'.
    Devuelve True si se imprimió, False si no.
    """
    if imprimir_texto(texto):
        return True
    mostrar_ticket_no_impreso(texto)
    return False

# ==========================
# PLANTILLAS
# ==========================
def cargar_plantilla(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def generar_texto_ticket(cabecera, lineas, plantilla=None):
    _, fecha, mesa, forma_pago, total = cabecera

    if plantilla:
        txt = plantilla
        txt = txt.replace("{fecha}", fecha)
        txt = txt.replace("{mesa}", str(mesa))
        txt = txt.replace("{forma_pago}", forma_pago)
        txt = txt.replace("{total}", f"{total:.2f} €")

        items = ""
        for cant, _, nombre, subtotal in lineas:
            items += f"{cant} x {nombre}    {subtotal:.2f} €\n"

        txt = txt.replace("{lineas}", items)
        return txt

    # Fallback sin plantilla
    salida = [
        "      TICKET",
        "----------------------",
        f"Fecha: {fecha}",
        f"Mesa: {mesa}",
        f"Pago: {forma_pago}",
        "----------------------",
    ]
    for cant, _, nombre, subtotal in lineas:
        salida.append(f"{cant} x {nombre}")
        salida.append(f"    {subtotal:.2f} €")
    salida.extend([
        "----------------------",
        f"TOTAL: {total:.2f} €",
        "",
        "Gracias por su visita"
    ])
    return "\n".join(salida)

def generar_texto_ticket_efectivo(cabecera, lineas, entregado, cambio, plantilla=None):
    texto = generar_texto_ticket(cabecera, lineas, plantilla)
    texto += f"\n\nEntregado: {entregado:.2f} €"
    texto += f"\nCambio: {cambio:.2f} €"
    return texto
