# sqlite_db.py
import sqlite3
from datetime import datetime
import os

# =====================================================
# RUTA BBDD
# =====================================================
DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "valverde.db")


# =====================================================
# CONEXIÓN
# =====================================================
def conectar():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# =====================================================
# CREAR TABLAS
# =====================================================
def crear_tablas():
    conn = conectar()
    cur = conn.cursor()

    # -----------------------------
    # CATEGORÍAS (PK MANUAL)
    # -----------------------------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS categorias (
            codigo INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            descripcion TEXT
        )
    """)

    # -----------------------------
    # ARTÍCULOS (PK MANUAL)
    # -----------------------------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS articulos (
            codigo INTEGER PRIMARY KEY,
            categoria_codigo INTEGER NOT NULL,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            precio_actual REAL NOT NULL,
            activo INTEGER DEFAULT 1,
            FOREIGN KEY (categoria_codigo) REFERENCES categorias(codigo)
        )
    """)

    # -----------------------------
    # MESAS (PK MANUAL)
    # -----------------------------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS mesas (
            codigo TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            asientos INTEGER NOT NULL
        )
    """)

    # -----------------------------
    # TICKETS
    # -----------------------------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            mesa_codigo TEXT NULL,
            forma_pago TEXT NOT NULL,
            total REAL NOT NULL,
            estado TEXT DEFAULT 'cerrado',
            FOREIGN KEY (mesa_codigo) REFERENCES mesas(codigo)
        )
    """)

    # -----------------------------
    # LÍNEAS DE TICKET (PRECIO CONGELADO)
    # -----------------------------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ticket_lineas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id INTEGER NOT NULL,
            articulo_codigo INTEGER,
            nombre_articulo TEXT NOT NULL,
            precio_unitario REAL NOT NULL,
            cantidad INTEGER NOT NULL,
            subtotal REAL NOT NULL,
            FOREIGN KEY (ticket_id) REFERENCES tickets(id)
        )
    """)

    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_ticket_lineas_ticket
        ON ticket_lineas(ticket_id)
    """)

    # -----------------------------
    # EMPRESAS
    # -----------------------------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS empresas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            cif TEXT,
            direccion TEXT
        )
    """)

    # -----------------------------
    # FACTURAS
    # -----------------------------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS facturas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id INTEGER NOT NULL UNIQUE,
            empresa_id INTEGER NOT NULL,
            fecha TEXT NOT NULL,
            numero TEXT NOT NULL UNIQUE,
            total REAL NOT NULL,
            anulada INTEGER DEFAULT 0,
            FOREIGN KEY (ticket_id) REFERENCES tickets(id),
            FOREIGN KEY (empresa_id) REFERENCES empresas(id)
        )
    """)

    conn.commit()
    conn.close()


# =====================================================
# CATEGORÍAS
# =====================================================
def obtener_categorias():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT codigo, nombre, descripcion FROM categorias ORDER BY codigo")
    datos = cur.fetchall()
    conn.close()
    return datos


def agregar_categoria(codigo, nombre, descripcion=""):
    conn = conectar()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO categorias (codigo, nombre, descripcion) VALUES (?, ?, ?)",
            (codigo, nombre, descripcion)
        )
        conn.commit()
        return True, ""
    except sqlite3.IntegrityError:
        return False, "Código de categoría duplicado"
    finally:
        conn.close()


def modificar_categoria(codigo, nombre, descripcion=""):
    conn = conectar()
    cur = conn.cursor()
    cur.execute(
        "UPDATE categorias SET nombre=?, descripcion=? WHERE codigo=?",
        (nombre, descripcion, codigo)
    )
    conn.commit()
    conn.close()
    return True, ""


def eliminar_categoria(codigo):
    conn = conectar()
    cur = conn.cursor()

    cur.execute("SELECT 1 FROM articulos WHERE categoria_codigo=?", (codigo,))
    if cur.fetchone():
        conn.close()
        return False

    cur.execute("DELETE FROM categorias WHERE codigo=?", (codigo,))
    conn.commit()
    conn.close()
    return True


# =====================================================
# ARTÍCULOS
# =====================================================
def obtener_articulos():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        SELECT a.codigo, c.nombre, a.nombre, a.descripcion, a.precio_actual
        FROM articulos a
        JOIN categorias c ON a.categoria_codigo = c.codigo
        WHERE a.activo = 1
        ORDER BY a.codigo
    """)
    datos = cur.fetchall()
    conn.close()
    return datos


def obtener_articulos_categoria(categoria_codigo):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        SELECT codigo, categoria_codigo, nombre, descripcion, precio_actual
        FROM articulos
        WHERE categoria_codigo=? AND activo=1
        ORDER BY nombre
    """, (categoria_codigo,))
    datos = cur.fetchall()
    conn.close()
    return datos


def agregar_articulo(codigo, categoria_codigo, nombre, descripcion, precio):
    conn = conectar()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO articulos
            (codigo, categoria_codigo, nombre, descripcion, precio_actual)
            VALUES (?, ?, ?, ?, ?)
        """, (codigo, categoria_codigo, nombre, descripcion, float(precio)))
        conn.commit()
        return True, ""
    except sqlite3.IntegrityError:
        return False, "Código de artículo duplicado"
    finally:
        conn.close()


def eliminar_articulo(codigo):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("DELETE FROM articulos WHERE codigo=?", (codigo,))
    conn.commit()
    conn.close()


# =====================================================
# MESAS
# =====================================================
def obtener_mesas():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT codigo, nombre, asientos FROM mesas ORDER BY codigo")
    datos = cur.fetchall()
    conn.close()
    return datos


def agregar_mesa(codigo, nombre, asientos):
    conn = conectar()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO mesas (codigo, nombre, asientos) VALUES (?, ?, ?)",
            (codigo, nombre, int(asientos))
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def modificar_mesa(codigo, nombre, asientos):
    conn = conectar()
    cur = conn.cursor()
    cur.execute(
        "UPDATE mesas SET nombre=?, asientos=? WHERE codigo=?",
        (nombre, int(asientos), codigo)
    )
    conn.commit()
    conn.close()


def eliminar_mesa(codigo):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("DELETE FROM mesas WHERE codigo=?", (codigo,))
    conn.commit()
    conn.close()
    return True


# =====================================================
# TICKETS
# =====================================================
def registrar_ticket(ticket_dict, mesa_codigo=None, forma_pago="Efectivo"):
    if not ticket_dict:
        return None

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    total = 0.0
    lineas = []

    for art_cod, info in ticket_dict.items():
        cantidad = info["cantidad"]
        precio = float(info["precio"])
        subtotal = cantidad * precio
        total += subtotal
        lineas.append((art_cod, info["nombre"], precio, cantidad, subtotal))

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO tickets (fecha, mesa_codigo, forma_pago, total)
        VALUES (?, ?, ?, ?)
    """, (fecha, mesa_codigo, forma_pago, total))

    ticket_id = cur.lastrowid

    for art_cod, nombre, precio, cantidad, subtotal in lineas:
        cur.execute("""
            INSERT INTO ticket_lineas
            (ticket_id, articulo_codigo, nombre_articulo, precio_unitario, cantidad, subtotal)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (ticket_id, art_cod, nombre, precio, cantidad, subtotal))

    conn.commit()
    conn.close()
    return ticket_id


# =====================================================
# INIT
# =====================================================
crear_tablas()
