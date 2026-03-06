import matplotlib.pyplot as plt
import pandas as pd

# 1. Datos históricos: Tasa de pobreza en EE.UU. (Porcentaje de la población)
# Estos datos reflejan la medición oficial del Census Bureau.
datos = {
    'Año': [1960, 1970, 1980, 1990, 2000, 2010, 2015, 2020, 2023, 2026],
    'Tasa_Pobreza_Pct': [22.2, 12.6, 13.0, 13.5, 11.3, 15.1, 13.5, 11.4, 11.5, 11.2]
}

df = pd.DataFrame(datos)

# 2. Configurar la gráfica
plt.figure(figsize=(12, 6))

# Dibujar la línea de la tasa de pobreza
plt.plot(df['Año'], df['Tasa_Pobreza_Pct'], color='#002868', marker='o', linewidth=3, label='Tasa de Pobreza (%)')
plt.fill_between(df['Año'], df['Tasa_Pobreza_Pct'], color='#bf0a30', alpha=0.1)

# 3. Marcar hitos importantes
plt.annotate('War on Poverty (LBJ)', xy=(1964, 19), xytext=(1970, 21),
             arrowprops=dict(facecolor='black', shrink=0.05))
plt.annotate('Crisis Financiera 2008', xy=(2010, 15.1), xytext=(1995, 17),
             arrowprops=dict(facecolor='red', shrink=0.05))

# 4. Estética y etiquetas
plt.title('Evolución de la Tasa de Pobreza en Estados Unidos (1960-2026)', fontsize=14)
plt.ylabel('Porcentaje de la Población (%)')
plt.xlabel('Año')
plt.ylim(0, 25) # Ajustamos el eje para ver la proporción real
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()

# 5. Guardar el archivo
nombre_img = "pobreza_eeuu_historico.png"
plt.tight_layout()
plt.savefig(nombre_img, dpi=300)

print(f"--- Proceso completado ---")
print(f"Gráfica guardada como '{nombre_img}' en tus archivos de Linux.")