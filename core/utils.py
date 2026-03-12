# core/utils.py
import qrcode
import os

QR_DIR = os.path.join("assets", "qrcodes")


def asegurar_carpeta_qr():
    """Crea la ruta completa si no existe."""
    if not os.path.exists(QR_DIR):
        os.makedirs(QR_DIR, exist_ok=True)


def generar_qr_producto(codigo, datos_str):
    """Genera un código QR individual y lo guarda en assets/qrcodes."""
    asegurar_carpeta_qr()

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=20,
        border=4,
    )
    qr.add_data(datos_str)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    ruta = os.path.join(QR_DIR, f"{codigo}.png")
    img.save(ruta)
    return ruta
