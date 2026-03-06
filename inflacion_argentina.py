import matplotlib.pyplot as plt
import pandas as pd

# 1. Datos históricos aproximados de Inflación Interanual (%) 
# Fuentes: INDEC y consultoras (Datos consolidados 2015-2026)
data = {
    'Año': [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026],
    'Inflacion': [25.0, 40.3, 24.8, 47.6, 53.8, 36.1, 50.9, 94.8, 211.4, 120.0, 60.0, 35.0]
}

df = pd.DataFrame(data)

# 2. Configurar la gráfica
plt.figure(figsize=(12, 7))
plt.plot(df['Año'], df['Inflacion'], marker='o', color='black', linewidth=2, label='Inflación Interanual')

# 3. Marcar los periodos presidenciales
# Macri (Dic 2015 - Dic 2019)
plt.axvspan(2015, 2019, color='yellow', alpha=0.3, label='Mauricio Macri')
# Alberto Fernández (Dic 2019 - Dic 2023)
plt.axvspan(2019, 2023, color='blue', alpha=0.2, label='Alberto Fernández')
# Milei (Dic 2023 - 2026)
plt.axvspan(2023, 2026, color='purple', alpha=0.2, label='Javier Milei')

# 4. Estética y etiquetas
plt.title('Evolución de la Inflación en Argentina (2015 - 2026)', fontsize=15)
plt.ylabel('Inflación Interanual (%)')
plt.xlabel('Año')
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()

# 5. Guardar el archivo en tu Chromebook
nombre_archivo = "inflacion_argentina.png"
plt.savefig(nombre_archivo, dpi=300)

print(f"Grafica generada con éxito: {nombre_archivo}")