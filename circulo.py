import matplotlib.pyplot as plt
import numpy as np

# Parámetros del proyecto
diametro_cm = 30
radio_cm = diametro_cm / 2
num_puntos = 250

# Tamaño de la figura (dejamos un poco más de margen para los números en zigzag)
fig_size_inches = (diametro_cm + 4) / 2.54 

fig, ax = plt.subplots(figsize=(fig_size_inches, fig_size_inches))

# Generar los ángulos
angulos = np.linspace(0, 2 * np.pi, num_puntos, endpoint=False)

# Coordenadas de los clavos (el punto 0 arriba a las 12)
x = radio_cm * np.cos(angulos - np.pi/2)
y = radio_cm * -np.sin(angulos - np.pi/2)

# Dibujar el círculo base
circulo = plt.Circle((0, 0), radio_cm, color='lightgray', fill=False, linewidth=1, linestyle='--')
ax.add_patch(circulo)

# Dibujar los 250 puntos
ax.scatter(x, y, s=10, color='black', zorder=2)

# Añadir etiquetas de texto para CADA punto en patrón zigzag
for i in range(num_puntos):
    # Si es par, lo ponemos a 0.5 cm del borde. Si es impar, a 1.2 cm.
    distancia_extra = 0.5 if i % 2 == 0 else 1.2 
    
    x_texto = (radio_cm + distancia_extra) * np.cos(angulos[i] - np.pi/2)
    y_texto = (radio_cm + distancia_extra) * -np.sin(angulos[i] - np.pi/2)
    
    # Usamos un tamaño de fuente pequeño (fontsize=5)
    ax.text(x_texto, y_texto, str(i), fontsize=5, ha='center', va='center')

# Configuración final
ax.set_aspect('equal')
ax.axis('off')

# Guardar el PDF
nombre_archivo = 'plantilla_250_numerada.pdf'
plt.savefig(nombre_archivo, format='pdf', bbox_inches='tight')

print(f"¡Listo! Plantilla generada con todos los números como '{nombre_archivo}'.")