# cli/menus.py
import os


def limpiar_pantalla():
    """Limpia la consola dependiendo del sistema operativo."""
    os.system("cls" if os.name == "nt" else "clear")


# ==========================================
# MENÚS DE SEGURIDAD Y ACCESO
# ==========================================
def mostrar_menu_inicio_sesion():
    limpiar_pantalla()
    print("\n" + "═" * 45)
    print("       📦 SISTEMA DE CONTROL DE INVENTARIOS")
    print("═" * 45)
    print("  1. [🔐] Iniciar Sesión")
    print("  2. [🔑] Recuperar Acceso")
    print("  3. [❌] Salir del Sistema")
    print("═" * 45)
    return input(">> Seleccione una opción: ").strip()


def menu_fallo_intentos(reinicio_actual, max_reinicios):
    print(
        f"\n⚠️  Aviso: Múltiples intentos fallidos ({reinicio_actual}/{max_reinicios})"
    )
    print("  1. Olvidé mi contraseña (Recuperar)")
    print("  2. Reiniciar intentos")
    print("  3. Salir")
    return input(">> ¿Qué desea hacer?: ").strip()


# ==========================================
# MENÚ PRINCIPAL Y SUBMENÚS DE NAVEGACIÓN
# ==========================================
def mostrar_menu_principal(usuario, rol, alertas=0):
    limpiar_pantalla()
    print("\n" + "═" * 45)
    print(f" 🏢 PANEL CENTRAL | Usuario: {usuario} | Rol: {rol}")
    print("═" * 45)

    # Alerta visual si hay productos con stock bajo
    if alertas > 0:
        print(f" ⚠️  ATENCIÓN: TIENE {alertas} PRODUCTOS CON STOCK BAJO")
        print("─" * 45)

    print("  1. 🔍 Ver y Buscar Inventario")
    print("  2. 📦 Mantenimiento de Productos (CRUD)")
    print("  3. 🔄 Movimientos de Stock (Entradas/Salidas)")
    print("  4. 👥 Gestión de Personal")
    print("  5. 🚪 Cerrar Sesión")
    print("═" * 45)
    return input(">> Seleccione una opción: ").strip()


def menu_filtros_inventario():
    print("\n--- BÚSQUEDA DE INVENTARIO ---")
    print("  1. Ver todo el inventario general")
    print("  2. Buscar por Nombre")
    print("  3. Buscar por Código")
    print("  4. Buscar por Categoría")
    print("  5. Buscar por Marca")
    print("  6. Volver")
    return input(">> Opción: ").strip()


def menu_mantenimiento():
    print("\n--- MANTENIMIENTO DE PRODUCTOS ---")
    print("  1. Registrar nuevo producto")
    print("  2. Editar producto existente")
    print("  3. Eliminar producto")
    print("  4. Volver")
    return input(">> Opción: ").strip()


def menu_movimientos():
    print("\n--- MOVIMIENTOS DE STOCK ---")
    print("  1. Registrar Entrada (Ingreso de mercancía)")
    print("  2. Registrar Salida (Despacho/Merma)")
    print("  3. Volver")
    return input(">> Opción: ").strip()


def menu_personal():
    print("\n--- GESTIÓN DE PERSONAL ---")
    print("  1. Añadir nuevo empleado")
    print("  2. Bloquear / Desbloquear empleado")
    print("  3. Eliminar empleado (Baja definitiva)")
    print("  4. Volver")
    return input(">> Opción: ").strip()
