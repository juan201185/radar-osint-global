import pandas as pd
import folium
import requests
from io import StringIO
import datetime

# --- CONFIGURACIÓN DE LA LUPA TÁCTICA ---
MAP_KEY = "c7d1ad2cb48cfb61a3b6653a1cf98ea9" 

# Coordenadas cerradas sobre Israel, Líbano y Gaza
# Formato: Oeste, Sur, Este, Norte
ZONA_TACTICA = "33.5,29.5,36.5,34.5" 

def obtener_datos_lupa(rango_dias=1):
    """Descarga datos satelitales enfocados solo en la franja del Levante"""
    url = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{MAP_KEY}/VIIRS_SNPP_NRT/{ZONA_TACTICA}/{rango_dias}"
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Enfocando satélite sobre Israel y Líbano...")
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            df = pd.read_csv(StringIO(response.text))
            print(f"-> Éxito: {len(df)} firmas térmicas detectadas en la lupa.")
            return df
        else:
            print(f"-> Error de conexión: {response.status_code}")
            return None
    except Exception as e:
        print(f"-> Error técnico: {e}")
        return None

def generar_lupa():
    df = obtener_datos_lupa(1)
    if df is None or df.empty:
        print("El satélite no reporta anomalías recientes en esta zona o no ha pasado aún.")
        return

    # Mapa centrado exactamente en el norte de Israel / Sur del Líbano con más zoom
    mapa = folium.Map(location=[33.0, 35.2], zoom_start=8, tiles='CartoDB dark_matter')

    # --- CALIBRACIÓN DE SENSIBILIDAD ---
    # Bajamos el umbral a 310 Kelvin para detectar impactos tácticos (artillería/cohetes)
    alertas_tacticas = df[df['bright_ti4'] > 310]
    ruido_menor = df[df['bright_ti4'] <= 310]

    # 1. Calor residual o muy leve (puntos grises pequeños)
    for _, fila in ruido_menor.iterrows():
        folium.CircleMarker(
            location=[fila['latitude'], fila['longitude']],
            radius=1, color='gray', fill=True, opacity=0.5,
            tooltip="Calor residual"
        ).add_to(mapa)

    # 2. Impactos tácticos / Incendios por artillería (Iconos rojos)
    for _, fila in alertas_tacticas.iterrows():
        temp_c = round(fila['bright_ti4'] - 273.15, 1)
        info = f"""
        <div style="font-family: Arial; width: 180px;">
            <b style="color:#ff3333;">ANOMALÍA TÁCTICA</b><br>
            <hr>
            <b>Coords:</b> {fila['latitude']}, {fila['longitude']}<br>
            <b>Temp:</b> {temp_c}°C<br>
            <b>Hora UTC:</b> {fila['acq_time']}<br>
            <b>Confianza:</b> {fila['confidence']}
        </div>
        """
        folium.Marker(
            location=[fila['latitude'], fila['longitude']],
            popup=folium.Popup(info, max_width=200),
            icon=folium.Icon(color='red', icon='crosshairs', prefix='fa') # Icono de mira táctica
        ).add_to(mapa)

    nombre_mapa = "lupa_tactica_israel.html"
    mapa.save(nombre_mapa)
    print(f"\n[LUPA TÁCTICA LISTA]")
    print(f"Abra el archivo: {nombre_mapa}")

if __name__ == "__main__":
    generar_lupa()