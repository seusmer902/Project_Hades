import sys
import json
import os
import qrcode
from datetime import datetime

# --- CONFIGURACIÓN ---
ARCHIVO_DATOS = "inventario.json"
CARPETA_QR = "codigos_qr"

# --- DATOS SEMILLA ---
INVENTARIO_INICIAL = {
    "PAP-001": {
        "nombre": "Cuaderno Universitario",
        "categoria": "Cuadernos",
        "precio": 1.50,
        "stock": 50,
    },
    "PAP-002": {
        "nombre": "Esfero Azul Bic",
        "categoria": "Escritura",
        "precio": 0.60,
        "stock": 200,
    },
    "PAP-003": {
        "nombre": "Resma Papel Bond A4",
        "categoria": "Papel",
        "precio": 4.50,
        "stock": 30,
    },
}

usuarios_db = {
    "admin": {"pass": "admin123", "rol": "Administrador"},
    "empleado": {"pass": "user123", "rol": "Empleado"},
}

inventario_db = {}


# --- 1. PERSISTENCIA (GUARDAR/CARGAR) ---
def cargar_datos():
    global inventario_db
    if os.path.exists(ARCHIVO_DATOS):
        try:
            with open(ARCHIVO_DATOS, "r", encoding="utf-8") as f:
                inventario_db = json.load(f)
        except json.JSONDecodeError:
            inventario_db = {}
    else:
        print(">> Primera ejecución. Cargando datos iniciales...")
        inventario_db = INVENTARIO_INICIAL.copy()
        guardar_datos()


def guardar_datos():
    try:
        with open(ARCHIVO_DATOS, "w", encoding="utf-8") as f:
            json.dump(inventario_db, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error al guardar: {e}")


# --- 2. GENERADOR DE QR (LA IMPRESORA) ---
def generar_qr(nombre_archivo, info_contenido):
    """Crea la imagen QR en la carpeta."""
    if not os.path.exists(CARPETA_QR):
        os.makedirs(CARPETA_QR)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(info_contenido)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    ruta_completa = f"{CARPETA_QR}/{nombre_archivo}.png"
    img.save(ruta_completa)
    print(f">> QR generado con éxito en: {ruta_completa}")


# --- 3. FUNCIONES DEL SISTEMA ---
def login():
    print("\n--- SISTEMA DE INVENTARIO V-1.4.2 ---")
    intentos = 3
    while intentos > 0:
        usuario = input("Usuario: ")
        password = input("Contraseña: ")
        if usuario in usuarios_db and usuarios_db[usuario]["pass"] == password:
            return usuarios_db[usuario]["rol"]
        else:
            print("Credenciales incorrectas.")
            intentos -= 1
    sys.exit()


def registrar_producto():
    print("\n--- REGISTRO ---")
    codigo = input("Código (ej: PAP-001): ")
    if not codigo or codigo in inventario_db:
        print("Error: Código vacío o duplicado.")
        return

    nombre = input("Nombre: ")
    categoria = input("Categoría: ")
    try:
        precio = float(input("Precio: "))
        stock = int(input("Stock inicial: "))
    except ValueError:
        print("Error: Ingrese números válidos.")
        return

    inventario_db[codigo] = {
        "nombre": nombre,
        "categoria": categoria,
        "precio": precio,
        "stock": stock,
    }
    guardar_datos()

    # Generar QR Automático
    texto_qr = f"ID: {codigo}\nProducto: {nombre}\nPrecio: ${precio:.2f}"
    generar_qr(codigo, texto_qr)


def editar_producto():
    print("\n--- EDITAR ---")
    codigo = input("Código a editar: ")
    if codigo not in inventario_db:
        print("No existe.")
        return

    prod = inventario_db[codigo]
    print(f"Editando: {prod['nombre']} (Enter para mantener actual)")

    nuevo_nom = input(f"Nombre [{prod['nombre']}]: ")
    if nuevo_nom:
        prod["nombre"] = nuevo_nom

    nuevo_cat = input(f"Categoría [{prod['categoria']}]: ")
    if nuevo_cat:
        prod["categoria"] = nuevo_cat

    nuevo_pre = input(f"Precio [{prod['precio']}]: ")
    if nuevo_pre:
        prod["precio"] = float(nuevo_pre)

    guardar_datos()
    print("Actualizado correctamente.")


def eliminar_producto():
    codigo = input("\nCódigo a eliminar: ")
    if codigo in inventario_db:
        if input("¿Seguro? (SI/NO): ").upper() == "SI":
            del inventario_db[codigo]
            guardar_datos()
            print("Eliminado.")
    else:
        print("No existe.")


def regenerar_qr_manualmente():
    print("\n--- REGENERAR QRs ---")
    print("1. Uno solo")
    print("2. TODOS")
    opcion = input("Opción: ")

    if opcion == "1":
        codigo = input("Código: ")
        if codigo in inventario_db:
            p = inventario_db[codigo]
            texto = f"ID: {codigo}\nProducto: {p['nombre']}\nPrecio: ${p['precio']:.2f}"
            generar_qr(codigo, texto)
    elif opcion == "2":
        if input("¿Seguro? (SI/NO): ").upper() == "SI":
            contador = 0
            for codigo, p in inventario_db.items():
                texto = (
                    f"ID: {codigo}\nProducto: {p['nombre']}\nPrecio: ${p['precio']:.2f}"
                )
                generar_qr(codigo, texto)
                contador += 1
            print(f"Terminado. {contador} QRs generados.")


def registrar_movimiento():
    codigo = input("\nCódigo producto: ")
    if codigo not in inventario_db:
        print("No existe.")
        return

    tipo = input("Tipo (E=Entrada / S=Salida): ").upper()
    try:
        cant = int(input("Cantidad: "))
    except:
        return

    if tipo == "E":
        inventario_db[codigo]["stock"] += cant
        print(f"Nuevo stock: {inventario_db[codigo]['stock']}")
    elif tipo == "S":
        if cant <= inventario_db[codigo]["stock"]:
            inventario_db[codigo]["stock"] -= cant
            print(f"Nuevo stock: {inventario_db[codigo]['stock']}")
        else:
            print("Stock insuficiente.")
    guardar_datos()


def consultar_inventario():
    print("\n--- INVENTARIO ---")
    print(f"{'CODIGO':<10} | {'NOMBRE':<20} | {'STOCK':<5}")
    for c, d in inventario_db.items():
        print(f"{c:<10} | {d['nombre']:<20} | {d['stock']:<5}")


# --- MENÚ PRINCIPAL ---
def menu_principal():
    cargar_datos()
    rol = login()
    print(f"\n---- Bienvenido (V-1.4.2) ---- {rol}")

    while True:
        print("\n1. Registrar (Admin)")
        print("2. Editar (Admin)")
        print("3. Eliminar (Admin)")
        print("4. Regenerar QRs (Admin)")
        print("5. Movimientos (Entrada/Salida)")
        print("6. Consultar")
        print("7. Salir")

        op = input("Opción: ")

        if op in ["1", "2", "3", "4"]:
            if rol == "Administrador":
                if op == "1":
                    registrar_producto()
                if op == "2":
                    editar_producto()
                if op == "3":
                    eliminar_producto()
                if op == "4":
                    regenerar_qr_manualmente()
            else:
                print("Acceso denegado.")
        elif op == "5":
            registrar_movimiento()
        elif op == "6":
            consultar_inventario()
        elif op == "7":
            break


if __name__ == "__main__":
    menu_principal()
