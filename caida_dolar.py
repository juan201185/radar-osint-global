import yfinance as yf
import matplotlib.pyplot as plt

# Descargamos el DXY para el rango de fechas de tu imagen
df = yf.download("DX-Y.NYB", start="2026-01-20", end="2026-01-31")

plt.figure(figsize=(10, 5))
plt.plot(df['Close'], color='red', linewidth=2)
plt.title('Caida del Indice del Dolar (DXY) - Enero 2026')
plt.grid(True, alpha=0.3)
plt.ylabel('Puntos del Indice')

plt.savefig("caida_dolar_enero.png")
print("Grafica guardada como caida_dolar_enero.png")