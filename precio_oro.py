import yfinance as yf
import matplotlib.pyplot as plt

# 1. Configurar el ticker del Oro (ETF GLD)
ticker = "GLD"

# 2. Descargar los datos desde enero de 2008 hasta hoy
print("Descargando datos históricos del Oro...")
data = yf.download(ticker, start="2008-01-01")

# 3. Usar el precio de cierre ajustado
# Si no existe 'Adj Close', usamos 'Close'
columna_precio = 'Adj Close' if 'Adj Close' in data.columns else 'Close'
precios_oro = data[columna_precio]

# 4. Crear la gráfica
plt.figure(figsize=(12, 6))
plt.plot(precios_oro.index, precios_oro, color='#D4AF37', linewidth=2)

# Configuración visual
plt.title('Evolución del Precio del Oro (GLD) desde 2008', fontsize=14)
plt.xlabel('Año')
plt.ylabel('Precio en USD por Acción del ETF')
plt.grid(True, linestyle='--', alpha=0.6)

# 5. Guardar la imagen en tu carpeta de archivos de Linux
nombre_imagen = "precio_oro_historico.png"
plt.savefig(nombre_imagen, dpi=300)

print(f"--- Proceso completado ---")
print(f"Busca el archivo '{nombre_imagen}' en tu carpeta 'Archivos de Linux'.")