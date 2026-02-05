# datos.py
import json
import os

# Cambio de ruta: Importamos desde el mismo paquete
from .config import (
    ARCHIVO_DATOS,
    ARCHIVO_VENTAS,
    INVENTARIO_INICIAL,
    ARCHIVO_CLIENTES,
    ARCHIVO_USUARIOS,
)

# Variables Globales (Sin cambios)
inventario_db = {}
ventas_db = []
clientes_db = {}
usuarios_db = {}

# Definición de Permisos y Roles (Sin cambios)
PERMISOS_DISPONIBLES = {
    "VENTAS": "Acceso a Caja y Facturación",
    "STOCK": "Movimientos de Entrada/Salida",
    "PROD": "Crear, Editar y Borrar Productos",
    "CLIENTES": "Registrar y Ver Clientes",
    "REPORTES": "Ver Historial de Ventas y Dinero",
    "ADMIN": "Gestión Total (Usuarios y Config)",
}

ROLES_PLANTILLA = {
    "Administrador": ["VENTAS", "STOCK", "PROD", "CLIENTES", "REPORTES", "ADMIN"],
    "Cajero": ["VENTAS", "CLIENTES"],
    "Bodeguero": ["STOCK", "PROD"],
    "Supervisor": ["VENTAS", "STOCK", "CLIENTES", "REPORTES"],
}


# Funciones de Carga y Guardado (Lógica original intacta)
def cargar_datos_sistema():
    global inventario_db, ventas_db, clientes_db, usuarios_db

    # 1. Cargar Inventario
    if os.path.exists(ARCHIVO_DATOS):
        try:
            with open(ARCHIVO_DATOS, "r", encoding="utf-8") as f:
                inventario_db = json.load(f)
        except:
            inventario_db = {}
    else:
        inventario_db = INVENTARIO_INICIAL.copy()
        guardar_inventario()

    # 2. Cargar Ventas
    if os.path.exists(ARCHIVO_VENTAS):
        try:
            with open(ARCHIVO_VENTAS, "r", encoding="utf-8") as f:
                ventas_db = json.load(f)
        except:
            ventas_db = []
    else:
        ventas_db = []

    # 3. Cargar Clientes
    if os.path.exists(ARCHIVO_CLIENTES):
        try:
            with open(ARCHIVO_CLIENTES, "r", encoding="utf-8") as f:
                clientes_db = json.load(f)
        except:
            clientes_db = {}
    else:
        clientes_db = {}

    # 4. Cargar Usuarios
    if os.path.exists(ARCHIVO_USUARIOS):
        try:
            with open(ARCHIVO_USUARIOS, "r", encoding="utf-8") as f:
                usuarios_db = json.load(f)

                # Migración automática de permisos (Tu lógica original)
                guardar = False
                for u, data in usuarios_db.items():
                    if "permisos" not in data:
                        rol_viejo = data.get("rol", "Cajero")
                        if rol_viejo in ROLES_PLANTILLA:
                            data["permisos"] = ROLES_PLANTILLA[rol_viejo]
                        else:
                            data["permisos"] = ROLES_PLANTILLA["Cajero"]
                        guardar = True
                if guardar:
                    guardar_usuarios()
        except:
            usuarios_db = {}
    else:
        # Admin por defecto
        print(">> Creando Admin inicial...")
        usuarios_db = {
            "admin": {
                "pass_hash": "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3",
                "rol": "Administrador",
                "permisos": ROLES_PLANTILLA["Administrador"],
            }
        }
        guardar_usuarios()


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
