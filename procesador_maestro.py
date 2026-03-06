import pandas as pd
import csv
import re
import os

# CONFIGURACIÓN
ARCHIVO_ENTRADA = "datos_brutos.txt"
ARCHIVO_SALIDA = "base_datos_patia_2021_2026.csv"

def limpiar_y_estructurar():
    print(f"⚙️ Procesando histórico 2021-2025...")
    datos_limpios = []
    
    with open(ARCHIVO_ENTRADA, 'r', encoding='utf-8') as f:
        lineas = f.readlines()
        
    anio_actual = "2025" # Valor por defecto inicial
    
    for linea in lineas:
        linea = linea.strip()
        
        # Detectar cambio de año en el texto
        if linea in ["2025", "2024", "2023", "2022", "2021"]:
            anio_actual = linea
            continue
            
        # Regex para detectar filas que empiezan con un número (formato de la tabla)
        # Ejemplo: "1  12/01/25  Valle del Cauca  Cali  3"
        match = re.match(r'^(\d+)\s+(\d{2}/\d{2}/\d{2,4})\s+(.*?)\s+(.*?)\s+(\d+|Por determinar)', linea)
        
        if match:
            num, fecha, depto, municipio, victimas = match.groups()
            
            # FILTRO CRUCIAL: Solo nos interesa el Cauca para este algoritmo
            if "Cauca" in depto:
                datos_limpios.append({
                    "id_evento": f"IND-{anio_actual}-{num}",
                    "fecha_exacta": fecha,
                    "año": anio_actual,
                    "departamento": depto.strip(),
                    "municipio": municipio.strip(),
                    "num_victimas": victimas,
                    "tipo_violencia": "Masacre",
                    "nivel_certeza": "Alta (Indepaz)",
                    "fuente_url": "Indepaz - Balance Histórico"
                })

    # Crear el DataFrame con las 22 columnas (rellenando las vacías para el futuro)
    df = pd.DataFrame(datos_limpios)
    
    # Añadimos las columnas faltantes que acordamos para la base PRO
    columnas_faltantes = [
        "corregimiento", "vereda", "coordenadas_xy", "actor_presunto", 
        "frente_bloque", "objetivo_ataque", "arma_usada", "modus_operandi", 
        "perfil_victima", "desplazamiento_forzado", "notas_inteligencia", 
        "alerta_previa", "ventana_dias"
    ]
    for col in columnas_faltantes:
        df[col] = "PENDIENTE_CRUCE"

    df.to_csv(ARCHIVO_SALIDA, index=False, encoding='utf-8-sig')
    print(f"✅ Base de datos generada: {ARCHIVO_SALIDA}")
    print(f"📊 Total eventos registrados en el Cauca: {len(df)}")

if __name__ == "__main__":
    limpiar_y_estructurar()