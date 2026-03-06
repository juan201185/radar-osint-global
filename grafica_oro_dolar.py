import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

# 1. Definir los activos
tickers_dict = {
    "GLD": "Oro (ETF)",
    "DX-Y.NYB": "Indice Dolar (DXY)",
    "^GSPC": "S&P 500"
}

# 2. Descargar datos
print("Descargando datos desde 2008...")
raw_data = yf.download(list(tickers_dict.keys()), start="2008-01-01")

# 3. Extraer precios de forma segura
if 'Adj Close' in raw_data.columns:
    data = raw_data['Adj Close']
else:
    data = raw_data['Close']

# 4. Limpiar y normalizar a base 100
data = data.dropna()
data_norm = (data / data.iloc[0]) * 100

# 5. Configurar el gráfico (sin abrir ventana)
plt.figure(figsize=(12, 6))
colors = {'GLD': '#D4AF37', 'DX-Y.NYB': '#1f77b4', '^GSPC': '#2ca02c'}

for ticker in data_norm.columns:
    plt.plot(data_norm.index, data_norm[ticker], 
             label=tickers_dict.get(ticker, ticker), 
             color=colors.get(ticker), 
             linewidth=2)

plt.title('Comparativa: Oro, Dolar y S&P 500 (Base 100 - Inicio 2008)', fontsize=14)
plt.ylabel('Crecimiento Relativo (%)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.axhline(100, color='black', lw=1)

# 6. GUARDAR EL ARCHIVO
nombre_archivo = "comparativa_mercados.png"
plt.savefig(nombre_archivo, dpi=300) # dpi=300 para alta calidad
print(f"¡Exito! La grafica se ha guardado como: {nombre_archivo}")