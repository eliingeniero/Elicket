# styles.py

import tkinter as tk

# =====================================================
# TIPOGRAFÍA
# =====================================================
FuenteBase = "Arial"

FuenteTituloXL = (FuenteBase, 28, "bold")
FuenteTitulo   = (FuenteBase, 22, "bold")
FuenteNormal   = (FuenteBase, 16)
FuentePequena  = (FuenteBase, 14)
FuenteTicket   = ("Courier", 10)

# =====================================================
# COLORES BASE
# =====================================================
Blanco = "#FFFFFF"
Negro  = "#000000"

GrisClaro  = "#F2F2F2"
GrisMedio  = "#E0E0E0"
GrisOscuro = "#9E9E9E"

# =====================================================
# COLORES PRINCIPALES (IDENTIDAD)
# =====================================================
Verde   = "#4CAF50"
Azul    = "#2196F3"
Naranja = "#FF9800"
Morado  = "#9C27B0"
Rojo    = "#F44336"

# =====================================================
# FONDOS
# =====================================================
FondoPantalla = GrisClaro
FondoPanel    = Blanco
FondoTicket   = GrisMedio
FondoPopup    = Blanco

# =====================================================
# BOTONES — GENERALES
# =====================================================
BotonConfirmarColor = Verde
BotonConfirmarFG    = Blanco

BotonSecundarioColor = Azul
BotonSecundarioFG    = Blanco

BotonAvisoColor      = Naranja
BotonAvisoFG         = Blanco

BotonCancelarColor   = Rojo
BotonCancelarFG      = Blanco

BotonNeutroColor     = GrisOscuro
BotonNeutroFG        = Blanco

# =====================================================
# BOTONES — SECCIONES
# =====================================================
BotonFacturarColor      = Verde
BotonConfiguracionColor = Azul
BotonHistoricoColor     = Naranja
BotonFacturasColor      = Morado
BotonSalirColor         = Rojo

# =====================================================
# BOTONES — TICKETS
# =====================================================
BotonImprimirColor = Verde
BotonGuardarColor  = Azul
BotonNoImpresoColor = Naranja

# =====================================================
# MONEDAS Y BILLETES
# =====================================================
MonedaColores = {
    0.01: "#b87333",
    0.02: "#b87333",
    0.05: "#cd7f32",
    0.10: "#d4a017",
    0.20: "#e5c100",
    0.50: "#ffd700",
    1:    "#c0c0c0",
    2:    "#ffd700",
}

BilleteColores = {
    5:   "#e0e0e0",
    10:  "#ff5252",
    20:  "#448aff",
    50:  "#ff9800",
    100: "#4caf50",
    200: "#cddc39",
}

# =====================================================
# LAYOUT INICIO
# =====================================================
BloqueInicioSuper    = 0.6
BloqueInicioMedio    = 0.3
BloqueInicioInferior = 0.1

# =====================================================
# DIMENSIONES ESTÁNDAR
# =====================================================
PopupPequeño = (360, 240)
PopupMedio   = (420, 300)
PopupGrande  = (420, 560)



def crear_popup(root, titulo="Popup", tamaño=(420, 560), modal=True):
    top = tk.Toplevel(root)
    top.title(titulo)
    w, h = tamaño
    screen_w = top.winfo_screenwidth()
    screen_h = top.winfo_screenheight()
    x = (screen_w - w) // 2
    y = (screen_h - h) // 2
    top.geometry(f"{w}x{h}+{x}+{y}")
    top.configure(bg=FondoPopup)
    top.resizable(False, False)
    if modal:
        top.transient(root)
        top.grab_set()
    return top