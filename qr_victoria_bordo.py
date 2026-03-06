import qrcode

# 1. La URL larga del blog
url_blog = "https://armerofuerzacauca.odoo.com/blog/noticias-2/el-grito-de-victoria-en-el-bordo-las-colonias-patianas-respaldan-a-victor-armero-16"

# 2. Configuración optimizada para URLs largas
qr = qrcode.QRCode(
    version=None, # fit=True calculará automáticamente el tamaño necesario
    error_correction=qrcode.constants.ERROR_CORRECT_M, # Nivel medio, ideal para URLs largas
    box_size=12,  # Aumentamos un poco el tamaño de los cuadros para mayor nitidez
    border=4,
)

# 3. Cargar los datos
qr.add_data(url_blog)
qr.make(fit=True)

# 4. Crear la imagen
# Usamos blanco y negro para asegurar que cualquier celular lo lea rápido
imagen = qr.make_image(fill_color="black", back_color="white")

# 5. Guardar con un nombre descriptivo
nombre_archivo = "qr_victoria_el_bordo.png"
imagen.save(nombre_archivo)

print("-" * 50)
print(f"✅ ¡QR Generado para la noticia de El Bordo!")
print(f"📁 Nombre del archivo: {nombre_archivo}")
print("-" * 50)