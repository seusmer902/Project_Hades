import json
import os
import hashlib
import random
import string

# Importamos configuración desde el mismo paquete
from .config import (
    ARCHIVO_DATOS,
    ARCHIVO_VENTAS,
    INVENTARIO_INICIAL,
    ARCHIVO_CLIENTES,
    ARCHIVO_USUARIOS,
    ARCHIVO_PENDIENTES,
)

# --- BASES DE DATOS EN MEMORIA ---
inventario_db = {}
ventas_db = []
clientes_db = {}
usuarios_db = {}
pendientes_db = {}

# --- ROLES Y PERMISOS (¡AQUÍ ESTABA EL ERROR!) ---
PERMISOS_DISPONIBLES = {
    "VENTAS": "Acceso a Caja y Facturación",
    "STOCK": "Movimientos de Entrada/Salida",
    "PROD": "Crear, Editar y Borrar Productos",
    "CLIENTES": "Registrar y Ver Clientes",
    "REPORTES": "Ver Historial de Ventas y Dinero",
    "ADMIN": "Gestión Total (Usuarios y Config)",
    "COMPRA_SELF": "Permiso para comprar como cliente",  # Nuevo
}

ROLES_PLANTILLA = {
    "Administrador": ["VENTAS", "STOCK", "PROD", "CLIENTES", "REPORTES", "ADMIN"],
    "Cajero": ["VENTAS", "CLIENTES"],
    "Bodeguero": ["STOCK", "PROD"],
    "Supervisor": ["VENTAS", "STOCK", "CLIENTES", "REPORTES"],
    "Cliente": ["COMPRA_SELF"],  # ROL NUEVO PARA INVITADOS
}


# --- UTILIDADES ---
def generar_codigo_recuperacion():
    chars = string.ascii_uppercase + string.digits
    return "".join(random.choice(chars) for _ in range(6))


# --- CARGA DE DATOS ---
def cargar_datos_sistema():
    global inventario_db, ventas_db, clientes_db, usuarios_db, pendientes_db

    # 1. Inventario
    if os.path.exists(ARCHIVO_DATOS):
        try:
            with open(ARCHIVO_DATOS, "r", encoding="utf-8") as f:
                data = json.load(f)
                inventario_db.clear()
                inventario_db.update(data)
        except:
            inventario_db.clear()
    else:
        inventario_db.clear()
        inventario_db.update(INVENTARIO_INICIAL)
        guardar_inventario()

    # 2. Ventas
    if os.path.exists(ARCHIVO_VENTAS):
        try:
            with open(ARCHIVO_VENTAS, "r", encoding="utf-8") as f:
                data = json.load(f)
                ventas_db[:] = data
        except:
            ventas_db[:] = []
    else:
        ventas_db[:] = []

    # 3. Clientes
    if os.path.exists(ARCHIVO_CLIENTES):
        try:
            with open(ARCHIVO_CLIENTES, "r", encoding="utf-8") as f:
                data = json.load(f)
                clientes_db.clear()
                clientes_db.update(data)
        except:
            clientes_db.clear()
    else:
        clientes_db.clear()

    # 4. Usuarios
    if os.path.exists(ARCHIVO_USUARIOS):
        try:
            with open(ARCHIVO_USUARIOS, "r", encoding="utf-8") as f:
                data = json.load(f)
                usuarios_db.clear()
                usuarios_db.update(data)

                # Migración de campos nuevos
                cambios = False
                for u, val in usuarios_db.items():
                    if "bloqueado" not in val:
                        val["bloqueado"] = False
                        cambios = True
                    if "codigo_recuperacion" not in val:
                        val["codigo_recuperacion"] = "ADMIN1"
                        cambios = True
                if cambios:
                    guardar_usuarios()
        except:
            usuarios_db.clear()
    else:
        # Admin por defecto (Pass: 123)
        pass_hash = hashlib.sha256("123".encode()).hexdigest()
        usuarios_db.clear()
        usuarios_db.update(
            {
                "admin": {
                    "pass_hash": pass_hash,
                    "rol": "Administrador",
                    "permisos": ROLES_PLANTILLA["Administrador"],
                    "bloqueado": False,
                    "codigo_recuperacion": "ADMIN1",
                }
            }
        )
        guardar_usuarios()

    # 5. Pendientes
    if os.path.exists(ARCHIVO_PENDIENTES):
        try:
            with open(ARCHIVO_PENDIENTES, "r", encoding="utf-8") as f:
                data = json.load(f)
                pendientes_db.clear()
                pendientes_db.update(data)
        except:
            pendientes_db.clear()
    else:
        pendientes_db.clear()


# --- GUARDADO ---
def guardar_inventario():
    with open(ARCHIVO_DATOS, "w", encoding="utf-8") as f:
        json.dump(inventario_db, f, indent=4)


def guardar_historial_ventas():
    with open(ARCHIVO_VENTAS, "w", encoding="utf-8") as f:
        json.dump(ventas_db, f, indent=4)


def guardar_clientes():
    with open(ARCHIVO_CLIENTES, "w", encoding="utf-8") as f:
        json.dump(clientes_db, f, indent=4)


def guardar_usuarios():
    with open(ARCHIVO_USUARIOS, "w", encoding="utf-8") as f:
        json.dump(usuarios_db, f, indent=4)


def guardar_pendientes():
    with open(ARCHIVO_PENDIENTES, "w", encoding="utf-8") as f:
        json.dump(pendientes_db, f, indent=4)


# --- ACCIONES ---
def resetear_password(usuario, nueva_pass):
    if usuario in usuarios_db:
        usuarios_db[usuario]["pass_hash"] = hashlib.sha256(
            nueva_pass.encode()
        ).hexdigest()
        guardar_usuarios()
        return True
    return False


def bloquear_usuario(usuario):
    if usuario in usuarios_db:
        usuarios_db[usuario]["bloqueado"] = True
        guardar_usuarios()
