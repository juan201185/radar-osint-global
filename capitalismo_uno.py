import matplotlib.pyplot as plt
import pandas as pd

# 1. Datos: Número total de personas en pobreza (en millones)
# Basado en datos históricos del U.S. Census Bureau y proyecciones del Banco Mundial
datos = {
    'Año': [1980, 1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020, 2023, 2026],
    'Pobreza_Millones': [29.3, 33.1, 33.6, 36.4, 31.1, 37.0, 46.2, 43.1, 37.2, 37.9, 37.5]
}

df = pd.DataFrame(datos)

# 2. Configurar la gráfica
plt.figure(figsize=(12, 6))

# Usamos colores de la bandera de EE.UU. (Azul y Rojo)
plt.fill_between(df['Año'], df['Pobreza_Millones'], color='#bf0a30', alpha=0.1)
plt.plot(df['Año'], df['Pobreza_Millones'], color='#002868', marker='o', linewidth=3, label='Personas en Pobreza')

# 3. Estética y etiquetas
plt.title('Número de Personas en Pobreza en EE. UU. (1980-2026)', fontsize=14)
plt.ylabel('Millones de Personas')
plt.xlabel('Año')
plt.grid(True, linestyle='--', alpha=0.5)

# Añadir etiquetas con el número exacto en los puntos clave
for i, txt in enumerate(df['Pobreza_Millones']):
    plt.annotate(f"{txt}M", (df['Año'][i], df['Pobreza_Millones'][i]), 
                 textcoords="offset points", xytext=(0,10), ha='center', fontsize=9)

# 4. Resaltar la diferencia con China
plt.text(1985, 45, 'EE.UU.: La pobreza se mantiene estable \nmientras la población crece.', 
         bbox=dict(facecolor='white', alpha=0.5))

# 5. Guardar archivo
nombre_img = "pobreza_eeuu_millones.png"
plt.tight_layout()
plt.savefig(nombre_img, dpi=300)

print(f"Éxito: Gráfica guardada como '{nombre_img}'")