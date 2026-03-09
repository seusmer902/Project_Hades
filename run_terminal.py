# run_terminal.py
from core import datos
import cli.operaciones as ops
import cli.menus as menus


def ejecutar_sistema():
    # Carga inicial de datos en memoria (Inventario, Empleados, Movimientos, Roles)
    datos.cargar_datos_sistema()
    USUARIO_ACTUAL = None

    while True:
        if USUARIO_ACTUAL is None:
            # --- ZONA PÚBLICA (NO LOGUEADO) ---
            op = menus.mostrar_menu_inicio_sesion()

            if op == "1":
                USUARIO_ACTUAL = ops.flujo_login()
            elif op == "2":
                ops.recuperar_acceso()
                input("\n[Presione ENTER para continuar...]")
            elif op == "3":
                print("👋 Cerrando el Sistema de Control de Inventarios...")
                break
            else:
                print("❌ Opción inválida.")

        else:
            # --- ZONA PRIVADA (LOGUEADO) ---
            user_data = datos.usuarios_db.get(USUARIO_ACTUAL, {})
            rol_str = user_data.get("rol", "Desconocido")
            es_admin = "ADMIN" in user_data.get("permisos", [])

            alertas_actuales = ops.obtener_alertas_stock()

            # Muestra el menú principal con las alertas en tiempo real
            op_main = menus.mostrar_menu_principal(
                USUARIO_ACTUAL, rol_str, alertas_actuales
            )

            # --- RUTEADOR DE OPCIONES ---
            if op_main == "1":
                ops.consultar_inventario()

            elif op_main == "2":
                sub_op = menus.menu_mantenimiento()
                if sub_op == "1":
                    ops.registrar_producto()
                elif sub_op == "2":
                    ops.editar_producto()
                elif sub_op == "3":
                    if es_admin:
                        ops.eliminar_producto()
                    else:
                        print("⛔ Solo el Administrador puede eliminar productos.")

            elif op_main == "3":
                sub_op = menus.menu_movimientos()
                if sub_op == "1":
                    ops.registrar_movimiento(USUARIO_ACTUAL, "ENTRADA")
                elif sub_op == "2":
                    ops.registrar_movimiento(USUARIO_ACTUAL, "SALIDA")

            elif op_main == "4":
                # Seguridad: Solo Admin o RRHH puede entrar aquí
                if es_admin or "RRHH" in user_data.get("permisos", []):
                    sub_op = menus.menu_personal()
                    if sub_op == "1":
                        ops.registrar_empleado()
                    elif sub_op == "2":
                        ops.gestionar_estado_empleado()
                    elif sub_op == "3":
                        ops.eliminar_empleado()
                    elif sub_op == "4":
                        rol_op = menus.menu_roles()
                        if rol_op == "1":
                            ops.listar_roles()
                        elif rol_op == "2":
                            ops.crear_rol()
                        elif rol_op == "3":
                            ops.editar_rol()
                else:
                    print("⛔ Acceso denegado. Se requiere rol de Administrador.")

            elif op_main == "5":
                ops.ver_mi_codigo_seguridad(USUARIO_ACTUAL)

            elif op_main == "6":
                print(f"👋 Sesión cerrada exitosamente para: {USUARIO_ACTUAL}")
                USUARIO_ACTUAL = None

            else:
                print("❌ Opción no reconocida.")

            # Pausa para que el usuario lea los resultados antes de limpiar la pantalla
            if op_main in ["1", "2", "3", "4", "5"]:
                input("\n[Presione ENTER para continuar...]")


if __name__ == "__main__":
    ejecutar_sistema()
