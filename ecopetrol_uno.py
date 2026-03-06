import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

# 1. DESCARGA Y PREPARACIÓN DE DATOS DE MERCADO
print("Descargando datos de mercado...")
# EC (Ecopetrol) y CL=F (Petróleo WTI como referencia estable)
tickers = ["EC", "CL=F"]
raw_data = yf.download(tickers, start="2002-08-07")

# Selección robusta de precios de cierre
if 'Adj Close' in raw_data.columns.get_level_values(0):
    data = raw_data['Adj Close'].copy()
else:
    data = raw_data['Close'].copy()

data = data.rename(columns={'CL=F': 'Petroleo', 'EC': 'Accion_EC'}).dropna()

# 2. DATOS HISTÓRICOS (Utilidades y Producción)
# Basado en reportes integrados de gestión de Ecopetrol
historia = {
    'Año': [2002, 2004, 2006, 2008, 2010, 2012, 2014, 2016, 2018, 2020, 2022, 2023, 2024, 2025],
    'Utilidad_Billones': [1.2, 2.5, 3.4, 11.6, 8.3, 15.0, 5.7, 1.6, 11.6, 1.7, 33.4, 19.1, 15.5, 12.0],
    'Produccion_KBPD': [450, 480, 520, 550, 615, 750, 755, 718, 720, 697, 709, 737, 741, 735]
}
df_h = pd.DataFrame(historia)

# Función para sombrear gobiernos
def sombrear_gobiernos(ax, es_fecha=True):
    periodos = [
        (2002, 2010, 'Uribe', '#ffeecc'),
        (2010, 2018, 'Santos', '#ccffcc'),
        (2018, 2022, 'Duque', '#cceeff'),
        (2022, 2026, 'Petro', '#ffcccc')
    ]
    for start, end, name, col in periodos:
        if es_fecha:
            inicio, fin = pd.to_datetime(f"{start}-01-01"), pd.to_datetime(f"{end}-12-31")
        else:
            inicio, fin = start, end
        ax.axvspan(inicio, fin, color=col, alpha=0.3, zorder=0)
        ax.text(start + (end-start)/2, ax.get_ylim()[1]*0.95, name, ha='center', fontsize=8, fontweight='bold')

# --- ARCHIVO 1: ACCIÓN VS PETRÓLEO ---
plt.figure(figsize=(10, 5))
ax1 = plt.gca()
ax1.plot(data.index, data['Petroleo'], color='gray', alpha=0.5, label='Petróleo (USD)')
ax1_twin = ax1.twinx()
ax1_twin.plot(data.index, data['Accion_EC'], color='green', label='Acción Ecopetrol (USD)')
ax1.set_title('Gráfica 1: Valor de Mercado vs Petróleo')
sombrear_gobiernos(ax1)
plt.savefig("1_mercado_ecopetrol.png")
print("Archivo 1 guardado.")

# --- ARCHIVO 2: UTILIDADES (GANANCIAS) ---
plt.figure(figsize=(10, 5))
plt.bar(df_h['Año'], df_h['Utilidad_Billones'], color='gold', edgecolor='black', zorder=3)
plt.title('Gráfica 2: Utilidad Neta Anual (Billones COP)')
plt.ylabel('Billones de Pesos')
sombrear_gobiernos(plt.gca(), es_fecha=False)
plt.savefig("2_utilidades_ecopetrol.png")
print("Archivo 2 guardado.")

# --- ARCHIVO 3: PRODUCCIÓN PETROLERA ---
plt.figure(figsize=(10, 5))
plt.plot(df_h['Año'], df_h['Produccion_KBPD'], color='blue', marker='o', linewidth=2)
plt.fill_between(df_h['Año'], df_h['Produccion_KBPD'], color='blue', alpha=0.1)
plt.title('Gráfica 3: Producción Diaria (Miles de Barriles Equivalentes - KBPD)')
plt.ylabel('KBPD')
sombrear_gobiernos(plt.gca(), es_fecha=False)
plt.savefig("3_produccion_ecopetrol.png")
print("Archivo 3 guardado.")