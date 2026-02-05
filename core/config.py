import os

# --- RUTAS DINÁMICAS ---
ruta_actual = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(ruta_actual)

# Carpetas
DB_DIR = os.path.join(BASE_DIR, "db")
CARPETA_QR = os.path.join(BASE_DIR, "codigos_qr")
CARPETA_FACTURAS = os.path.join(BASE_DIR, "facturas")

# Archivos JSON
ARCHIVO_DATOS = os.path.join(DB_DIR, "inventario.json")
ARCHIVO_VENTAS = os.path.join(DB_DIR, "ventas.json")
ARCHIVO_CLIENTES = os.path.join(DB_DIR, "clientes.json")
ARCHIVO_USUARIOS = os.path.join(DB_DIR, "usuarios.json")
# NUEVO: Archivo para registros externos
ARCHIVO_PENDIENTES = os.path.join(DB_DIR, "usuarios_pendientes.json")

# Datos Semilla
INVENTARIO_INICIAL = {
    "PAP-001": {
        "nombre": "Cuaderno 100h",
        "categoria": "Cuadernos",
        "precio": 1.50,
        "stock": 50,
    },
    "PAP-002": {
        "nombre": "Esfero Azul",
        "categoria": "Escritura",
        "precio": 0.60,
        "stock": 200,
    },
}
