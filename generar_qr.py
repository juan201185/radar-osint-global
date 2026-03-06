import qrcode

# 1. La URL de destino
url_campana = "https://armerofuerzacauca.odoo.com/"

# 2. Configuración del QR
# version=1: Controla el tamaño (1 es el más pequeño, aumenta si hay muchos datos)
# box_size=10: Cuántos píxeles tiene cada "cuadrito" del QR
# border=4: El borde blanco obligatorio (estándar es 4)
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H, 
    box_size=10,
    border=4,
)

# 3. Agregar los datos
qr.add_data(url_campana)
qr.make(fit=True)

# 4. Crear la imagen (Colores estándar: Negro sobre Blanco)
# Si quisieras usar los colores del Partido Verde, podrías cambiar fill_color="green"
imagen = qr.make_image(fill_color="black", back_color="white")

# 5. Guardar el archivo
nombre_archivo = "qr_armero_fuerza_cauca.png"
imagen.save(nombre_archivo)

print(f"✅ ¡Éxito!")
print(f"🔗 URL procesada: {url_campana}")
print(f"📁 Código QR guardado como: {nombre_archivo}")