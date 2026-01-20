from datos import cargar_datos_sistema
from utils import limpiar_pantalla
import operaciones as ops


def menu_principal():
    cargar_datos_sistema()
    rol = ops.login()

    while True:
        limpiar_pantalla()
        print("=" * 40)
        print(f"   SISTEMA HADES - TERMINAL (V-1.6.0)")
        print(f"   Usuario: {rol}")
        print("=" * 40)

        print("\n[ ADMINISTRACIÓN ]")
        print("1. Registrar Producto")
        print("2. Editar Producto")
        print("3. Eliminar Producto")
        print("4. Regenerar QRs")
        print("\n[ OPERACIÓN ]")
        print("5. Movimientos Stock (Entrada/Salida)")
        print("6. Consultar Inventario")
        print("7. Registrar Venta (Caja) 🛒")
        print("8. Historial de Ventas 📊")
        print("\n9. Salir")

        op = input("\n>> Seleccione opción: ")

        if op in ["1", "2", "3", "4"]:
            if rol == "Administrador":
                if op == "1":
                    ops.registrar_producto()
                elif op == "2":
                    ops.editar_producto()
                elif op == "3":
                    ops.eliminar_producto()
                elif op == "4":
                    ops.regenerar_qr_manualmente()
            else:
                print("⛔ Acceso denegado (Requiere Admin).")

        elif op == "5":
            ops.registrar_movimiento()
        elif op == "6":
            ops.consultar_inventario()
        elif op == "7":
            ops.registrar_venta()
        elif op == "8":
            ops.consultar_historial_ventas()
        elif op == "9":
            print("\n👋 ¡Hasta luego!")
            break
        else:
            print("⚠️ Opción no válida.")

        print("\n" + "-" * 40)
        input("Presione [ENTER] para volver al menú...")


if __name__ == "__main__":
    menu_principal()
