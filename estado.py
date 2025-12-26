# estado.py

# clave: codigo_mesa (None para venta rápida)
# valor: ticket dict
ticketsTemporalesMesa = {}

def obtener_ticket(mesa):
    return ticketsTemporalesMesa.setdefault(mesa, {})

def borrar_ticket(mesa):
    ticketsTemporalesMesa.pop(mesa, None)

def limpiar_todo():
    ticketsTemporalesMesa.clear()
