# config.py
import os

# Archivos de Datos
ARCHIVO_DATOS = "inventario.json"
ARCHIVO_VENTAS = "ventas.json"
ARCHIVO_CLIENTES = "clientes.json"
ARCHIVO_USUARIOS = "usuarios.json"

# Carpetas
CARPETA_QR = "codigos_qr"
CARPETA_FACTURAS = "facturas"

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
