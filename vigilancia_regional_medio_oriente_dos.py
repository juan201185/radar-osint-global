import pandas as pd
import folium
from folium.plugins import MarkerCluster
import requests
from io import StringIO
import datetime
import json
import feedparser
import random

# --- CONFIGURACIÓN ESTRATÉGICA E.T.B. ---
MAP_KEY = "c7d1ad2cb48cfb61a3b6653a1cf98ea9" 
ZONA_REGIONAL = "32,12,63,38" 

# Diccionario geográfico rápido para las zonas de alerta en Israel
ZONAS_ISRAEL = {
    "Tel Aviv": [32.0853, 34.7818],
    "Jerusalem": [31.7683, 35.2137],
    "Haifa": [32.7940, 34.9896],
    "Upper Galilee": [33.0111, 35.4386], # Norte / Frontera Líbano
    "Gaza Envelope": [31.5017, 34.4668], # Sur / Sderot
    "Ashkelon": [31.6693, 34.5715],
    "Ashdod": [31.8014, 34.6435],
    "Golan": [33.0000, 35.7000],
    "Eilat": [29.5577, 34.9519]
}

def obtener_datos_regionales(rango_dias=3):
    """Capa 1: Descarga datos de satélite VIIRS (Daños en tierra)"""
    url = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{MAP_KEY}/VIIRS_SNPP_NRT/{ZONA_REGIONAL}/{rango_dias}"
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Escaneando anomalías térmicas en Medio Oriente (NASA)...")
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            df = pd.read_csv(StringIO(response.text))
            print(f"   -> Éxito: {len(df)} anomalías térmicas detectadas en tierra.")
            return df
        else:
            print(f"   [!] Error de conexión con la NASA: {response.status_code}")
            return None
    except Exception as e:
        print(f"   [!] Error técnico satelital: {e}")
        return None

def obtener_alertas_aereas_israel():
    """Capa 2: Escáner de Alertas Antiaéreas (Vía Proxy Antibloqueo)"""
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Interceptando red de sirenas (Vía Proxy)...")
    
    # Camuflaje para el proxy
    feedparser.USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    
    # Buscamos cables de última hora (when:1d) que reporten sirenas en Israel
    url_alertas = "https://news.google.com/rss/search?q=rocket+sirens+OR+red+alert+israel+when:1d&hl=en-US&gl=US&ceid=US:en"
    
    alertas_procesadas = []
    try:
        flujo = feedparser.parse(url_alertas)
        for entrada in flujo.entries[:40]: # Tomamos los últimos 40 reportes de ataques
            texto = (entrada.title + " " + entrada.description).lower()
            
            # Asignación táctica de la zona
            coords = ZONAS_ISRAEL["Tel Aviv"]
            zona_texto = "Centro de Israel"
            
            if "galilee" in texto or "north" in texto or "lebanon" in texto or "hezbollah" in texto: 
                coords = ZONAS_ISRAEL["Upper Galilee"]
                zona_texto = "Alta Galilea / Norte"
            elif "sderot" in texto or "gaza" in texto or "south" in texto or "hamas" in texto: 
                coords = ZONAS_ISRAEL["Gaza Envelope"]
                zona_texto = "Frontera con Gaza"
            elif "ashkelon" in texto: 
                coords = ZONAS_ISRAEL["Ashkelon"]
                zona_texto = "Ascalón"
            elif "haifa" in texto: 
                coords = ZONAS_ISRAEL["Haifa"]
                zona_texto = "Haifa"
            elif "jerusalem" in texto: 
                coords = ZONAS_ISRAEL["Jerusalem"]
                zona_texto = "Jerusalén"
            elif "golan" in texto: 
                coords = ZONAS_ISRAEL["Golan"]
                zona_texto = "Altos del Golán"
            
            # Desplazamiento aleatorio para ver la lluvia de cohetes esparcida (enjambre)
            lat_offset = random.uniform(-0.15, 0.15)
            lon_offset = random.uniform(-0.15, 0.15)
            
            # Limpiamos el título para el popup
            titulo_limpio = entrada.title.split(' - ')[0]
            
            alertas_procesadas.append({
                'fecha': entrada.get('published', 'Reciente'),
                'titulo': titulo_limpio,
                'zona': zona_texto,
                'lat': coords[0] + lat_offset,
                'lon': coords[1] + lon_offset
            })
        print(f"   -> Éxito: {len(alertas_procesadas)} impactos/sirenas detectados en el espacio aéreo.")
    except Exception as e:
        print(f"   [!] Error en el proxy de sirenas: {e}")
        
    return alertas_procesadas

def generar_mapa_fusionado():
    print("\n=== INICIANDO FUSIÓN DE SENSORES E.T.B. ===")
    df_nasa = obtener_datos_regionales(3)
    alertas_israel = obtener_alertas_aereas_israel()

    # Mapa base centrado en Medio Oriente
    mapa = folium.Map(location=[31.5, 38.0], zoom_start=6, tiles='CartoDB dark_matter')
    
    # Capas (Layers) para poder encenderlas o apagarlas en el mapa
    capa_tierra = folium.FeatureGroup(name="NASA: Impactos en Tierra (Rojo)").add_to(mapa)
    capa_aire = folium.FeatureGroup(name="ISRAEL: Sirenas Antiaéreas (Azul)").add_to(mapa)

    # --- 1. PINTAR DATOS DE LA NASA (Tierra) ---
    if df_nasa is not None and not df_nasa.empty:
        alertas_criticas = df_nasa[df_nasa['bright_ti4'] > 325]
        
        for _, fila in alertas_criticas.iterrows():
            temp_c = round(fila['bright_ti4'] - 273.15, 1)
            # Extracción táctica de coordenadas
            lat_str = round(fila['latitude'], 5)
            lon_str = round(fila['longitude'], 5)
            
            info = f"""
            <div style="font-family: Arial; width: 220px;">
                <b style="color:#ff3333;">IMPACTO EN TIERRA / INCENDIO</b><br><hr>
                <b>Coordenadas:</b> {lat_str}, {lon_str}<br>
                <b>Temp:</b> {temp_c}°C<br>
                <b>Sensor:</b> NASA VIIRS<br>
                <b>Confianza:</b> {fila['confidence']}
            </div>
            """
            folium.Marker(
                location=[fila['latitude'], fila['longitude']],
                popup=folium.Popup(info, max_width=250),
                icon=folium.Icon(color='red', icon='fire', prefix='fa')
            ).add_to(capa_tierra)

    # --- 2. PINTAR ALERTAS DE SIRENAS (Aire) ---
    if alertas_israel:
        for alerta in alertas_israel:
            # Extracción táctica de coordenadas para las sirenas
            lat_alerta = round(alerta['lat'], 5)
            lon_alerta = round(alerta['lon'], 5)
            
            info = f"""
            <div style="font-family: Arial; width: 220px;">
                <b style="color:#33ccff;">INTERCEPCIÓN / SIRENA</b><br><hr>
                <b>Coordenadas (Est.):</b> {lat_alerta}, {lon_alerta}<br>
                <b>Alerta:</b> {alerta['titulo']}<br>
                <b>Zona:</b> {alerta['zona']}<br>
                <b>Hora:</b> {alerta['fecha']}
            </div>
            """
            folium.Marker(
                location=[alerta['lat'], alerta['lon']],
                popup=folium.Popup(info, max_width=250),
                icon=folium.Icon(color='blue', icon='rocket', prefix='fa')
            ).add_to(capa_aire)

    # Agregar control de capas y guardar
    folium.LayerControl().add_to(mapa)
    nombre_mapa = "radar_regional_medio_oriente.html"
    mapa.save(nombre_mapa)
    
    print(f"\n[MAPA FUSIONADO GENERADO EXITOSAMENTE]")
    print(f"Archivo guardado: {nombre_mapa}")
    print("=========================================")

if __name__ == "__main__":
    generar_mapa_fusionado()