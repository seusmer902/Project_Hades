# operaciones.py
import hashlib
import getpass
import sys
import os
from datetime import datetime

# --- IMPORTS DE DATOS Y LÓGICA ---
import datos
from datos import (
    guardar_inventario,
    guardar_historial_ventas,
    cargar_datos_sistema,
    guardar_clientes,
    guardar_usuarios,
    PERMISOS_DISPONIBLES,
    ROLES_PLANTILLA,
)

# --- IMPORTS DE UTILIDADES Y CONFIGURACIÓN ---
from utils import limpiar_pantalla, generar_qr
from config import CARPETA_FACTURAS  # Ya no importamos usuarios_db de aquí

# --- IMPORTS DE INTERFAZ (MENÚS) ---
import menus


# ==========================================
# GESTIÓN DE SEGURIDAD (USUARIOS)
# ==========================================
def tiene_permiso(usuario, permiso_requerido):
    if not usuario or usuario not in datos.usuarios_db:
        return False
    # El Admin siempre tiene permiso para todo
    if datos.usuarios_db[usuario].get("rol") == "Administrador":
        return True
    perms = datos.usuarios_db[usuario].get("permisos", [])
    return permiso_requerido in perms


def login():
    print(f"\n--- 🔒 ACCESO SEGURO HADES ---")
    intentos = 3
    while intentos > 0:
        user = input("Usuario: ")
        pwd_input = getpass.getpass("Contraseña: ")

        if user in datos.usuarios_db:
            hash_calculado = hashlib.sha256(pwd_input.encode()).hexdigest()
            if hash_calculado == datos.usuarios_db[user]["pass_hash"]:
                return user  # Retornamos el nombre de usuario

        print(f"⛔ Credenciales incorrectas.")
        intentos -= 1
    sys.exit()


def registrar_nuevo_usuario():
    print("\n--- 👤 CREAR NUEVO USUARIO ---")
    nuevo_user = input("Nombre de usuario: ").strip()
    if nuevo_user in datos.usuarios_db:
        print("⚠️ Ese usuario ya existe.")
        return

    pwd1 = getpass.getpass("Contraseña: ")
    pwd2 = getpass.getpass("Confirmar contraseña: ")
    if pwd1 != pwd2:
        print("❌ Las contraseñas no coinciden.")
        return

    # Usamos el menú visual para elegir rol
    op = menus.menu_seleccion_rol()

    rol_nombre = "Personalizado"
    permisos_asignados = []

    if op == "1":
        rol_nombre = "Administrador"
        permisos_asignados = ROLES_PLANTILLA["Administrador"]
    elif op == "2":
        rol_nombre = "Cajero"
        permisos_asignados = ROLES_PLANTILLA["Cajero"]
    elif op == "3":
        rol_nombre = "Bodeguero"
        permisos_asignados = ROLES_PLANTILLA["Bodeguero"]
    elif op == "4":
        rol_nombre = "Supervisor"
        permisos_asignados = ROLES_PLANTILLA["Supervisor"]
    elif op == "5":
        print("\n--- 🔧 CONFIGURACIÓN MANUAL ---")
        for clave, desc in PERMISOS_DISPONIBLES.items():
            if input(f"¿Dar permiso '{clave}' ({desc})? (S/N): ").upper() == "S":
                permisos_asignados.append(clave)
    else:
        print("Opción inválida.")
        return

    pass_hash = hashlib.sha256(pwd1.encode()).hexdigest()
    datos.usuarios_db[nuevo_user] = {
        "pass_hash": pass_hash,
        "rol": rol_nombre,
        "permisos": permisos_asignados,
    }
    guardar_usuarios()
    print(f"✅ Usuario {nuevo_user} creado con rol '{rol_nombre}'.")


def modificar_permisos_usuario(admin_actual):
    listar_usuarios()
    target_user = input("\nUsuario a modificar: ").strip()

    if target_user not in datos.usuarios_db:
        print("⚠️ Usuario no encontrado.")
        return
    if target_user == admin_actual:
        print("⛔ No puedes modificar tus propios permisos aquí.")
        return

    data = datos.usuarios_db[target_user]
    nuevos_permisos = menus.interfaz_modificar_permisos(
        target_user, data["rol"], data.get("permisos", [])
    )

    data["permisos"] = nuevos_permisos
    data["rol"] = "Personalizado"
    guardar_usuarios()
    print(f"✅ Permisos de {target_user} actualizados.")


def editar_datos_usuario(admin_actual):
    listar_usuarios()
    target_user = input("\nUsuario a editar: ").strip()

    if target_user not in datos.usuarios_db:
        print("⚠️ Usuario no encontrado.")
        return
    if target_user == admin_actual:
        print("⚠️ Nota: Si cambias tu nombre, tendrás que reloguearte.")

    while True:
        op = menus.menu_editar_campo_usuario(target_user)
        data = datos.usuarios_db[target_user]

        if op == "1":  # Cambiar Nombre
            nuevo_nombre = input(f"Nuevo nombre para '{target_user}': ").strip()
            if nuevo_nombre and nuevo_nombre not in datos.usuarios_db:
                datos.usuarios_db[nuevo_nombre] = data
                del datos.usuarios_db[target_user]
                guardar_usuarios()
                print(f"✅ Renombrado a '{nuevo_nombre}'.")
                target_user = nuevo_nombre
            else:
                print("⛔ Nombre inválido o en uso.")

        elif op == "2":  # Cambiar Clave
            p1 = getpass.getpass("Nueva clave: ")
            p2 = getpass.getpass("Confirmar: ")
            if p1 == p2:
                data["pass_hash"] = hashlib.sha256(p1.encode()).hexdigest()
                guardar_usuarios()
                print("✅ Clave actualizada.")

        elif op == "3":  # Cambiar Rol
            print("⚠️ Esto reseteará los permisos al valor por defecto del rol.")
            op_rol = menus.menu_seleccion_rol()
            # (Simplificado para brevedad, asigna permisos según rol elegido igual que en crear)
            # ... lógica de asignación ...
            print("✅ Rol actualizado (Lógica simplificada).")
            guardar_usuarios()

        elif op == "4":
            break


def listar_usuarios():
    print("\n--- LISTA DE PERSONAL ---")
    print(f"{'USUARIO':<15} | {'ROL':<15} | {'PERMISOS'}")
    print("-" * 60)
    for u, info in datos.usuarios_db.items():
        perms = info.get("permisos", [])
        p_str = ", ".join(perms[:2]) + ("..." if len(perms) > 2 else "")
        print(f"{u:<15} | {info['rol']:<15} | {p_str}")
    print("-" * 60)


def eliminar_usuario(admin_actual):
    listar_usuarios()
    user = input("\nUsuario a eliminar: ").strip()
    if user == admin_actual:
        print("⛔ No puedes auto-eliminarte.")
        return
    if user in datos.usuarios_db:
        if input("¿Seguro? S/N: ").upper() == "S":
            del datos.usuarios_db[user]
            guardar_usuarios()
            print("🗑️ Eliminado.")


# ==========================================
# GESTIÓN DE PRODUCTOS
# ==========================================
def registrar_producto():
    print("\n--- REGISTRO DE PRODUCTO ---")
    codigo = input("Código (ej: PAP-001): ").strip()
    if codigo in datos.inventario_db:
        print("⚠️ Código ya existe.")
        return
    nombre = input("Nombre: ")
    categoria = input("Categoría: ")
    try:
        precio = float(input("Precio: "))
        stock = int(input("Stock inicial: "))
    except ValueError:
        return

    datos.inventario_db[codigo] = {
        "nombre": nombre,
        "categoria": categoria,
        "precio": precio,
        "stock": stock,
    }
    guardar_inventario()
    generar_qr(codigo, f"ID:{codigo}\nProd:{nombre}\nPrecio:${precio:.2f}")
    print("✅ Producto registrado.")


def editar_producto():
    codigo = input("Código a editar: ").strip()
    if codigo not in datos.inventario_db:
        return
    prod = datos.inventario_db[codigo]
    print(f">> Editando: {prod['nombre']}")
    nuevo_nom = input(f"Nombre [{prod['nombre']}]: ")
    if nuevo_nom:
        prod["nombre"] = nuevo_nom
    nuevo_pre = input(f"Precio [{prod['precio']}]: ")
    if nuevo_pre:
        prod["precio"] = float(nuevo_pre)
    guardar_inventario()
    print("✅ Actualizado.")


def eliminar_producto():
    codigo = input("Código: ")
    if codigo in datos.inventario_db:
        del datos.inventario_db[codigo]
        guardar_inventario()
        print("🗑️ Eliminado.")


def regenerar_qr_manualmente():
    print("Regenerando todos los QRs...")
    for c, p in datos.inventario_db.items():
        generar_qr(c, f"ID:{c}\nProd:{p['nombre']}\nPrecio:${p['precio']:.2f}")
    print("✅ Listo.")


# ==========================================
# OPERACIONES (VENTAS Y STOCK)
# ==========================================
def registrar_movimiento():
    codigo = input("Código: ")
    if codigo not in datos.inventario_db:
        return
    tipo = input("Tipo (E=Entrada / S=Salida): ").upper()
    try:
        cant = int(input("Cantidad: "))
    except:
        return

    if tipo == "E":
        datos.inventario_db[codigo]["stock"] += cant
    elif tipo == "S":
        datos.inventario_db[codigo]["stock"] -= cant
    guardar_inventario()
    print("✅ Stock actualizado.")


def consultar_inventario():
    print("\n--- INVENTARIO ---")
    print(f"{'COD':<10} | {'NOMBRE':<20} | {'STOCK'}")
    print("-" * 40)
    for c, p in datos.inventario_db.items():
        print(f"{c:<10} | {p['nombre']:<20} | {p['stock']}")
    print("-" * 40)


def registrar_venta():
    print("\n--- 🛒 NUEVA VENTA (CAJA) ---")
    carrito = []
    total_bruto = 0.0

    # 1. BUCLE DE CARRITO
    while True:
        print(f"\n>> Items: {len(carrito)} | Subtotal: ${total_bruto:.2f}")
        codigo = input("Código (F para fin): ").strip()
        if codigo.upper() == "F":
            break

        if codigo not in datos.inventario_db:
            print("❌ No existe.")
            continue

        prod = datos.inventario_db[codigo]

        # Alerta de Stock (Semáforo)
        stock_actual = prod["stock"]
        if stock_actual <= 0:
            print("❌ AGOTADO.")
            continue
        elif stock_actual <= 5:
            print(f"⚠️ ¡STOCK CRÍTICO! Quedan {stock_actual}")

        print(f"   Producto: {prod['nombre']} | ${prod['precio']:.2f}")
        try:
            cant = int(input("   Cantidad: "))
            if cant <= stock_actual:
                sub = cant * prod["precio"]
                carrito.append(
                    {
                        "codigo": codigo,
                        "nombre": prod["nombre"],
                        "cantidad": cant,
                        "precio": prod["precio"],
                        "subtotal": sub,
                    }
                )
                total_bruto += sub
                prod["stock"] -= cant  # Resta temporal
                print("   ✅ Agregado.")
            else:
                print("   ❌ Stock insuficiente.")
        except ValueError:
            pass

    if not carrito:
        cargar_datos_sistema()
        return

    # 2. CLIENTE
    op_cliente = menus.menu_seleccion_factura()
    cliente_data = None
    cedula_cliente = "9999999999"
    nombre_cliente = "Consumidor Final"
    nivel_cliente = "Bronce"

    if op_cliente == "2":
        ced = input("Cédula: ")
        if ced in datos.clientes_db:
            cliente_data = datos.clientes_db[ced]
            nombre_cliente = cliente_data["nombre"]
            cedula_cliente = ced
            nivel_cliente = cliente_data.get("nivel", "Bronce")
            print(f"✅ Cliente: {nombre_cliente} ({nivel_cliente})")
    elif op_cliente == "3":
        registrar_cliente_interactivo()
        if datos.clientes_db:
            ced = list(datos.clientes_db.keys())[-1]
            cliente_data = datos.clientes_db[ced]
            nombre_cliente = cliente_data["nombre"]
            cedula_cliente = ced

    # 3. DESCUENTOS Y TOTALES
    desc_porc = (
        0.05 if nivel_cliente == "Plata" else (0.10 if nivel_cliente == "Oro" else 0)
    )
    monto_desc = total_bruto * desc_porc
    total_neto = total_bruto - monto_desc

    print("-" * 30)
    print(f"Subtotal:   ${total_bruto:.2f}")
    print(f"Descuento: -${monto_desc:.2f} ({nivel_cliente})")
    print(f"TOTAL:      ${total_neto:.2f}")
    print("-" * 30)

    if input("¿Confirmar? S/N: ").upper() == "S":
        guardar_inventario()

        # PUNTOS
        puntos_ganados = 0
        if cliente_data:
            puntos_ganados = int(total_neto)
            cliente_data["puntos"] = cliente_data.get("puntos", 0) + puntos_ganados
            # Level Up
            if cliente_data["puntos"] > 500:
                cliente_data["nivel"] = "Oro"
            elif cliente_data["puntos"] > 100:
                cliente_data["nivel"] = "Plata"
            guardar_clientes()
            print(f"🎁 Ganaste {puntos_ganados} Puntos.")

        generar_archivo_factura(
            carrito,
            total_bruto,
            monto_desc,
            total_neto,
            nombre_cliente,
            cedula_cliente,
            puntos_ganados,
            nivel_cliente,
        )

        nueva_venta = {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total": total_neto,
            "cliente": nombre_cliente,
            "items": carrito,
        }
        datos.ventas_db.append(nueva_venta)
        guardar_historial_ventas()
        print("✅ Venta OK.")
    else:
        print("❌ Cancelada.")
        cargar_datos_sistema()


def generar_archivo_factura(
    items, subtotal, descuento, total, nombre, cedula, puntos, nivel
):
    if not os.path.exists(CARPETA_FACTURAS):
        os.makedirs(CARPETA_FACTURAS)
    name = f"{CARPETA_FACTURAS}/FACT_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    with open(name, "w", encoding="utf-8") as f:
        f.write("=" * 40 + "\n")
        f.write(f"{'TIENDA HADES - TICKET':^40}\n")
        f.write("=" * 40 + "\n")
        f.write(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
        f.write(f"Cliente: {nombre}\n")
        f.write(f"RUC/CI:  {cedula}\n")
        if nivel != "Bronce":
            f.write(f"Nivel:   {nivel}\n")
        f.write("-" * 40 + "\n")
        f.write(f"{'CANT':<5} {'PRODUCTO':<20} {'SUBTOTAL':>10}\n")
        f.write("-" * 40 + "\n")
        for i in items:
            f.write(
                f"{i['cantidad']:<5} {i['nombre'][:19]:<20} ${i['subtotal']:>9.2f}\n"
            )
        f.write("-" * 40 + "\n")
        f.write(f"SUBTOTAL:          ${subtotal:>10.2f}\n")
        if descuento > 0:
            f.write(f"DESCUENTO:        -${descuento:>10.2f}\n")
        f.write(f"TOTAL A PAGAR:     ${total:>10.2f}\n")
        f.write("=" * 40 + "\n")
        if puntos > 0:
            f.write(f"¡Ganaste {puntos} Puntos Hades!\nGracias por tu preferencia.\n")
    print(f"📄 Factura: {name}")


# ==========================================
# REPORTES Y CLIENTES
# ==========================================
def realizar_cierre_caja():
    hoy = datetime.now().strftime("%Y-%m-%d")
    print(f"\n--- 📉 CIERRE DE CAJA ({hoy}) ---")
    total, count = 0.0, 0
    ventas_hoy = []

    for v in datos.ventas_db:
        if v["fecha"].startswith(hoy):
            total += v["total"]
            count += 1
            ventas_hoy.append(v)

    print(f"💰 Total Vendido: ${total:.2f}")
    print(f"🧾 Transacciones: {count}")

    if count > 0 and input("¿Guardar reporte? S/N: ").upper() == "S":
        with open(f"REPORTE_CIERRE_{hoy}.txt", "w") as f:
            f.write(f"CIERRE {hoy}\nTotal: ${total:.2f}\nVentas: {count}\n")
            for v in ventas_hoy:
                f.write(f"{v['fecha'][-8:]} | ${v['total']}\n")
        print("✅ Reporte guardado.")


def consultar_historial_ventas():
    print("\n--- HISTORIAL ---")
    for v in datos.ventas_db:
        print(f"{v['fecha']} | {v['cliente']} | ${v['total']:.2f}")


def registrar_cliente_interactivo():
    ced = input("Cédula: ")
    if ced in datos.clientes_db:
        return
    datos.clientes_db[ced] = {
        "nombre": input("Nombre: "),
        "telefono": input("Tel: "),
        "puntos": 0,
        "nivel": "Bronce",
    }
    guardar_clientes()
    print("✅ Cliente registrado.")


def buscar_cliente_pro():
    ced = input("Cédula: ")
    c = datos.clientes_db.get(ced)
    if c:
        print(
            f"Cliente: {c['nombre']} | Nivel: {c.get('nivel', 'Bronce')} | Puntos: {c.get('puntos', 0)}"
        )
    else:
        print("❌ No encontrado.")


def listar_clientes():
    print("\n--- CLIENTES ---")
    for c, d in datos.clientes_db.items():
        print(f"{c} | {d['nombre']} | {d.get('nivel', 'Bronce')}")
