import os
import json
from . import config


import os
import json
from . import config


def correr_scanner_hades():
    print("\n" + "=" * 50)
    print("🩺 HADES HEALTH CHECK & AUTO-PATCH (V-1.7.4)")
    print("=" * 50)

    errores = 0
    # 1. VERIFICAR CARPETAS (Igual que antes)
    carpetas = [
        config.DB_DIR,
        config.ASSETS_DIR,
        config.DIR_VENTAS_DIARIAS,
        config.CARPETA_FACTURAS,
        config.CARPETA_REPORTES,
        config.CARPETA_QR,
    ]

    for c in carpetas:
        if not os.path.exists(c):
            os.makedirs(c)
            print(f"⚠️  [FIX] Carpeta creada: {os.path.basename(c)}")

    # 2. VERIFICAR FINANZAS (El nuevo archivo de capital)
    if not os.path.exists(config.ARCHIVO_FINANZAS):
        capital_inicial = {"capital_disponible": 500.0, "moneda": "USD"}
        with open(config.ARCHIVO_FINANZAS, "w") as f:
            json.dump(capital_inicial, f, indent=4)
        print("✅ [NEW] Archivo de Finanzas inicializado ($500.00).")

    # 3. AUTO-PARCHEO DE INVENTARIO (HARDENING DE DATOS)
    if os.path.exists(config.ARCHIVO_DATOS):
        try:
            with open(config.ARCHIVO_DATOS, "r", encoding="utf-8") as f:
                inventario = json.load(f)

            modificado = False
            for ref, item in inventario.items():
                # Si falta 'costo', calculamos uno base (60% del precio)
                if "costo" not in item:
                    item["costo"] = round(item["precio"] * 0.60, 2)
                    modificado = True
                # Si falta 'stock_minimo', ponemos 5 por defecto
                if "stock_minimo" not in item:
                    item["stock_minimo"] = 5
                    modificado = True

            if modificado:
                with open(config.ARCHIVO_DATOS, "w", encoding="utf-8") as f:
                    json.dump(inventario, f, indent=4)
                print("✨ [PATCH] Inventario actualizado con campos de Analítica.")
            else:
                print("✅ [OK] Estructura de Inventario íntegra.")
        except:
            print("🔥 [CRÍTICO] No se pudo leer el Inventario para parchar.")
            errores += 1

    print("=" * 50)
    return errores == 0


def verificar_integridad_inventario(inventario):
    """
    Asegura que cada producto tenga los campos necesarios para la V-1.7.4
    """
    cambios = False
    for ref, datos in inventario.items():
        # Si no tiene costo, le ponemos el 60% del precio de venta por defecto
        if "costo" not in datos:
            datos["costo"] = round(datos["precio"] * 0.60, 2)
            cambios = True
        # Si no tiene stock_minimo, ponemos 5 por defecto
        if "stock_minimo" not in datos:
            datos["stock_minimo"] = 5
            cambios = True

    return cambios

    print("=" * 40)
    if errores > 0:
        print(f"🚨 ESCANEO FINALIZADO: {errores} errores críticos encontrados.")
        print("El sistema podría fallar. Revise los archivos JSON.")
    else:
        print(f"✨ SISTEMA SALUDABLE: {advertencias} ajustes menores realizados.")
    print("=" * 40 + "\n")

    return errores == 0  # Retorna True si puede continuar
