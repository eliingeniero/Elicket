# historicoFacturas.py
import tkinter as tk
from tkinter import scrolledtext, messagebox
import sqlite_db
import imprimir
import styles

def abrir_historico_facturas(root, parent):
    # Ocultar pantalla anterior
    parent.pack_forget()

    # Crear frame histórico
    frame_hist = tk.Frame(root, bg=styles.FondoPantalla)
    frame_hist.pack(fill="both", expand=True)

    tk.Label(frame_hist, text="Histórico de Facturas",
             font=styles.FuenteTitulo, bg=styles.FondoPantalla).pack(pady=15)

    contenedor = tk.Frame(frame_hist, bg=styles.FondoPantalla)
    contenedor.pack(fill="both", expand=True, padx=10, pady=5)

    canvas = tk.Canvas(contenedor, bg=styles.FondoPantalla)
    scrollbar_y = tk.Scrollbar(contenedor, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg=styles.FondoPantalla)

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar_y.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar_y.pack(side="right", fill="y")

    def refrescar():
        for w in scroll_frame.winfo_children():
            w.destroy()

        facturas = sqlite_db.obtener_facturas()
        facturas.sort(key=lambda x: x[3], reverse=True)  # ordenar por fecha descendente

        for i, f in enumerate(facturas):
            color_fila = styles.FondoTicket if i % 2 == 0 else styles.FondoPanel
            fila = tk.Frame(scroll_frame, bg=color_fila, bd=1, relief="solid", padx=5, pady=5)
            fila.pack(fill="x", pady=2)

            info = f"Código: {f[0]}  |  Ticket: {f[1]}  |  Empresa: {f[2]}  |  Fecha: {f[3]}  |  Importe: {f[5]:.2f} €  |  Anulada: {'Sí' if f[6] else 'No'}"
            tk.Label(fila, text=info, font=styles.FuenteNormal, bg=color_fila, anchor="w").pack(side="left", padx=5)

            tk.Button(fila, text="Ver detalle",
                      font=styles.FuentePequena,
                      bg=styles.BotonFacturasColor, fg=styles.BotonConfirmarFG,
                      command=lambda factura=f: mostrar_detalle_factura(factura)).pack(side="right", padx=5)

    def mostrar_detalle_factura(factura):
        """
        factura = (id, codigoTicket, nombreEmpresa, fecha, numeroFactura, importe, anulada)
        """
        top = tk.Toplevel(root)
        top.title(f"Detalle Factura {factura[4]}")
        top.configure(bg=styles.FondoPantalla)
        top.geometry("450x600")

        # Detalle del ticket asociado
        detalle_db = sqlite_db.obtener_detalle_ticket(factura[1])
        detalle_para_imprimir = []
        for _, cod_articulo, uds, precio_total in detalle_db:
            articulo = sqlite_db.obtener_articulo_paraticket(cod_articulo)
            nombre = articulo["nombre"] if articulo else "Desconocido"
            detalle_para_imprimir.append((uds, cod_articulo, nombre, precio_total))

        cabecera = (factura[1], factura[3], "-", "-", factura[5])
        texto = imprimir.generar_texto_ticket(cabecera, detalle_para_imprimir)
        texto = f"Factura: {factura[4]}\nEmpresa: {factura[2]}\nFecha: {factura[3]}\n\n" + texto

        area = scrolledtext.ScrolledText(top, font=styles.FuenteTicket)
        area.pack(fill="both", expand=True, padx=10, pady=10)
        area.insert("1.0", texto)
        area.config(state="disabled", bg=styles.FondoPopup)

        frame_botones = tk.Frame(top, bg=styles.FondoPantalla)
        frame_botones.pack(fill="x", padx=10, pady=5)

        if not factura[6]:
            tk.Button(frame_botones, text="Anular factura",
                      font=styles.FuenteNormal,
                      bg=styles.BotonAvisoColor, fg=styles.BotonAvisoFG,
                      command=lambda: confirmar_anulacion(factura[0], top)).pack(side="left", padx=5, pady=5)

        def confirmar_anulacion(id_factura, ventana):
            if messagebox.askyesno("Confirmar", "¿Seguro que quieres anular esta factura?"):
                sqlite_db.anular_factura(id_factura)
                messagebox.showinfo("Éxito", "Factura anulada")
                ventana.destroy()
                refrescar()

        tk.Button(frame_botones, text="Cerrar", font=styles.FuenteNormal,
                  bg=styles.BotonCancelarColor, fg=styles.BotonCancelarFG,
                  command=top.destroy).pack(side="right", padx=5, pady=5)

    tk.Button(frame_hist, text="Atrás", font=styles.FuenteNormal,
              bg=styles.BotonCancelarColor, fg=styles.BotonCancelarFG,
              command=lambda: [frame_hist.destroy(), parent.pack(fill="both", expand=True)]).pack(pady=10)

    refrescar()
