import qrcode

# 1. La URL de tu sitio en PythonAnywhere
url_sitio = "http://juan85.pythonanywhere.com"

# 2. Configuración del diseño del QR
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L, # Nivel estándar de corrección
    box_size=10,
    border=4,
)

# 3. Cargar la URL
qr.add_data(url_sitio)
qr.make(fit=True)

# 4. Generar la imagen
# He puesto el fondo blanco y el código negro para máxima compatibilidad de escaneo
imagen = qr.make_image(fill_color="black", back_color="white")

# 5. Guardar en tu carpeta de Linux
nombre_archivo = "qr_juan85_pythonanywhere.png"
imagen.save(nombre_archivo)

print("-" * 30)
print(f"✅ ¡Listo, compadre!")
print(f"🔗 URL: {url_sitio}")
print(f"📁 Archivo: {nombre_archivo}")
print("-" * 30)