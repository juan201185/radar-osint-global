import matplotlib.pyplot as plt
import pandas as pd

# Datos conceptuales de Colombia (Tendencia 2022-2026)
data = {
    'Año': [2022, 2023, 2024, 2025, 2026],
    'Gasto_Publico': [100, 115, 128, 140, 155], # Representa inversión estatal
    'PIB_Consumo': [100, 102, 105, 108, 112]    # Crecimiento del consumo interno
}

df = pd.DataFrame(data)

plt.figure(figsize=(10, 5))
plt.plot(df['Año'], df['Gasto_Publico'], label='Gasto Público (Estado)', color='blue', marker='o')
plt.plot(df['Año'], df['PIB_Consumo'], label='Consumo Interno', color='green', marker='s')

plt.title('Lógica Keynesiana: El Estado impulsando el Consumo')
plt.xlabel('Año')
plt.ylabel('Índice Base 100')
plt.legend()
plt.grid(True, alpha=0.3)

plt.savefig("keynesianismo_colombia.png")
print("Gráfica guardada como keynesianismo_colombia.png")