import pandas as pd

# Diccionario de Coordenadas Maestras (Puntos Críticos detectados)
# Estas coordenadas son aproximadas para centros poblados y veredas clave
COORDENADAS_CAUCA = {
    'El Patía': [2.0689, -77.0314],
    'El Bordo': [2.1132, -76.9839],
    'Galíndez': [2.0294, -77.1064],
    'El Estrecho': [2.0355, -77.1353],
    'Argelia': [2.1283, -77.1167],
    'Balboa': [2.1056, -77.2189],
    'Puerto Tejada': [3.2281, -76.4169],
    'Guachené': [3.1311, -76.3939],
    'Buenos Aires': [2.9556, -76.6439],
    'Santander de Quilichao': [3.0089, -76.4853]
}

def generar_datos_mapa():
    print("📍 Geocodificando base de datos para 2026...")
    
    # Cargamos el resultado de las masacres
    df = pd.read_csv("PROYECTO_FINAL_PATIA_MASACRES.csv")
    
    def asignar_lat(muni):
        return COORDENADAS_CAUCA.get(muni, [2.4411, -76.6061])[0] # Por defecto Popayán
        
    def asignar_lon(muni):
        return COORDENADAS_CAUCA.get(muni, [2.4411, -76.6061])[1]

    df['latitude'] = df['municipio'].apply(asignar_lat)
    df['longitude'] = df['municipio'].apply(asignar_lon)

    # Crear etiqueta de Alerta para el mapa
    def etiqueta_aviso(fila):
        if fila['indice_riesgo_2026'] >= 5:
            return f"⚠️ ALERTA ACTIVA 2026: {fila['actor_presunto']}"
        return "Riesgo Histórico"

    df['AVISO_PREDICCION'] = df.apply(etiqueta_aviso, axis=1)

    # Guardar para Google My Maps
    df.to_csv("MAPA_PREDICCION_PATIA_2026.csv", index=False)
    print("✅ Archivo listo: MAPA_PREDICCION_PATIA_2026.csv")
    print("👉 Instrucción: Sube este archivo a Google My Maps y usa 'AVISO_PREDICCION' como nombre del marcador.")

if __name__ == "__main__":
    generar_datos_mapa()