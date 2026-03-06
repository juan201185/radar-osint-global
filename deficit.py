import matplotlib.pyplot as plt
import pandas as pd

# 1. Datos representativos de los países con mayor déficit fiscal (% del PIB)
# Estos datos reflejan economías bajo presión, conflictos o grandes planes de estímulo.
datos = {
    'País': [
        'Ucrania', 'Líbano', 'Yemen', 'Sudán', 'Egipto', 
        'Argentina', 'EE.UU.', 'Italia', 'Francia', 'India',
        'Brasil', 'Turquía', 'Pakistán', 'Reino Unido', 'España',
        'Japón', 'Sudáfrica', 'Colombia', 'Ghana', 'Argelia'
    ],
    'Deficit_PIB': [
        22.5, 18.2, 15.1, 14.5, 11.8, 
        8.5, 7.2, 6.8, 5.5, 5.4, 
        5.2, 4.9, 4.8, 4.6, 4.2, 
        4.1, 3.9, 3.8, 3.5, 3.2
    ]
}

df = pd.DataFrame(datos)

# Ordenar de mayor a menor déficit
df = df.sort_values(by='Deficit_PIB', ascending=False)

# 2. Configurar la gráfica
plt.figure(figsize=(12, 8))
# Usamos un mapa de colores que vaya de rojo (alto déficit) a naranja
colors = plt.cm.Reds(df['Deficit_PIB'] / df['Deficit_PIB'].max())

bars = plt.barh(df['País'], df['Deficit_PIB'], color=colors, edgecolor='black')

# 3. Estética y etiquetas
plt.gca().invert_yaxis() # Los países con más déficit arriba
plt.title('Top 20 Países con Mayor Déficit Fiscal (Est. 2025-2026)', fontsize=15)
plt.xlabel('Déficit como % del PIB')
plt.grid(axis='x', linestyle='--', alpha=0.6)

# Añadir etiquetas de valor al final de cada barra
for bar in bars:
    plt.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2, 
             f"{bar.get_width()}%", va='center', fontweight='bold')

# 4. Guardar archivo
nombre_salida = "top_deficit_fiscal.png"
plt.tight_layout()
plt.savefig(nombre_salida, dpi=300)

print(f"Éxito: La gráfica se guardó como '{nombre_salida}'")