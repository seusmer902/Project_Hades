# run_terminal.py
from core import datos
import cli.operaciones as ops
import cli.menus as menus


def ejecutar_sistema():
    datos.cargar_datos_sistema()
    USUARIO_ACTUAL = None

    while True:
        if USUARIO_ACTUAL is None:
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
            user_data = datos.usuarios_db.get(USUARIO_ACTUAL, {})
            rol_str = user_data.get("rol", "Desconocido")
            es_admin = "ADMIN" in user_data.get("permisos", [])
            alertas_actuales = ops.obtener_alertas_stock()

            op_main = menus.mostrar_menu_principal(
                USUARIO_ACTUAL, rol_str, alertas_actuales
            )

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
                elif sub_op == "4":
                    qr_op = menus.menu_qr()
                    if qr_op == "1":
                        ops.flujo_generar_qr_unico()
                    elif qr_op == "2":
                        ops.flujo_generar_qr_masivo()

            elif op_main == "3":
                sub_op = menus.menu_movimientos()
                if sub_op == "1":
                    ops.registrar_movimiento(USUARIO_ACTUAL, "ENTRADA")
                elif sub_op == "2":
                    ops.registrar_movimiento(USUARIO_ACTUAL, "SALIDA")
                elif sub_op == "3":
                    ops.escanear_qr_movimiento(USUARIO_ACTUAL)
                elif sub_op == "4":
                    # --- AQUÍ ESTÁ LA MAGIA DE LOS REPORTES ---
                    op_rep = menus.menu_reportes()
                    if op_rep == "1":
                        ops.generar_reporte_diario()
                    elif op_rep == "2":
                        ops.consultar_reporte_por_fecha()
                    elif op_rep == "3":
                        ops.ver_historial_completo()

            elif op_main == "4":
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

            if op_main in ["1", "2", "3", "4", "5"]:
                input("\n[Presione ENTER para continuar...]")


if __name__ == "__main__":
    ejecutar_sistema()
