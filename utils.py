# utils.py
import os
import qrcode
from config import CARPETA_QR


def limpiar_pantalla():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def generar_qr(nombre_archivo, info_contenido):
    if not os.path.exists(CARPETA_QR):
        os.makedirs(CARPETA_QR)

    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(info_contenido)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    ruta = f"{CARPETA_QR}/{nombre_archivo}.png"
    img.save(ruta)
    print(f">> QR generado: {ruta}")
