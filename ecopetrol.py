import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

# 1. Descarga de datos
print("Descargando datos... Por favor espera.")

# Probamos con el crudo ligero (CL=F) que es más estable en Yahoo que el Brent (BZ=F)
tickers = ["EC", "CL=F"] 
raw_data = yf.download(tickers, start="2002-08-07")

# Extraemos solo los precios de cierre
if 'Adj Close' in raw_data.columns.get_level_values(0):
    data = raw_data['Adj Close'].copy()
else:
    data = raw_data['Close'].copy()

# LIMPIEZA: Eliminamos filas vacías para que la gráfica no salga cortada
data = data.dropna()

# RENOMBRADO SEGURO: 
# En lugar de forzar nombres, mapeamos lo que realmente se descargó
nombres = {'CL=F': 'Petroleo_WTI', 'EC': 'Accion_Ecopetrol'}
data = data.rename(columns=nombres)

print(f"Datos descargados con éxito. Columnas detectadas: {list(data.columns)}")

# 2. Datos de Ganancias (Cifras oficiales de tendencia)
ganancias_data = {
    'Año': [2002, 2004, 2006, 2008, 2010, 2012, 2014, 2016, 2018, 2020, 2022, 2023, 2024, 2025],
    'Utilidad_Billones_COP': [1.2, 2.5, 3.4, 11.6, 8.3, 15.0, 5.7, 1.6, 11.6, 1.7, 33.4, 19.1, 15.5, 12.0]
}
df_ganancias = pd.DataFrame(ganancias_data)

# 3. Gráficas
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

# --- GRÁFICA 1: ACCIÓN VS PETRÓLEO ---
if 'Petroleo_WTI' in data.columns:
    ax1.plot(data.index, data['Petroleo_WTI'], color='black', alpha=0.3, label='Precio Petróleo (USD)')
    ax1.set_ylabel('Precio Petróleo (USD)')

ax1_twin = ax1.twinx()
if 'Accion_Ecopetrol' in data.columns:
    ax1_twin.plot(data.index, data['Accion_Ecopetrol'], color='green', linewidth=2, label='Acción Ecopetrol (USD)')
    ax1_twin.set_ylabel('Precio Acción EC (USD)')

ax1.set_title('Histórico: Ecopetrol vs. Mercado Petrolero')

# --- GRÁFICA 2: GANANCIAS ---
ax2.bar(df_ganancias['Año'], df_ganancias['Utilidad_Billones_COP'], color='gold', edgecolor='black', alpha=0.7)
ax2.set_title('Utilidad Neta Anual de Ecopetrol (Billones COP)')
ax2.set_ylabel('Billones COP')

# 4. Sombreado de Gobiernos
periodos = [
    (2002, 2010, 'Uribe', '#ffeecc'),
    (2010, 2018, 'Santos', '#ccffcc'),
    (2018, 2022, 'Duque', '#cceeff'),
    (2022, 2026, 'Petro', '#ffcccc')
]

for start, end, name, col in periodos:
    # Ajuste para el eje de fechas
    ax1.axvspan(pd.Timestamp(year=start, month=1, day=1), 
                pd.Timestamp(year=min(end, 2026), month=12, day=31), 
                color=col, alpha=0.3)
    # Ajuste para el eje de años (enteros)
    ax2.axvspan(start, end, color=col, alpha=0.3)

plt.tight_layout()
plt.savefig("ecopetrol_fix.png")
print("Proceso terminado. Busca el archivo 'ecopetrol_fix.png' en tu carpeta de Linux.")