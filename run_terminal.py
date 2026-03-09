# run_terminal.py
from core import datos
import cli.operaciones as ops
import cli.menus as menus


def ejecutar_sistema():
    # Carga inicial de datos en memoria (Inventario, Empleados, Movimientos)
    datos.cargar_datos_sistema()
    USUARIO_ACTUAL = None

    # Bucle infinito para mantener el sistema vivo
    while True:
        if USUARIO_ACTUAL is None:
            # --- ZONA PÚBLICA (NO LOGUEADO) ---
            op = menus.mostrar_menu_inicio_sesion()

            if op == "1":
                # Paso 2: Inicio de sesión
                USUARIO_ACTUAL = ops.flujo_login()
            elif op == "2":
                ops.recuperar_acceso()
                input("\n[Presione ENTER para continuar...]")
            elif op == "3":
                # Paso 7: Salida del sistema de forma segura
                print("👋 Cerrando el Sistema de Control de Inventarios...")
                break
            else:
                print("❌ Opción inválida.")

        else:
            # --- ZONA PRIVADA (LOGUEADO) ---
            # Obtenemos los datos del usuario actual para validar permisos
            user_data = datos.usuarios_db.get(USUARIO_ACTUAL, {})
            rol_str = user_data.get("rol", "Desconocido")
            es_admin = "ADMIN" in user_data.get("permisos", [])

            # Calculamos las alertas de stock antes de mostrar el menú
            alertas_actuales = ops.obtener_alertas_stock()

            # Paso 3: Menú principal
            op_main = menus.mostrar_menu_principal(
                USUARIO_ACTUAL, rol_str, alertas_actuales
            )

            # --- RUTEADOR DE OPCIONES ---
            if op_main == "1":
                # Paso 5: Consulta de inventario
                ops.consultar_inventario()

            elif op_main == "2":
                # Módulo de Mantenimiento (CRUD)
                sub_op = menus.menu_mantenimiento()
                if sub_op == "1":
                    # Paso 4: Registro de productos
                    ops.registrar_producto()
                elif sub_op == "2":
                    ops.editar_producto()
                elif sub_op == "3":
                    if es_admin:
                        ops.eliminar_producto()
                    else:
                        print("⛔ Solo el Administrador puede eliminar productos.")

            elif op_main == "3":
                # Paso 6: Entrada y salida de productos para mantener el stock actualizado
                sub_op = menus.menu_movimientos()
                if sub_op == "1":
                    ops.registrar_movimiento(USUARIO_ACTUAL, "ENTRADA")
                elif sub_op == "2":
                    ops.registrar_movimiento(USUARIO_ACTUAL, "SALIDA")

            elif op_main == "4":
                # Gestión de Personal
                if es_admin:
                    sub_op = menus.menu_personal()
                    if sub_op == "1":
                        ops.registrar_empleado()
                    elif sub_op == "2":
                        ops.gestionar_estado_empleado()
                    elif sub_op == "3":
                        ops.eliminar_empleado()
                else:
                    print("⛔ Acceso denegado. Se requiere rol de Administrador.")

            elif op_main == "5":
                print(f"👋 Sesión cerrada exitosamente para: {USUARIO_ACTUAL}")
                USUARIO_ACTUAL = None  # Regresa al Menú de Inicio (Público)

            else:
                print("❌ Opción no reconocida.")

            # Pausa dramática para que el usuario pueda leer los resultados antes de limpiar pantalla
            if op_main in ["1", "2", "3", "4"]:
                input("\n[Presione ENTER para continuar...]")


if __name__ == "__main__":
    ejecutar_sistema()
