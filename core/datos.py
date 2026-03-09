# core/datos.py
import os
import json
import random
import string
import hashlib

# ==========================================
# RUTAS DE ARCHIVOS (Configuración Base)
# ==========================================
DB_DIR = "db"
ARCHIVO_INVENTARIO = os.path.join(DB_DIR, "inventario.json")
ARCHIVO_EMPLEADOS = os.path.join(DB_DIR, "empleados.json")
ARCHIVO_MOVIMIENTOS = os.path.join(DB_DIR, "movimientos.json")
ARCHIVO_ROLES = os.path.join(DB_DIR, "roles.json")  # NUEVO: Base de datos de roles

# ==========================================
# BASES DE DATOS EN MEMORIA (Diccionarios)
# ==========================================
inventario_db = {}
usuarios_db = {}
movimientos_db = []
roles_db = {}


# ==========================================
# FUNCIONES DE CARGA Y GUARDADO
# ==========================================
def asegurar_carpetas():
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)


def cargar_datos_sistema():
    """Carga todos los JSON a la memoria del programa de forma segura."""
    global inventario_db, usuarios_db, movimientos_db
    asegurar_carpetas()

    # 1. Cargar Inventario (Con datos por defecto de papelería si no existe)
    if os.path.exists(ARCHIVO_INVENTARIO):
        with open(ARCHIVO_INVENTARIO, "r", encoding="utf-8") as f:
            inventario_db.clear()
            inventario_db.update(json.load(f))
    else:
        # Inventario semilla (predeterminado)
        inventario_db.clear()
        inventario_db.update(
            {
                "PAP-001": {
                    "nombre": "Cuaderno Universitario 100h",
                    "categoria": "Cuadernos",
                    "marca": "Norma",
                    "stock": 50,
                    "stock_minimo": 10,
                },
                "PAP-002": {
                    "nombre": "Esfero Tinta Seca Azul",
                    "categoria": "Escritura",
                    "marca": "Bic",
                    "stock": 120,
                    "stock_minimo": 20,
                },
                "PAP-003": {
                    "nombre": "Lápiz de Grafito HB 2",
                    "categoria": "Escritura",
                    "marca": "Staedtler",
                    "stock": 80,
                    "stock_minimo": 15,
                },
                "PAP-004": {
                    "nombre": "Resma de Papel A4 75g",
                    "categoria": "Papelería",
                    "marca": "Chamex",
                    "stock": 25,
                    "stock_minimo": 5,
                },
                "PAP-005": {
                    "nombre": "Borrador de Queso",
                    "categoria": "Accesorios",
                    "marca": "Pelikan",
                    "stock": 40,
                    "stock_minimo": 10,
                },
                "PAP-006": {
                    "nombre": "Caja de Marcadores x12",
                    "categoria": "Arte",
                    "marca": "Crayola",
                    "stock": 15,
                    "stock_minimo": 5,
                },
            }
        )
        guardar_inventario()

    # 3. Cargar Empleados (Con creación de Admin por defecto)
    if os.path.exists(ARCHIVO_EMPLEADOS):
        with open(ARCHIVO_EMPLEADOS, "r", encoding="utf-8") as f:
            usuarios_db.clear()
            usuarios_db.update(json.load(f))
    else:
        usuarios_db.clear()
        usuarios_db["admin"] = {
            "pass_hash": hashlib.sha256("123".encode()).hexdigest(),
            "rol": "Administrador",
            "permisos": roles_db[
                "Administrador"
            ],  # Usa los permisos del nuevo roles_db
            "bloqueado": False,
            "codigo_recuperacion": "ADMIN-0000",
        }
        guardar_empleados()

    # 4. Cargar Movimientos
    if os.path.exists(ARCHIVO_MOVIMIENTOS):
        with open(ARCHIVO_MOVIMIENTOS, "r", encoding="utf-8") as f:
            movimientos_db.clear()
            movimientos_db.extend(json.load(f))


def guardar_inventario():
    with open(ARCHIVO_INVENTARIO, "w", encoding="utf-8") as f:
        json.dump(inventario_db, f, indent=4)


def guardar_empleados():
    with open(ARCHIVO_EMPLEADOS, "w", encoding="utf-8") as f:
        json.dump(usuarios_db, f, indent=4)


def guardar_movimientos():
    with open(ARCHIVO_MOVIMIENTOS, "w", encoding="utf-8") as f:
        json.dump(movimientos_db, f, indent=4)


def guardar_roles():
    with open(ARCHIVO_ROLES, "w", encoding="utf-8") as f:
        json.dump(roles_db, f, indent=4)


# ==========================================
# FUNCIONES DE SEGURIDAD Y CONTROL DE ESTADO
# ==========================================
def generar_codigo_recuperacion():
    caracteres = string.ascii_uppercase + string.digits
    return "".join(random.choice(caracteres) for _ in range(6))


def bloquear_usuario(usuario):
    if usuario in usuarios_db:
        usuarios_db[usuario]["bloqueado"] = True
        guardar_empleados()


def desbloquear_usuario(usuario):
    if usuario in usuarios_db:
        usuarios_db[usuario]["bloqueado"] = False
        usuarios_db[usuario]["codigo_recuperacion"] = generar_codigo_recuperacion()
        guardar_empleados()
