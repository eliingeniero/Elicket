# inicio.py
import tkinter as tk

import styles
import facturar
import historico
import histoFacturas
import configuracion


def abrir_inicio(root):
    root.state('zoomed')
    root.update()

    pantalla_inicio = tk.Frame(root, bg=styles.FondoPantalla)
    pantalla_inicio.pack(fill="both", expand=True)

    # BLOQUE SUPERIOR
    bloque1 = tk.Frame(pantalla_inicio, bg=styles.FondoPantalla)
    bloque1.place(relx=0, rely=0, relwidth=1, relheight=styles.BloqueInicioSuper)

    btn_facturar = tk.Button(
        bloque1,
        text="FACTURAR",
        font=styles.FuenteTitulo,
        bg=styles.BotonFacturarColor,
        fg=styles.BotonConfirmarFG,
        command=lambda: facturar.abrir_facturar(root, pantalla_inicio)
    )
    btn_facturar.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.5, relheight=0.3)

    # BLOQUE MEDIO
    bloque2 = tk.Frame(pantalla_inicio, bg=styles.FondoPantalla)
    bloque2.place(relx=0, rely=styles.BloqueInicioSuper, relwidth=1, relheight=styles.BloqueInicioMedio)

    btn_config = tk.Button(
        bloque2,
        text="Configuración",
        font=styles.FuenteNormal,
        bg=styles.BotonConfiguracionColor,
        fg=styles.BotonConfirmarFG,
        command=lambda: [pantalla_inicio.pack_forget(), configuracion.abrir_configuracion(root, pantalla_inicio)]
    )
    btn_historico = tk.Button(
        bloque2,
        text="Histórico de tickets",
        font=styles.FuenteNormal,
        bg=styles.BotonHistoricoColor,
        fg=styles.BotonConfirmarFG,
        command=lambda: historico.abrir_historico(root, pantalla_inicio)
    )
    btn_facturas = tk.Button(
        bloque2,
        text="Histórico de facturas",
        font=styles.FuenteNormal,
        bg=styles.BotonFacturasColor,
        fg=styles.BotonConfirmarFG,
        command=lambda: histoFacturas.abrir_historico_facturas(root, pantalla_inicio)
    )

    btn_config.place(relx=0.05, rely=0.2, relwidth=0.28, relheight=0.6)
    btn_historico.place(relx=0.36, rely=0.2, relwidth=0.28, relheight=0.6)
    btn_facturas.place(relx=0.67, rely=0.2, relwidth=0.28, relheight=0.6)

    # BLOQUE INFERIOR
    bloque3 = tk.Frame(pantalla_inicio, bg=styles.FondoPantalla)
    bloque3.place(relx=0, rely=styles.BloqueInicioSuper + styles.BloqueInicioMedio,
                  relwidth=1, relheight=styles.BloqueInicioInferior)

    btn_salir = tk.Button(
        bloque3,
        text="SALIR",
        font=styles.FuenteTitulo,
        bg=styles.BotonSalirColor,
        fg=styles.BotonCancelarFG,
        command=root.quit
    )
    btn_salir.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.5, relheight=0.6)
