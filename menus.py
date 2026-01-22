# menus.py
from utils import limpiar_pantalla
from datos import PERMISOS_DISPONIBLES, ROLES_PLANTILLA


def mostrar_menu_principal(usuario, rol):
    """Muestra el menú principal y retorna la opción."""
    limpiar_pantalla()
    print("=" * 50)
    print(f"   SISTEMA HADES - TERMINAL (V-1.6.4)")
    print(f"   Usuario: {usuario} | Rol: {rol}")
    print("=" * 50)

    print("\n[ ADMINISTRACIÓN ]")
    print("1. Registrar Producto")
    print("2. Editar Producto")
    print("3. Eliminar Producto")
    print("4. Regenerar QRs")
    print("5. Gestión de Personal (Usuarios) 👮")

    print("\n[ OPERACIÓN ]")
    print("6. Movimientos Stock (Entrada/Salida)")
    print("7. Consultar Inventario")
    print("8. Registrar Venta (Caja) 🛒")
    print("9. Reportes y Cierre de Caja 📉")
    print("10. Gestión de Clientes 👥")
    # ...
    print("\n11. Salir")

    return input("\n>> Seleccione opción: ")


def menu_reportes():
    limpiar_pantalla()
    print("--- 📊 REPORTES Y CIERRE ---")
    print("1. Ver Historial Completo de Ventas")
    print("2. 📅 Realizar CIERRE DE CAJA (Hoy)")
    print("3. Volver")
    return input("\n>> Seleccione: ")


def menu_gestion_clientes():
    while True:
        limpiar_pantalla()
        print("--- 👥 GESTIÓN DE CLIENTES ---")
        print("1. Registrar Cliente")
        print("2. Listar Clientes")
        print("3. Buscar Cliente (Detalles)")
        print("4. Volver")
        op = input("\n>> Seleccione: ")

        # Importamos aquí para evitar 'circular import'
        import operaciones as ops

        if op == "1":
            ops.registrar_cliente_interactivo()
        elif op == "2":
            ops.listar_clientes()
        elif op == "3":
            ops.buscar_cliente_pro()
        elif op == "4":
            break

        input("\nPresione [ENTER] para continuar...")


def menu_gestion_usuarios():
    limpiar_pantalla()
    print("--- 👮 GESTIÓN DE PERSONAL ---")
    print("1. Crear Nuevo Usuario")
    print("2. Listar Personal")
    print("3. Eliminar Usuario")
    print("4. Modificar Permisos (Avanzado) 🔧")
    print("5. Editar Datos (Nombre/Clave/Rol) ✏️")
    print("6. Volver")
    return input("\n>> Seleccione: ")


def menu_editar_campo_usuario(usuario):
    """Sub-menú para elegir qué dato cambiar."""
    print(f"\n--- ✏️ EDITANDO A: {usuario} ---")
    print("1. Cambiar Nombre de Usuario (Login)")
    print("2. Cambiar Contraseña")
    print("3. Cambiar Rol (Resetea permisos)")
    print("4. Volver")
    return input(">> ¿Qué desea modificar?: ")


def menu_seleccion_rol():
    """Muestra los roles disponibles y retorna la elección."""
    print("\n--- SELECCIÓN DE ROL ---")
    print("1. Administrador (Control Total)")
    print("2. Cajero (Ventas + Clientes)")
    print("3. Bodeguero (Stock + Productos)")
    print("4. Supervisor (Gestión sin Admin)")
    print("5. 🔧 PERSONALIZADO (Elegir permisos manualmente)")
    return input(">> Seleccione Rol: ")


def interfaz_modificar_permisos(usuario, rol_actual, permisos_actuales):
    """
    Interfaz interactiva para activar/desactivar permisos.
    Retorna la nueva lista de permisos.
    """
    limpiar_pantalla()
    print(f"🔧 EDITANDO PERMISOS DE: {usuario}")
    print(f"   Rol actual: {rol_actual}")
    print("-" * 50)
    print("Instrucciones: Escribe 'S' para activar, 'N' para desactivar.")
    print("               Presiona [ENTER] para dejarlo como está.")
    print("-" * 50)

    nuevos_permisos = []

    for clave, descripcion in PERMISOS_DISPONIBLES.items():
        tiene = clave in permisos_actuales
        estado_icon = "✅ SI" if tiene else "❌ NO"

        resp = input(
            f"   [{estado_icon}] {clave} ({descripcion}) -> Nuevo estado? "
        ).upper()

        if resp == "S":
            nuevos_permisos.append(clave)
        elif resp == "N":
            pass  # No lo agrega
        else:
            # Si da enter, mantiene el estado original
            if tiene:
                nuevos_permisos.append(clave)

    return nuevos_permisos


def menu_seleccion_factura():
    """Menú dentro de la caja para elegir cliente."""
    print("\n--- 👤 DATOS DE FACTURACIÓN ---")
    print("1. Consumidor Final")
    print("2. Cliente Ya Registrado (Buscar por Cédula)")
    print("3. Registrar Nuevo Cliente Ahora Mismo")
    return input("Seleccione opción (1-3): ").strip()
