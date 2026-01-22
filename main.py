# main.py
from datos import cargar_datos_sistema
import operaciones as ops
import menus

# Variable global de sesión
USUARIO_ACTUAL = None


def verificar(permiso):
    """Verifica si el usuario logueado tiene la llave."""
    if ops.tiene_permiso(USUARIO_ACTUAL, permiso):
        return True
    else:
        print(f"⛔ ACCESO DENEGADO. Requiere permiso: {permiso}")
        return False


def ejecutar_sistema():
    global USUARIO_ACTUAL
    cargar_datos_sistema()

    # 1. Login
    USUARIO_ACTUAL = ops.login()

    while True:
        # Recuperamos el rol para mostrarlo bonito
        rol_str = "Desconocido"
        if USUARIO_ACTUAL in ops.datos.usuarios_db:
            rol_str = ops.datos.usuarios_db[USUARIO_ACTUAL]["rol"]

        # 2. Mostrar Menú Principal
        op = menus.mostrar_menu_principal(USUARIO_ACTUAL, rol_str)

        # --- LÓGICA DE NAVEGACIÓN Y PERMISOS ---

        # [1-4] PRODUCTOS
        if op in ["1", "2", "3", "4"]:
            if verificar("PROD"):
                if op == "1":
                    ops.registrar_producto()
                elif op == "2":
                    ops.editar_producto()
                elif op == "3":
                    ops.eliminar_producto()
                elif op == "4":
                    ops.regenerar_qr_manualmente()

        # [5] GESTIÓN DE PERSONAL
        elif op == "5":
            if verificar("ADMIN"):
                while True:
                    sub_op = menus.menu_gestion_usuarios()

                    if sub_op == "1":
                        ops.registrar_nuevo_usuario()
                    elif sub_op == "2":
                        ops.listar_usuarios()
                    elif sub_op == "3":
                        ops.eliminar_usuario(USUARIO_ACTUAL)
                    elif sub_op == "4":
                        ops.modificar_permisos_usuario(USUARIO_ACTUAL)
                    elif sub_op == "5":
                        ops.editar_datos_usuario(USUARIO_ACTUAL)  # <--- ¡AQUÍ ESTÁ!
                    elif sub_op == "6":
                        break  # Ahora salir es la 6

                    if sub_op != "6":
                        input("\nPresione [ENTER] para continuar...")

        # [6] MOVIMIENTOS
        elif op == "6":
            if verificar("STOCK"):
                ops.registrar_movimiento()

        # [7] INVENTARIO
        elif op == "7":
            if ops.tiene_permiso(USUARIO_ACTUAL, "VENTAS") or ops.tiene_permiso(
                USUARIO_ACTUAL, "STOCK"
            ):
                ops.consultar_inventario()
            else:
                print("⛔ No tienes acceso al inventario.")

        # [8] CAJA
        elif op == "8":
            if verificar("VENTAS"):
                ops.registrar_venta()

        # [9] REPORTES Y CIERRE (Requiere permiso REPORTES)
        elif op == "9":
            if verificar("REPORTES"):
                while True:
                    sub = menus.menu_reportes()
                    if sub == "1":
                        ops.consultar_historial_ventas()
                        input("Enter para volver...")
                    elif sub == "2":
                        ops.realizar_cierre_caja()
                        input("Enter para volver...")
                    elif sub == "3":
                        break

        # [10] CLIENTES
        elif op == "10":
            if verificar("CLIENTES"):
                menus.menu_gestion_clientes()

        elif op == "11":
            print("👋 ¡Hasta luego!")
            break

        else:
            print("⚠️ Opción no válida.")

        print("\n" + "-" * 40)
        input("Presione [ENTER] para continuar...")


if __name__ == "__main__":
    ejecutar_sistema()
