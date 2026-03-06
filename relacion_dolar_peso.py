import matplotlib.pyplot as plt
import pandas as pd

# Datos simulados que representan la realidad argentina
# Muestra cómo cuando el dólar salta, el poder adquisitivo (Salario) cae
data = {
    'Mes': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct'],
    'Precio_Dolar': [800, 820, 1000, 1050, 1100, 1250, 1300, 1350, 1400, 1450],
    'Poder_Compra_Salario': [100, 98, 85, 82, 80, 72, 70, 68, 66, 65]
}

df = pd.DataFrame(data)

fig, ax1 = plt.subplots(figsize=(10, 5))

# Eje para el Dólar
ax1.set_xlabel('Meses')
ax1.set_ylabel('Precio del Dólar ($)', color='blue')
ax1.plot(df['Mes'], df['Precio_Dolar'], color='blue', marker='o', label='Subida del Dólar')

# Eje para el Poder Adquisitivo
ax2 = ax1.twinx()
ax2.set_ylabel('Poder Adquisitivo (Base 100)', color='red')
ax2.plot(df['Mes'], df['Poder_Compra_Salario'], color='red', marker='x', label='Caída del Salario')

plt.title('Relación Inversa: Dólar vs. Poder Adquisitivo')
plt.grid(alpha=0.3)
plt.savefig("relacion_dolar_peso.png")

print("Gráfica guardada como 'relacion_dolar_peso.png'")