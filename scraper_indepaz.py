import pandas as pd
import requests
import os
from io import StringIO

# CONFIGURACIÓN
URL_MASACRES = "https://indepaz.org.co/informe-de-masacres-en-colombia-durante-el-2020-2021/"
ARCHIVO_SALIDA = "masacres_cauca_2021_2026.csv"

def ejecutar_extraccion():
    print(f"🚀 Iniciando extracción en: {os.getcwd()}")
    
    try:
        # Simulamos un navegador real de forma más completa
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'es-ES,es;q=0.9',
        }
        
        print("📥 Conectando con la web de Indepaz...")
        response = requests.get(URL_MASACRES, headers=headers, timeout=15)
        response.raise_for_status() # Lanza error si la página no carga

        # Usamos StringIO para evitar advertencias de pandas en versiones nuevas
        print("📊 Buscando tablas en el contenido...")
        tablas = pd.read_html(StringIO(response.text))
        
        if not tablas:
            print("❌ No se encontraron tablas en la página. Es posible que el contenido sea dinámico.")
            return

        # Seleccionamos la tabla (probamos con la primera que tenga datos)
        df = None
        for t in tablas:
            if len(t) > 10: # Buscamos una tabla con datos reales, no una pequeña
                df = t
                break
        
        if df is None:
            df = tablas[0]

        # Estandarizar columnas
        df.columns = [str(c).strip().upper() for c in df.columns]
        
        # Buscar la columna departamento (puede variar el nombre)
        col_depto = [c for c in df.columns if 'DEP' in c][0]
        
        print(f"✅ Tabla encontrada. Registros totales: {len(df)}")
        
        # Filtrar por Cauca
        df_cauca = df[df[col_depto].str.contains('Cauca', case=False, na=False)].copy()
        
        # Guardar CSV
        df_cauca.to_csv(ARCHIVO_SALIDA, index=False, encoding='utf-8-sig')
        print(f"📂 Archivo generado: {ARCHIVO_SALIDA} ({len(df_cauca)} registros del Cauca)")

    except Exception as e:
        print(f"❌ Error técnico detallado: {e}")

if __name__ == "__main__":
    ejecutar_extraccion()