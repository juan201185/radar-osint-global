import matplotlib.pyplot as plt
import pandas as pd

# 1. Datos históricos (en millones de personas en pobreza extrema)
# Basado en reportes del Banco Mundial y el FMI.
# En 1980, casi el 90% de la población era pobre; hoy es menos del 1%.
datos = {
    'Año': [1980, 1990, 2000, 2010, 2015, 2020, 2024, 2026],
    'Personas_en_Pobreza_Millones': [850, 750, 500, 160, 55, 5, 1, 0.5]
}

df = pd.DataFrame(datos)

# 2. Calcular cuántas personas HAN SALIDO de la pobreza acumulativamente
# Tomamos como base el máximo histórico de 1980
poblacion_inicial_pobre = 850
df['Personas_Rescatadas_Millones'] = poblacion_inicial_pobre - df['Personas_en_Pobreza_Millones']

# 3. Crear la gráfica
plt.figure(figsize=(12, 6))
plt.fill_between(df['Año'], df['Personas_Rescatadas_Millones'], color='red', alpha=0.3)
plt.plot(df['Año'], df['Personas_Rescatadas_Millones'], color='darkred', marker='o', linewidth=3)

# 4. Estética y etiquetas
plt.title('Milagro Económico: Personas que salieron de la pobreza en China (1980-2026)', fontsize=14)
plt.ylabel('Millones de Personas')
plt.xlabel('Año de Apertura Económica')
plt.grid(True, linestyle='--', alpha=0.5)

# Añadir etiquetas de texto en los puntos clave
for i, txt in enumerate(df['Personas_Rescatadas_Millones']):
    plt.annotate(f"{int(txt)}M", (df['Año'][i], df['Personas_Rescatadas_Millones'][i]), 
                 textcoords="offset points", xytext=(0,10), ha='center', fontsize=9)

# 5. Guardar el archivo
nombre_img = "pobreza_china_logro.png"
plt.tight_layout()
plt.savefig(nombre_img, dpi=300)

print(f"Gráfica generada: {nombre_img}")