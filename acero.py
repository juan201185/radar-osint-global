import matplotlib.pyplot as plt
import pandas as pd

# 1. Datos representativos de producción de acero crudo
# Medido en Millones de Toneladas Métricas (MT)
# Fuente: World Steel Association / AISI (Estimaciones consolidadas)
data = {
    'Año': [2021, 2022, 2023, 2024, 2025, 2026],
    'Produccion_Acero': [85.8, 80.5, 80.7, 81.5, 82.2, 83.0]
}

df = pd.DataFrame(data)

# 2. Configuración de la gráfica
plt.figure(figsize=(12, 6))
plt.plot(df['Año'], df['Produccion_Acero'], color='#2c3e50', marker='s', linewidth=3, label='Producción de Acero Crudo')
plt.fill_between(df['Año'], df['Produccion_Acero'], color='#95a5a6', alpha=0.2)

# 3. Marcar periodos presidenciales
# Biden (2021 - Enero 2025)
plt.axvspan(2021, 2024.9, color='#002868', alpha=0.15, label='Gestión Biden')
# Trump (Enero 2025 - 2026)
plt.axvspan(2024.9, 2026, color='#bf0a30', alpha=0.15, label='Gestión Trump')

# 4. Estética y etiquetas
plt.title('Producción de Acero en EE. UU. (2021 - 2026)', fontsize=14)
plt.ylabel('Millones de Toneladas Métricas (MT)')
plt.xlabel('Año')
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(loc='lower right')

# Añadir etiquetas de valor
for i, val in enumerate(df['Produccion_Acero']):
    plt.text(df['Año'][i], val + 0.2, f"{val} MT", ha='center', fontweight='bold')

# 5. Guardar archivo
nombre_img = "produccion_acero_eeuu.png"
plt.tight_layout()
plt.savefig(nombre_img, dpi=300)

print(f"Gráfica generada exitosamente como '{nombre_img}'")