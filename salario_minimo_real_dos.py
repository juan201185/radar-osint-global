import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# -----------------------------------------------------------------------------
# 1. DATOS (Mismos datos históricos, sin cambios)
# -----------------------------------------------------------------------------
anios = list(range(1990, 2026))

data = {
    'Año': anios,
    
    # Inflación (IPC)
    'IPC_Causado': [
        26.12, 32.36, 26.82, 22.60, 22.59, 19.46, 21.63, 17.68, 16.70, 9.23,
        8.75, 7.65, 6.99, 6.49, 5.50, 4.85, 4.48, 5.69, 7.67, 2.00,
        3.17, 3.73, 2.44, 1.94, 3.66, 6.77, 5.75, 4.09, 3.18, 3.80,
        1.61, 5.62, 13.12, 9.28, 5.20, 3.60
    ],

    # Aumento Salario Mínimo
    'Aumento_Salarial': [
        26.0, 26.1, 26.0, 25.0, 21.1, 20.5, 19.5, 21.0, 18.5, 16.0,
        10.0, 10.0, 8.0, 7.4, 7.8, 6.6, 6.9, 6.4, 7.7, 3.6,
        3.6, 4.0, 5.8, 4.02, 4.5, 4.6, 7.0, 7.0, 5.9, 6.0,
        6.0, 3.5, 10.07, 16.0, 12.07, 9.54
    ],
    
    # Meta Inflación (Aproximada antes de 2000 para continuidad visual)
    'Meta_Inflacion': [
        25.0, 25.0, 24.0, 22.0, 20.0, 18.0, 18.0, 18.0, 16.0, 15.0, # Estimado 90s
        10.0, 8.0, 6.0, 5.5, 5.0, 4.5, 4.0, 4.0, 4.0, 3.5,            
        3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0,             
        3.0, 3.0, 3.0, 3.0, 3.0, 3.0                                  
    ],

    # Productividad
    'Productividad': [
        0.5, 0.8, 1.2, 1.0, 0.9, 0.5, -0.5, 0.2, -1.5, -2.0,
        1.5, 1.0, 1.2, 1.8, 2.0, 1.5, 1.8, 1.2, 0.5, -0.8,
        0.5, 1.5, 0.8, 0.9, 0.8, 0.6, 0.5, 0.6, 0.7, 0.8,
        -0.6, 1.2, 1.1, 0.8, 0.78, 0.8
    ],
    
    # Participación Salarios en el PIB (Share Laboral)
    'Participacion_Salarios': [
        38.5, 38.0, 37.5, 37.0, 36.5, 36.0, 35.5, 35.0, 34.5, 34.0,
        33.5, 33.2, 33.0, 32.5, 32.0, 31.8, 31.5, 31.2, 31.5, 32.0,
        32.5, 33.0, 33.2, 33.5, 33.6, 33.8, 34.0, 34.2, 34.1, 34.0,
        33.5, 32.8, 31.5, 32.0, 32.5, 32.8
    ]
}

df = pd.DataFrame(data)

# -----------------------------------------------------------------------------
# 2. GRAFICACIÓN CON ESCALA UNIFICADA
# -----------------------------------------------------------------------------
plt.figure(figsize=(16, 10))
plt.style.use('seaborn-v0_8-whitegrid')

ax = plt.gca()

# --- A. CONTEXTO ESTRUCTURAL (Parte Alta) ---
# Participación de los salarios en el PIB (Suele estar entre 30% y 40%)
ax.plot(df['Año'], df['Participacion_Salarios'], 
         color='#ff7f0e', linewidth=3, linestyle='-', alpha=0.8, 
         label='Participación Salarios en PIB (La tajada del trabajador)')

# --- B. VARIABLES DE NEGOCIACIÓN (Parte Media/Baja) ---

# 1. Aumento Salarial (RESALTADO - Lo más importante)
ax.plot(df['Año'], df['Aumento_Salarial'], 
         color='#d62728', linewidth=5, label='Aumento Salarial Decretado (SMLV)', zorder=10)

# 2. Inflación (IPC)
ax.plot(df['Año'], df['IPC_Causado'], 
         color='#1f77b4', linewidth=2, linestyle='--', label='Inflación (IPC - Costo de Vida)')

# 3. Meta Inflación
ax.plot(df['Año'], df['Meta_Inflacion'], 
         color='#2ca02c', linewidth=1.5, linestyle=':', alpha=0.6, label='Meta Inflación (BanRep)')

# 4. Productividad (Suele estar cerca de 0-2%)
ax.plot(df['Año'], df['Productividad'], 
         color='#9467bd', linewidth=2, linestyle='-.', label='Productividad')

# --- C. ÁREAS DE INTERÉS ---

# Sombrear la ganancia real en la negociación (Diferencia entre Salario e IPC+Prod)
techo_tecnico = df['IPC_Causado'] + df['Productividad']
ax.fill_between(df['Año'], techo_tecnico, df['Aumento_Salarial'], 
                 where=(df['Aumento_Salarial'] > techo_tecnico),
                 color='#ffd700', alpha=0.3, label='Ganancia de Negociación (Plus Sindical)')

# --- D. FORMATO Y TEXTOS ---

# Títulos
plt.title('Economía Colombiana: Variables Salariales en la MISMA ESCALA (1990-2025)\nComparativa Directa de Porcentajes', 
          fontsize=16, fontweight='bold', pad=20)

plt.ylabel('Porcentaje Total (%)', fontsize=14, fontweight='bold')
plt.xlabel('Año (Periodos Presidenciales)', fontsize=12)

# Configurar Eje Y para que se vea todo claro (0 a 45%)
plt.ylim(-3, 45) 
plt.yticks(np.arange(0, 46, 5)) # Marcas cada 5%

# Leyenda unificada
plt.legend(loc='center right', frameon=True, shadow=True, fontsize=11, bbox_to_anchor=(1, 0.6))

# Marcas de presidentes (Verticales)
presidentes = [
    (1990, 'Gaviria'), (1994, 'Samper'), (1998, 'Pastrana'), 
    (2002, 'Uribe I'), (2006, 'Uribe II'), (2010, 'Santos I'), 
    (2014, 'Santos II'), (2018, 'Duque'), (2022, 'Petro')
]
for anio, nombre in presidentes:
    plt.axvline(x=anio, color='gray', linestyle=':', alpha=0.4)
    plt.text(anio, 42, nombre, rotation=90, verticalalignment='top', fontsize=9, color='#555')

plt.tight_layout()

# Guardar archivo
nombre_archivo = 'grafica_escala_unificada.png'
plt.savefig(nombre_archivo, dpi=300, bbox_inches='tight')
print(f"✅ Gráfica generada: {nombre_archivo}")
print("   (Ahora todas las líneas usan el eje izquierdo de 0% a 45%)")

plt.show()