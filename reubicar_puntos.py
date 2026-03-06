import pandas as pd

# Coordenadas exactas que faltan
NUEVAS_COORDENADAS = {
    'El Estrecho': [2.0355, -77.1353],
    'Galíndez': [2.0294, -77.1064],
    'Argelia': [2.1283, -77.1167],
    'Balboa': [2.1056, -77.2189],
    'Piedra de Moler': [2.0520, -77.0620]
}

def corregir_mapa():
    print("🎯 Reubicando puntos críticos: El Estrecho, Galíndez y Argelia...")
    df = pd.read_csv("MAPA_PREDICCION_PATIA_2026.csv")

    for lugar, coords in NUEVAS_COORDENADAS.items():
        # Buscamos si el lugar aparece en el municipio o en la vereda
        mask = (df['municipio'].str.contains(lugar, case=False, na=False)) | \
               (df['vereda'].str.contains(lugar, case=False, na=False))
        
        if mask.any():
            df.loc[mask, 'latitude'] = coords[0]
            df.loc[mask, 'longitude'] = coords[1]
            df.loc[mask, 'AVISO_PREDICCION'] = f"⚠️ ALERTA EN CORREGIMIENTO: {lugar}"
            print(f"✅ Punto corregido: {lugar}")
        else:
            # Si no existía el registro, lo creamos como alerta predictiva basada en los PDFs
            print(f"➕ Añadiendo punto preventivo: {lugar} (Detectado en Alerta 008-25)")
            nueva_fila = df.iloc[0].copy()
            nueva_fila['municipio'] = lugar
            nueva_fila['latitude'] = coords[0]
            nueva_fila['longitude'] = coords[1]
            nueva_fila['indice_riesgo_2026'] = 10
            nueva_fila['AVISO_PREDICCION'] = f"⚠️ RIESGO INMINENTE 2026: {lugar}"
            df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)

    df.to_csv("MAPA_CORREGIDO_FINAL.csv", index=False)
    print("\n🚀 ¡Listo! Sube 'MAPA_CORREGIDO_FINAL.csv' a My Maps.")

if __name__ == "__main__":
    corregir_mapa()