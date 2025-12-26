# configuracion.py
import tkinter as tk
import inicio
import categoriasArticulos
import mesas
import empresas
import plantilla
import styles

def abrir_configuracion(root, parent):
    # Ocultar pantalla anterior
    parent.pack_forget()

    pantalla_config = tk.Frame(root, bg=styles.FondoPantalla)
    pantalla_config.pack(fill="both", expand=True)

    # Título
    tk.Label(
        pantalla_config,
        text="Configuración",
        font=styles.FuenteTitulo,
        bg=styles.FondoPantalla
    ).pack(pady=20)

    # Funciones lambda que reciben pantalla_config para ocultarla
    botones_info = [
        ("Artículos", lambda: categoriasArticulos.abrir_articulos(root, pantalla_config)),
        ("Categorías", lambda: categoriasArticulos.abrir_categorias(root, pantalla_config)),
        ("Mesas", lambda: mesas.abrir_mesas(root, pantalla_config)),
        ("Empresas", lambda: empresas.abrir_empresas(root, pantalla_config)),
        ("Plantilla ticket", lambda: plantilla.abrir_editor_plantilla(root))  # Emergente, no oculta configuración
    ]

    # Contenedor de botones
    cont_botones = tk.Frame(pantalla_config, bg=styles.FondoPantalla)
    cont_botones.pack(fill="both", expand=True, padx=50, pady=20)

    cols = 2
    for i, (texto, funcion) in enumerate(botones_info):
        ancho = 25 if texto == "Plantilla ticket" else 20
        alto = 2 if texto == "Plantilla ticket" else 5
        btn = tk.Button(
            cont_botones,
            text=texto,
            width=ancho,
            height=alto,
            font=styles.FuenteNormal,
            bg=styles.BotonNeutroColor,
            fg=styles.BotonNeutroFG,
            command=funcion
        )
        btn.grid(row=i//cols, column=i%cols, sticky="nsew", padx=20, pady=20)

    for r in range((len(botones_info) + cols - 1) // cols):
        cont_botones.grid_rowconfigure(r, weight=1)
    for c in range(cols):
        cont_botones.grid_columnconfigure(c, weight=1)

    # Botón volver
    tk.Button(
        pantalla_config,
        text="Volver",
        width=15,
        height=2,
        font=styles.FuenteNormal,
        bg=styles.BotonCancelarColor,
        fg=styles.BotonCancelarFG,
        command=lambda: [pantalla_config.pack_forget(), inicio.abrir_inicio(root)]
    ).pack(pady=20)
