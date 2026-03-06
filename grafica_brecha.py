import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# -----------------------------------------------------------------------------
# 1. DATOS Y PROYECCIÓN MACROECONÓMICA
# -----------------------------------------------------------------------------
anios = list(range(1990, 2026))

# Datos base (Inflación y Crecimiento Real) para calcular el PIB Nominal año tras año
data_vars = {
    'Año': anios,
    'IPC': [26.12, 32.36, 26.82, 22.60, 22.59, 19.46, 21.63, 17.68, 16.70, 9.23,
            8.75, 7.65, 6.99, 6.49, 5.50, 4.85, 4.48, 5.69, 7.67, 2.00,
            3.17, 3.73, 2.44, 1.94, 3.66, 6.77, 5.75, 4.09, 3.18, 3.80,
            1.61, 5.62, 13.12, 9.28, 5.20, 3.60],
    'PIB_Real': [4.3, 2.4, 4.0, 5.0, 5.8, 5.2, 2.1, 3.4, 0.6, -4.2,
                 2.9, 1.7, 2.5, 3.9, 5.3, 4.7, 6.7, 6.9, 3.5, 1.7,
                 4.0, 6.6, 4.0, 4.3, 4.6, 3.1, 2.1, 1.4, 2.6, 3.2,
                 -7.0, 10.7, 7.3, 0.6, 1.8, 3.2],
    # Porcentaje del PIB que va al bolsillo de los trabajadores (Remuneración Asalariados)
    # Fuente estructural: En Colombia oscila entre 32% y 38%. El resto es Capital e Impuestos.
    'Share_Laboral': [0.38, 0.37, 0.37, 0.36, 0.36, 0.35, 0.35, 0.34, 0.34, 0.33,
                      0.33, 0.32, 0.32, 0.32, 0.31, 0.31, 0.31, 0.31, 0.32, 0.32,
                      0.33, 0.33, 0.33, 0.34, 0.34, 0.34, 0.34, 0.34, 0.34, 0.34,
                      0.33, 0.32, 0.31, 0.32, 0.33, 0.33] 
}

# CALCULO DE BILLONES DE PESOS (NOMINAL)
# Base aproximada 1990: PIB ~23.6 Billones
pib_actual = 23.6 
lista_pib = []
lista_capital = []
lista_trabajo = []

for i in range(len(anios)):
    # Crecimiento nominal = (1 + Inflación) * (1 + Crecimiento Real)
    factor = (1 + data_vars['IPC'][i]/100) * (1 + data_vars['PIB_Real'][i]/100)
    pib_actual = pib_actual * factor
    
    share_trabajo = data_vars['Share_Laboral'][i]
    # Share capital es el restante (simplificado: Excedente Bruto + Ingreso Mixto)
    share_capital = 1.0 - share_trabajo 
    
    lista_pib.append(pib_actual)
    lista_trabajo.append(pib_actual * share_trabajo)
    lista_capital.append(pib_actual * share_capital)

df = pd.DataFrame({
    'Año': anios,
    'PIB_Total': lista_pib,
    'Ganancia_Capital': lista_capital,
    'Ganancia_Trabajo': lista_trabajo
})

# -----------------------------------------------------------------------------
# 2. GRAFICAR (VISUALIZACIÓN REALISTA)
# -----------------------------------------------------------------------------
plt.figure(figsize=(14, 8))
plt.style.use('seaborn-v0_8-whitegrid')

# 1. PIB TOTAL (Línea Superior - El techo de la economía)
plt.plot(df['Año'], df['PIB_Total'], color='black', linewidth=1, linestyle='--', alpha=0.5)
plt.fill_between(df['Año'], df['PIB_Total'], df['Ganancia_Trabajo'], 
                 color='#1f2d3d', alpha=0.85, label='Ganancia del CAPITAL (Empresas, Bancos, Rentas)')

# 2. GANANCIA DEL PUEBLO (Parte inferior)
# Muestra la porción que realmente llega a los trabajadores
plt.plot(df['Año'], df['Ganancia_Trabajo'], color='#c0392b', linewidth=3)
plt.fill_between(df['Año'], 0, df['Ganancia_Trabajo'], 
                 color='#e74c3c', alpha=0.6, label='Ganancia del PUEBLO (Salarios Totales)')

# Configuración de Ejes
plt.yscale('linear') # Escala lineal para ver la magnitud real
plt.title('Distribución de la Riqueza en Colombia (1990 - 2025)\nCapital vs. Trabajo (Misma Escala)', 
          fontsize=16, fontweight='bold', pad=20)
plt.ylabel('Billones de Pesos Corrientes', fontsize=12, fontweight='bold')
plt.xlabel('Año', fontsize=12)

# Formato de miles en el eje Y
ax = plt.gca()
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

# Leyenda y Grid
plt.legend(loc='upper left', fontsize=11, frameon=True, shadow=True)
plt.grid(True, linestyle='--', alpha=0.5)

# Anotaciones de desigualdad
ultimo_anio = df.iloc[-1]
brecha = ultimo_anio['Ganancia_Capital'] / ultimo_anio['Ganancia_Trabajo']

plt.annotate(f'El Capital se lleva\n{brecha:.1f} veces lo que\nse lleva el pueblo', 
             xy=(2020, df[df['Año']==2020]['Ganancia_Capital'].values[0]), 
             xytext=(2010, df['PIB_Total'].max()*0.8),
             arrowprops=dict(facecolor='white', shrink=0.05),
             fontsize=10, fontweight='bold', color='white',
             bbox=dict(boxstyle="round,pad=0.3", fc="black", ec="none", alpha=0.7))

plt.tight_layout()

# Guardar
plt.savefig('grafica_desigualdad_real.png', dpi=300, bbox_inches='tight')
print("Gráfica guardada: 'grafica_desigualdad_real.png'")
plt.show()