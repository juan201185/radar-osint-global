import pandas as pd
import re

# Diccionarios de Inteligencia
ACTORES_CLAVE = {
    'Frente Carlos Patiño': r'Carlos Patiño|fcp|disidencias|mordisco|bocja',
    'ELN': r'ELN|Ejército de Liberación Nacional|bolivariano',
    'Segunda Marquetalia': r'Segunda Marquetalia|Diomer Cortés|marquetalia',
    'EGC / Clan del Golfo': r'EGC|Clan del Golfo|Autodefensas Gaitanistas|gaitanistas'
}

VEREDAS_PATIA = ['Galíndez', 'El Estrecho', 'La Mesa', 'Piedra de Moler', 'Carmelito', 'Angulo', 'El Cabuyal', 'La Fonda']

def corregir_anio(fecha_str):
    """Extrae el año sin importar si es 25 o 2025"""
    fecha_str = str(fecha_str).strip()
    partes = fecha_str.split('/')
    if len(partes) == 3:
        anio = partes[2]
        if len(anio) == 2:
            return int("20" + anio)
        return int(anio)
    return 2025 # Fallback

def caracterizar_datos():
    print("🚀 Iniciando caracterización profesional...")
    
    # Cargar los archivos generados en el paso anterior
    df_l = pd.read_csv("RESULTADO_LIDERES_ALERTA.csv")
    df_m = pd.read_csv("RESULTADO_MASACRES_ALERTA.csv")
    
    # --- 1. LIMPIEZA DE ACTORES Y VEREDAS ---
    def extraer_actor(fila):
        alertas = str(fila['alerta_previa']).lower()
        if alertas == "sin_alerta_detectada": return "ACTOR_DESCONOCIDO"
        for actor, patron in ACTORES_CLAVE.items():
            if re.search(patron, alertas): return actor
        return "DISPUTA_NO_DETERMINADA"

    print("⚔️ Cruzando actores armados con informes de la Defensoría...")
    df_l['actor_presunto'] = df_l.apply(extraer_actor, axis=1)
    df_m['actor_presunto'] = df_m.apply(extraer_actor, axis=1)

    # --- 2. CÁLCULO DE VENTANA DE RIESGO (CORREGIDO) ---
    print("📅 Calculando ventanas de tiempo (Alerta vs Hecho)...")
    def calcular_ventana(fila):
        alertas = str(fila['alerta_previa'])
        anio_hecho = corregir_anio(fila['fecha_exacta'])
        
        # El algoritmo asigna el año de la alerta más antigua detectada
        if "018-22" in alertas: return (anio_hecho - 2022) * 12
        if "036-23" in alertas: return (anio_hecho - 2023) * 12
        if "003-24" in alertas: return (anio_hecho - 2024) * 12
        if "008-25" in alertas: return (anio_hecho - 2025) * 12
        return 0

    df_l['ventana_meses'] = df_l.apply(calcular_ventana, axis=1)
    df_m['ventana_meses'] = df_m.apply(calcular_ventana, axis=1)

    # --- 3. GENERACIÓN DEL ÍNDICE DE RIESGO 2026 ---
    # Un municipio es de ALTO RIESGO si tiene alertas de 2025 y masacres recientes
    def calcular_riesgo(fila):
        score = 0
        alertas = str(fila['alerta_previa'])
        if "008-25" in alertas: score += 5  # Alerta de inminencia reciente
        if "003-24" in alertas: score += 3  # Riesgo estructural no resuelto
        if fila['actor_presunto'] != "ACTOR_DESCONOCIDO": score += 2
        return score

    df_m['indice_riesgo_2026'] = df_m.apply(calcular_riesgo, axis=1)

    # --- 4. GUARDAR BASE MAESTRA FINAL ---
    df_l.to_csv("BASE_MAESTRA_LIDERES_FINAL.csv", index=False)
    df_m.to_csv("BASE_MAESTRA_MASACRES_FINAL.csv", index=False)
    
    print("\n✅ PROCESO COMPLETADO")
    print("📂 Archivos listos en: /home/fatreber85/routersploit/")
    print(f"📊 Promedio de ventana de respuesta: {df_m[df_m['ventana_meses']>0]['ventana_meses'].mean():.1f} meses")

if __name__ == "__main__":
    caracterizar_datos()