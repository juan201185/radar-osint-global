import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# -----------------------------------------------------------------------------
# 1. DATOS HISTÓRICOS (1990 - 2025)
# -----------------------------------------------------------------------------
# Periodo: Gobiernos desde César Gaviria hasta Gustavo Petro (actualidad)

anios = list(range(1990, 2026))

# Datos aproximados basados en series del DANE y Banco de la República
data = {
    'Año': anios,
    
    # IPC Causado (Inflación real del año anterior usada para negociar)
    'IPC_Causado': [
        26.12, 32.36, 26.82, 22.60, 22.59, 19.46, 21.63, 17.68, 16.70, 9.23, # 90-99
        8.75, 7.65, 6.99, 6.49, 5.50, 4.85, 4.48, 5.69, 7.67, 2.00,        # 00-09
        3.17, 3.73, 2.44, 1.94, 3.66, 6.77, 5.75, 4.09, 3.18, 3.80,        # 10-19
        1.61, 5.62, 13.12, 9.28, 5.20, 3.60                                # 20-25 (Est. final)
    ],

    # Aumento Salario Mínimo Legal Vigente (Nominal)
    'Aumento_Salarial': [
        26.0, 26.1, 26.0, 25.0, 21.1, 20.5, 19.5, 21.0, 18.5, 16.0, # 90-99
        10.0, 10.0, 8.0, 7.4, 7.8, 6.6, 6.9, 6.4, 7.7, 3.6,        # 00-09
        3.6, 4.0, 5.8, 4.02, 4.5, 4.6, 7.0, 7.0, 5.9, 6.0,         # 10-19
        6.0, 3.5, 10.07, 16.0, 12.07, 9.54                         # 20-25
    ],
    
    # Crecimiento del PIB
    'PIB_Crecimiento': [
        4.3, 2.4, 4.0, 5.0, 5.8, 5.2, 2.1, 3.4, 0.6, -4.2, 
        2.9, 1.7, 2.5, 3.9, 5.3, 4.7, 6.7, 6.9, 3.5, 1.7,  
        4.0, 6.6, 4.0, 4.3, 4.6, 3.1, 2.1, 1.4, 2.6, 3.2,  
        -7.0, 10.7, 7.3, 0.6, 1.8, 3.2                     
    ],
    
    # Meta de Inflación (BanRep) - Nula antes del 2000 aprox
    'Meta_Inflacion': [
        np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 16.0, 15.0,
        10.0, 8.0, 6.0, 5.5, 5.0, 4.5, 4.0, 4.0, 4.0, 3.5,            
        3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0,             
        3.0, 3.0, 3.0, 3.0, 3.0, 3.0                                  
    ],

    # Productividad (PTF/Laboral) - Factor estructural aproximado
    'Productividad': [
        0.5, 0.8, 1.2, 1.0, 0.9, 0.5, -0.5, 0.2, -1.5, -2.0,
        1.5, 1.0, 1.2, 1.8, 2.0, 1.5, 1.8, 1.2, 0.5, -0.8,
        0.5, 1.5, 0.8, 0.9, 0.8, 0.6, 0.5, 0.6, 0.7, 0.8,
        -0.6, 1.2, 1.1, 0.8, 0.78, 0.8
    ],
    
    # Participación de Salarios en Ingreso Nacional (% PIB)
    'Participacion_Salarios': [
        38.5, 38.0, 37.5, 37.0, 36.5, 36.0, 35.5, 35.0, 34.5, 34.0,
        33.5, 33.2, 33.0, 32.5, 32.0, 31.8, 31.5, 31.2, 31.5, 32.0,
        32.5, 33.0, 33.2, 33.5, 33.6, 33.8, 34.0, 34.2, 34.1, 34.0,
        33.5, 32.8, 31.5, 32.0, 32.5, 32.8
    ]
}

# Crear DataFrame
df = pd.DataFrame(data)

# Calcular el Factor de Negociación (Residual)
df['Factor_Negociacion'] = df['Aumento_Salarial'] - (df['IPC_Causado'] + df['Productividad'])

# -----------------------------------------------------------------------------
# 2. CONFIGURACIÓN DE LA GRÁFICA
# -----------------------------------------------------------------------------
plt.figure(figsize=(16, 9)) # Formato panorámico
plt.style.use('seaborn-v0_8-whitegrid')

# EJE IZQUIERDO: Variables de Variación (%)
ax1 = plt.gca()

# 1. Aumento Salarial (RESALTADO PRINCIPAL)
ax1.plot(df['Año'], df['Aumento_Salarial'], 
         color='#d62728', linewidth=5, label='Aumento Salarial (SMLV)', zorder=10)

# 2. IPC Causado (Inflación)
ax1.plot(df['Año'], df['IPC_Causado'], 
         color='#1f77b4', linewidth=2, linestyle='--', label='IPC Causado (Inflación)', alpha=0.9)

# 3. Productividad
ax1.plot(df['Año'], df['Productividad'], 
         color='#9467bd', linewidth=2, linestyle='-.', label='Productividad', alpha=0.8)

# 4. Meta de Inflación
ax1.plot(df['Año'], df['Meta_Inflacion'], 
         color='#2ca02c', linewidth=1.5, linestyle=':', label='Meta Inflación (BanRep)', alpha=0.6)

# Sombrear el "Factor de Negociación" (Área amarilla entre la fórmula técnica y el aumento real)
# Fórmula Técnica = IPC + Productividad
formula_tecnica = df['IPC_Causado'] + df['Productividad']
ax1.fill_between(df['Año'], formula_tecnica, df['Aumento_Salarial'], 
                 where=(df['Aumento_Salarial'] > formula_tecnica),
                 color='#ffd700', alpha=0.2, label='Factor de Negociación (Ganancia)')

# EJE DERECHO: Participación de Salarios (% del PIB)
# Se usa eje derecho porque la escala es diferente (30-40%) a la variación anual (0-25%)
ax2 = ax1.twinx()
ax2.plot(df['Año'], df['Participacion_Salarios'], 
         color='#ff7f0e', linewidth=2.5, linestyle='-', alpha=0.6, label='Participación Salarios en PIB')
ax2.set_ylabel('Participación en el Ingreso Nacional (%)', fontsize=12, color='#ff7f0e', rotation=270, labelpad=20)
ax2.tick_params(axis='y', labelcolor='#ff7f0e')
ax2.set_ylim(0, 50) 
ax2.grid(False) # Desactivar rejilla secundaria para limpieza visual

# Etiquetas y Títulos
ax1.set_ylabel('Variación Anual (%)', fontsize=12, fontweight='bold')
ax1.set_xlabel('Año (Periodos Presidenciales)', fontsize=12)
ax1.set_title('Dinámica Salarial en Colombia: Ley 278 de 1996 vs Realidad (1990-2025)', 
              fontsize=16, fontweight='bold', pad=20)

# Leyenda unificada
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper right', frameon=True, shadow=True, fontsize=10)

# Marcas de presidentes en el eje X
presidentes = [
    (1990, 'Gaviria'), (1994, 'Samper'), (1998, 'Pastrana'), 
    (2002, 'Uribe I'), (2006, 'Uribe II'), (2010, 'Santos I'), 
    (2014, 'Santos II'), (2018, 'Duque'), (2022, 'Petro')
]
for anio, nombre in presidentes:
    ax1.axvline(x=anio, color='gray', linestyle=':', alpha=0.4)
    if anio < 2022:
        ax1.text(anio + 0.5, 30, nombre, rotation=90, verticalalignment='top', fontsize=8, color='#555')
    else:
        ax1.text(anio, 30, nombre, rotation=90, verticalalignment='top', fontsize=8, color='#555')

plt.tight_layout()

# -----------------------------------------------------------------------------
# 3. GUARDAR Y MOSTRAR
# -----------------------------------------------------------------------------

nombre_archivo = 'grafica_economia_colombia.png'
plt.savefig(nombre_archivo, dpi=300, bbox_inches='tight')
print(f"✅ Gráfica generada exitosamente.")
print(f"📁 Archivo guardado como: {nombre_archivo}")
print("   (Busca en tu carpeta 'Archivos de Linux')")

plt.show()