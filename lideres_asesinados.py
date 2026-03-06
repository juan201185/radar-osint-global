import pandas as pd
import re

# CONFIGURACIÓN
ARCHIVO_LIDERES = "lideres_asesinados.txt"
SALIDA_LIDERES = "lideres_caracterizados_cauca.csv"

def caracterizar_lideres():
    print("🧠 Caracterizando perfiles de líderes asesinados...")
    datos = []
    
    with open(ARCHIVO_LIDERES, 'r', encoding='utf-8') as f:
        lineas = f.readlines()

    for linea in lineas:
        linea = linea.strip()
        
        # Regex para capturar: Nº, Nombre, Fecha, Departamento, Municipio, Sector
        # Ejemplo: "6  Diany Ruiz  13/01/2025  Santander  Barrancabermeja  LGBTIQ+"
        match = re.match(r'^(\d+)\s+(.*?)\s+(\d{2}/\d{2}/\d{4})\s+(.*?)\s+(.*?)\s+([A-ZÁÉÍÓÚ\+].*)$', linea)
        
        if match:
            num, nombre, fecha, depto, muni, sector = match.groups()
            
            # Filtramos solo Cauca
            if "Cauca" in depto:
                datos.append({
                    "id_evento": f"LID-{num}",
                    "nombre_victima": nombre.strip(),
                    "fecha_exacta": fecha,
                    "municipio": muni.strip(),
                    "perfil_victima": sector.strip(),
                    "tipo_violencia": "Homicidio Selectivo",
                    "nivel_certeza": "Alta (Indepaz)"
                })

    df = pd.DataFrame(datos)
    
    # Añadimos las columnas técnicas para que encaje con tu base maestra
    for col in ["vereda", "actor_presunto", "modus_operandi", "alerta_previa"]:
        df[col] = "PENDIENTE_CRUCE_PDF"

    df.to_csv(SALIDA_LIDERES, index=False, encoding='utf-8-sig')
    print(f"✅ Archivo generado: {SALIDA_LIDERES}")
    print(f"📊 Líderes caracterizados en el Cauca: {len(df)}")
    print("\nResumen de sectores afectados en Cauca:")
    print(df['perfil_victima'].value_counts())

if __name__ == "__main__":
    caracterizar_lideres()