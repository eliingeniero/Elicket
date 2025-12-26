# plantilla.py
import os
import tkinter as tk
from tkinter import messagebox, scrolledtext

PLANTILLA_PATH = os.path.join(
    os.path.dirname(__file__),
    "ticket_58mm.txt"
)

def abrir_editor_plantilla(root, on_close=None):
    """
    Abre una ventana emergente para editar la plantilla del ticket.
    on_close: función opcional que se llama al cerrar la ventana
    """
    if not os.path.exists(PLANTILLA_PATH):
        messagebox.showerror("Error", "No existe ticket_58mm.txt")
        return

    win = tk.Toplevel(root)
    win.title("Plantilla ticket 58mm")
    win.geometry("520x600")

    # Asegurar que la ventana emergente esté sobre la principal
    win.transient(root)
    win.grab_set()

    # Texto editable
    area = scrolledtext.ScrolledText(
        win,
        font=("Courier New", 10),
        wrap="none"
    )
    area.pack(fill="both", expand=True, padx=5, pady=5)

    with open(PLANTILLA_PATH, "r", encoding="utf-8") as f:
        area.insert("1.0", f.read())

    def guardar():
        try:
            with open(PLANTILLA_PATH, "w", encoding="utf-8") as f:
                f.write(area.get("1.0", "end-1c"))
            messagebox.showinfo("Guardado", "Plantilla guardada correctamente")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Frame con botones
    frame = tk.Frame(win)
    frame.pack(pady=5)

    tk.Button(frame, text="Guardar", width=12, command=guardar).pack(side="left", padx=5)

    def cerrar():
        win.destroy()
        if on_close:
            on_close()  # se llama la función opcional al cerrar

    tk.Button(frame, text="Cerrar", width=12, command=cerrar).pack(side="right", padx=5)
