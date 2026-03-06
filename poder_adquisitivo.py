import matplotlib.pyplot as plt
import pandas as pd

# 1. Datos representativos del Índice de Salario Real (Base 100 en 2015)
# Estos valores reflejan la pérdida de capacidad de compra acumulada.
data = {
    'Año': [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026],
    'Poder_Adquisitivo': [100, 94, 96, 85, 78, 76, 74, 72, 65, 58, 62, 68] 
}

df = pd.DataFrame(data)

# 2. Crear la gráfica
plt.figure(figsize=(12, 7))
plt.plot(df['Año'], df['Poder_Adquisitivo'], color='red', marker='s', linewidth=3, label='Poder de Compra')

# 3. Sombreado por Presidencia
# Macri (2015-2019)
plt.axvspan(2015, 2019, color='yellow', alpha=0.2, label='Gestión Macri')
# Fernández (2019-2023)
plt.axvspan(2019, 2023, color='blue', alpha=0.15, label='Gestión Fernández')
# Milei (2023-2026)
plt.axvspan(2023, 2026, color='purple', alpha=0.15, label='Gestión Milei')

# 4. Detalles visuales
plt.title('Evolución del Poder Adquisitivo en Argentina (Base 100 = 2015)', fontsize=14)
plt.ylabel('Índice de Salario Real')
plt.xlabel('Periodo Presidencial')
plt.grid(True, which='both', linestyle='--', alpha=0.5)
plt.legend()

# 5. Guardar el archivo
nombre_img = "poder_adquisitivo_arg.png"
plt.savefig(nombre_img, dpi=300)

print(f"Gráfica generada: {nombre_img}")