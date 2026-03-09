# cli/operaciones.py
import hashlib
import getpass
from datetime import datetime

# IMPORTACIÓN CORREGIDA: Ya no importamos ROLES_PLANTILLA, ahora usamos roles_db
from core.datos import (
    inventario_db,
    usuarios_db,
    movimientos_db,
    roles_db,
    guardar_inventario,
    guardar_empleados,
    guardar_movimientos,
    guardar_roles,
    bloquear_usuario,
)
from cli import menus

try:
    from core.utils import generar_qr_producto
except ImportError:

    def generar_qr_producto(codigo, texto):
        pass


# ==========================================
# 1. MÓDULO DE SEGURIDAD Y ACCESO
# ==========================================
def flujo_login():
    max_reinicios = 3
    reinicio = 0

    while reinicio < max_reinicios:
        user = input("Usuario: ").strip()
        if not user:
            print("⚠️ El usuario no puede quedar en blanco.")
            continue

        if user in usuarios_db and usuarios_db[user].get("bloqueado"):
            print("🚫 Cuenta bloqueada. Contacte al administrador.")
            return None

        intentos = 0
        while intentos < 3:
            pwd = getpass.getpass(f"Contraseña (Intento {intentos + 1}/3): ")
            h = hashlib.sha256(pwd.encode()).hexdigest()

            if user in usuarios_db and usuarios_db[user]["pass_hash"] == h:
                return user

            intentos += 1
            print("❌ Credenciales incorrectas.")

        reinicio += 1
        accion = menus.menu_fallo_intentos(reinicio, max_reinicios)

        if accion == "1":
            recuperar_acceso(user)
            return None
        elif accion == "2":
            if reinicio >= max_reinicios:
                print(
                    f"🛑 BLOQUEO DE SEGURIDAD: Excedió los {max_reinicios} reinicios permitidos."
                )
                bloquear_usuario(user)
                return None
            continue
        else:
            return None

    return None


def recuperar_acceso(user=None):
    print("\n--- RECUPERACIÓN DE CUENTA ---")
    if not user:
        user = input("Ingrese su usuario: ").strip()

    if user in usuarios_db:
        codigo = input("Ingrese su código único de recuperación: ").strip()
        if codigo == usuarios_db[user].get("codigo_recuperacion"):
            nueva_pwd = getpass.getpass("Nueva contraseña: ")
            usuarios_db[user]["pass_hash"] = hashlib.sha256(
                nueva_pwd.encode()
            ).hexdigest()
            print("✅ Contraseña actualizada. Inicie sesión nuevamente.")
            guardar_empleados()
            return
    print("❌ Datos incorrectos. Operación cancelada.")


def ver_mi_codigo_seguridad(usuario):
    """Permite al usuario logueado ver su propio código de recuperación."""
    print("\n--- MI CÓDIGO DE RECUPERACIÓN ---")
    pwd = getpass.getpass("Por seguridad, ingrese su contraseña actual: ")
    h = hashlib.sha256(pwd.encode()).hexdigest()

    if usuarios_db[usuario]["pass_hash"] == h:
        print(
            f"✅ Su código único es: {usuarios_db[usuario].get('codigo_recuperacion')}"
        )
        print("⚠️  Guárdelo en un lugar seguro.")
    else:
        print("❌ Contraseña incorrecta. Acceso denegado.")


# ==========================================
# 2. MÓDULO DE MANTENIMIENTO (CRUD PRODUCTOS)
# ==========================================
def registrar_producto():
    print("\n--- NUEVO PRODUCTO ---")
    codigo = input("Código (ej: PROD-001): ").strip().upper()
    if codigo in inventario_db:
        print("❌ El código ya existe.")
        return

    nombre = input("Nombre: ").strip()
    categoria = input("Categoría: ").strip()
    marca = input("Marca: ").strip()

    try:
        stock = int(input("Stock Inicial: "))
        if stock < 0:
            raise ValueError
        stock_min = int(input("Stock Mínimo Alerta: "))
    except ValueError:
        print("❌ Error: Ingrese valores numéricos positivos para el stock.")
        return

    inventario_db[codigo] = {
        "nombre": nombre,
        "categoria": categoria,
        "marca": marca,
        "stock": stock,
        "stock_minimo": stock_min,
    }
    guardar_inventario()
    generar_qr_producto(codigo, f"Código: {codigo}\nNombre: {nombre}\nMarca: {marca}")
    print("✅ Producto registrado y código QR generado.")


def editar_producto():
    print("\n--- EDITAR PRODUCTO ---")
    codigo = input("Código del producto a editar: ").strip().upper()
    if codigo not in inventario_db:
        print("❌ Producto no encontrado.")
        return

    p = inventario_db[codigo]
    print(f"Editando: {p['nombre']} (Presione ENTER para mantener el valor actual)")

    n_nombre = input(f"Nombre [{p['nombre']}]: ").strip()
    if n_nombre:
        p["nombre"] = n_nombre

    n_cat = input(f"Categoría [{p.get('categoria', '')}]: ").strip()
    if n_cat:
        p["categoria"] = n_cat

    n_marca = input(f"Marca [{p.get('marca', '')}]: ").strip()
    if n_marca:
        p["marca"] = n_marca

    try:
        n_min = input(f"Stock Mínimo [{p.get('stock_minimo', 5)}]: ").strip()
        if n_min:
            p["stock_minimo"] = int(n_min)
    except ValueError:
        print("❌ Valor inválido. No se actualizó el stock mínimo.")

    guardar_inventario()
    print("✅ Producto actualizado.")


def eliminar_producto():
    print("\n--- ELIMINAR PRODUCTO ---")
    codigo = input("Código del producto a eliminar: ").strip().upper()
    if codigo in inventario_db:
        if (
            input(
                f"¿Seguro que desea eliminar '{inventario_db[codigo]['nombre']}'? (S/N): "
            ).upper()
            == "S"
        ):
            del inventario_db[codigo]
            guardar_inventario()
            print("✅ Producto eliminado.")
    else:
        print("❌ Producto no encontrado.")


# ==========================================
# 3. MÓDULO DE INVENTARIO (CONSULTAS)
# ==========================================
def obtener_alertas_stock():
    return sum(
        1 for p in inventario_db.values() if p["stock"] <= p.get("stock_minimo", 5)
    )


def imprimir_tabla_inventario(diccionario_filtrado):
    if not diccionario_filtrado:
        print("📦 No se encontraron productos.")
        return

    print(
        f"\n{'CÓDIGO':<12} | {'NOMBRE':<20} | {'MARCA':<15} | {'CATEGORÍA':<15} | {'STOCK'}"
    )
    print("-" * 75)
    for c, p in diccionario_filtrado.items():
        alerta = "⚠️" if p["stock"] <= p.get("stock_minimo", 5) else ""
        print(
            f"{c:<12} | {p['nombre'][:19]:<20} | {p.get('marca', '')[:14]:<15} | {p.get('categoria', '')[:14]:<15} | {p['stock']} {alerta}"
        )


def consultar_inventario():
    opcion = menus.menu_filtros_inventario()

    if opcion == "1":
        imprimir_tabla_inventario(inventario_db)
    elif opcion in ["2", "3", "4", "5"]:
        termino = input("Ingrese el término de búsqueda: ").strip().lower()
        resultados = {}
        for cod, prod in inventario_db.items():
            if opcion == "2" and termino in prod["nombre"].lower():
                resultados[cod] = prod
            elif opcion == "3" and termino in cod.lower():
                resultados[cod] = prod
            elif opcion == "4" and termino in prod.get("categoria", "").lower():
                resultados[cod] = prod
            elif opcion == "5" and termino in prod.get("marca", "").lower():
                resultados[cod] = prod
        imprimir_tabla_inventario(resultados)


# ==========================================
# 4. MÓDULO DE MOVIMIENTOS DE STOCK (KARDEX)
# ==========================================
def registrar_movimiento(usuario, tipo_movimiento):
    print(f"\n--- REGISTRO DE {tipo_movimiento} ---")
    codigo = input("Código del producto: ").strip().upper()

    if codigo not in inventario_db:
        print("❌ Producto no encontrado.")
        return

    prod = inventario_db[codigo]
    print(f"📦 {prod['nombre']} | Stock actual: {prod['stock']}")

    try:
        cant = int(
            input(
                f"Cantidad a {'ingresar' if tipo_movimiento == 'ENTRADA' else 'retirar'}: "
            )
        )
        if cant <= 0:
            print("❌ La cantidad debe ser mayor a cero.")
            return

        if tipo_movimiento == "SALIDA" and cant > prod["stock"]:
            print(
                f"❌ ERROR LÓGICO: No puede retirar {cant} unidades. Solo hay {prod['stock']} disponibles."
            )
            return

    except ValueError:
        print("❌ Error: Ingrese un número entero.")
        return

    motivo = input("Motivo / Documento: ").strip() or "No especificado"

    if tipo_movimiento == "ENTRADA":
        prod["stock"] += cant
    else:
        prod["stock"] -= cant

    guardar_inventario()

    movimiento = {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "tipo": tipo_movimiento,
        "codigo_prod": codigo,
        "cantidad": cant,
        "usuario": usuario,
        "motivo": motivo,
    }
    movimientos_db.append(movimiento)
    guardar_movimientos()
    print(f"✅ Movimiento registrado. Nuevo stock: {prod['stock']}")


# ==========================================
# 5. MÓDULO DE RRHH Y ROLES (DINÁMICOS)
# ==========================================
def listar_personal():
    print(f"\n{'USUARIO':<15} | {'ROL':<15} | {'ESTADO':<15} | {'CÓDIGO RECUP.'}")
    print("-" * 65)
    for u, d in usuarios_db.items():
        estado = "🚫 BLOQUEADO" if d.get("bloqueado") else "✅ Activo"
        print(
            f"{u:<15} | {d.get('rol', 'N/A'):<15} | {estado:<15} | {d.get('codigo_recuperacion', 'N/A')}"
        )


def registrar_empleado():
    print("\n--- ALTA DE EMPLEADO ---")
    user = input("Nuevo usuario: ").strip()
    if user in usuarios_db:
        print("❌ El usuario ya existe.")
        return

    pwd = getpass.getpass("Contraseña: ")
    print(f"Roles disponibles: {', '.join(roles_db.keys())}")
    rol = input("Rol asignado: ").strip().capitalize()

    # CORRECCIÓN: Toma los permisos de la base de roles (por defecto Bodeguero si se equivoca)
    permisos = roles_db.get(rol, roles_db.get("Bodeguero", []))

    from core.datos import generar_codigo_recuperacion

    codigo_rec = generar_codigo_recuperacion()

    usuarios_db[user] = {
        "pass_hash": hashlib.sha256(pwd.encode()).hexdigest(),
        "rol": rol,
        "permisos": permisos,
        "bloqueado": False,
        "codigo_recuperacion": codigo_rec,
    }
    guardar_empleados()
    print(f"✅ Empleado registrado. Su código de recuperación es: {codigo_rec}")


def gestionar_estado_empleado():
    listar_personal()
    user = input("\nUsuario a gestionar: ").strip()
    if user in usuarios_db:
        if usuarios_db[user].get("bloqueado", False):
            if (
                input(f"El usuario está BLOQUEADO. ¿Desbloquear? (S/N): ").upper()
                == "S"
            ):
                from core.datos import desbloquear_usuario

                desbloquear_usuario(user)
                print("✅ Usuario reactivado.")
        else:
            if (
                input(f"El usuario está ACTIVO. ¿Forzar bloqueo? (S/N): ").upper()
                == "S"
            ):
                bloquear_usuario(user)
                print("🚫 Usuario bloqueado.")
    else:
        print("❌ Usuario no encontrado.")


def eliminar_empleado():
    listar_personal()
    user = input("\nUsuario a ELIMINAR definitivamente: ").strip()
    if user == "admin":
        print("⛔ No se puede eliminar al Administrador principal.")
        return

    if user in usuarios_db:
        if input(f"⚠️ ¿Seguro que desea borrar a '{user}'? (S/N): ").upper() == "S":
            del usuarios_db[user]
            guardar_empleados()
            print("✅ Empleado eliminado del sistema.")
    else:
        print("❌ Usuario no encontrado.")


# --- GESTIÓN DE ROLES ---
def listar_roles():
    print("\n--- ROLES DEL SISTEMA ---")
    for r, perms in roles_db.items():
        print(f"- {r}: {', '.join(perms)}")


def crear_rol():
    print("\n--- CREAR NUEVO ROL ---")
    nuevo_rol = input("Nombre del nuevo rol (ej. Supervisor): ").strip().capitalize()
    if nuevo_rol in roles_db:
        print("❌ Ese rol ya existe.")
        return

    print("Permisos válidos: ADMIN, PROD, STOCK, RRHH, MOVIMIENTOS, VER_STOCK")
    permisos_str = input("Ingrese los permisos separados por coma: ").strip().upper()
    permisos_lista = [p.strip() for p in permisos_str.split(",") if p.strip()]

    roles_db[nuevo_rol] = permisos_lista
    guardar_roles()
    print(f"✅ Rol '{nuevo_rol}' creado con éxito.")


def editar_rol():
    listar_roles()
    rol_editar = input("\nIngrese el nombre del rol a editar: ").strip().capitalize()
    if rol_editar not in roles_db:
        print("❌ El rol no existe.")
        return
    if rol_editar == "Administrador":
        print("⛔ No se pueden modificar los permisos del Administrador principal.")
        return

    print("Permisos válidos: ADMIN, PROD, STOCK, RRHH, MOVIMIENTOS, VER_STOCK")
    permisos_str = input("Nuevos permisos separados por coma: ").strip().upper()
    permisos_lista = [p.strip() for p in permisos_str.split(",") if p.strip()]

    roles_db[rol_editar] = permisos_lista
    guardar_roles()

    # Actualiza los permisos de todos los empleados que tengan este rol
    for u, datos in usuarios_db.items():
        if datos.get("rol") == rol_editar:
            datos["permisos"] = permisos_lista
    guardar_empleados()

    print(f"✅ Rol '{rol_editar}' y usuarios asociados actualizados.")


def flujo_generar_qr_unico():
    codigo = (
        input("Ingrese el código del producto para generar su QR: ").strip().upper()
    )
    if codigo in inventario_db:
        p = inventario_db[codigo]
        info = f"ID: {codigo}\nNombre: {p['nombre']}\nMarca: {p['marca']}\nCat: {p['categoria']}"
        ruta = generar_qr_producto(codigo, info)
        print(f"✅ QR generado con éxito en: {ruta}")
    else:
        print("❌ Producto no encontrado.")


def flujo_generar_qr_masivo():
    print(f"⌛ Generando QR para {len(inventario_db)} productos...")
    for codigo, p in inventario_db.items():
        info = f"ID: {codigo}\nNombre: {p['nombre']}\nMarca: {p['marca']}\nCat: {p['categoria']}"
        generar_qr_producto(codigo, info)
    print(f"✅ Se han generado {len(inventario_db)} códigos QR en la carpeta /qrcodes.")
