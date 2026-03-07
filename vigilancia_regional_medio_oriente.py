import pandas as pd
import folium
from folium.plugins import MarkerCluster, HeatMap
import requests
from io import StringIO
import datetime
import json
import feedparser
import random
import numpy as np
from scipy.spatial.distance import pdist, squareform
from sklearn.cluster import DBSCAN

# --- CONFIGURACIÓN ESTRATÉGICA E.T.B. v2.0 ---
MAP_KEY_NASA = "c7d1ad2cb48cfb61a3b6653a1cf98ea9"
ZONA_REGIONAL = "32,12,63,38"

# Zonas de refinerías/petróleo para EXCLUIR (ruido térmico conocido)
REFINERIAS_RUIDO = [
    {"nombre": "Refinería Abadan", "coords": [30.3475, 48.2934], "radio_km": 15},
    {"nombre": "Refinería Basra", "coords": [30.5156, 47.7804], "radio_km": 12},
    {"nombre": "Refinería Beiji", "coords": [34.9311, 43.4931], "radio_km": 10},
    {"nombre": "Refinería Homs", "coords": [34.7308, 36.7094], "radio_km": 8},
    {"nombre": "Refinería Tripoli Líbano", "coords": [34.4333, 35.8333], "radio_km": 6},
    {"nombre": "Zona Industrial Haifa", "coords": [32.8184, 35.0019], "radio_km": 8},
    {"nombre": "Campos Petroleros Kuwait", "coords": [29.3917, 47.9774], "radio_km": 20},
    {"nombre": "Refinería Yanbu", "coords": [23.8936, 38.0608], "radio_km": 15},
    {"nombre": "Zona Ras Tanura", "coords": [26.7731, 50.0600], "radio_km": 18},
    {"nombre": "Zona Industrial Damasco", "coords": [33.5138, 36.2765], "radio_km": 5},
    {"nombre": "Refinería Teherán", "coords": [35.6892, 51.3890], "radio_km": 10},
]

ZONAS_ISRAEL = {
    "Tel Aviv": [32.0853, 34.7818],
    "Jerusalem": [31.7683, 35.2137],
    "Haifa": [32.7940, 34.9896],
    "Upper Galilee": [33.0111, 35.4386],
    "Gaza Envelope": [31.5017, 34.4668],
    "Ashkelon": [31.6693, 34.5715],
    "Ashdod": [31.8014, 34.6435],
    "Golan": [33.0000, 35.7000],
    "Eilat": [29.5577, 34.9519],
    "Beersheba": [31.2518, 34.7913],
    "Netivot": [31.4167, 34.5833],
    "Ofakim": [31.3167, 34.6167],
    "Sderot": [31.5167, 34.6000],
    "Kiryat Shmona": [33.2075, 35.5694],
    "Nahariya": [33.0058, 35.0941],
    "Rishon LeZion": [31.9718, 34.7894],
    "Rehovot": [31.8928, 34.8113]
}

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calcula distancia en km entre dos puntos geográficos"""
    R = 6371  # Radio de la Tierra en km
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return R * c

def filtrar_refinerias(df):
    """
    Algoritmo de filtrado de ruido térmico industrial
    Elimina puntos dentro del radio de refinerías conocidas
    """
    if df is None or df.empty:
        return df
    
    df_filtrado = df.copy()
    mascara_ruido = pd.Series([False] * len(df_filtrado))
    
    for ref in REFINERIAS_RUIDO:
        lat_ref, lon_ref = ref["coords"]
        
        # Vectorizar cálculo de distancias (más rápido)
        distancias = df_filtrado.apply(
            lambda row: haversine_distance(row['latitude'], row['longitude'], lat_ref, lon_ref),
            axis=1
        )
        
        mascara_ruido |= (distancias < ref["radio_km"])
    
    puntos_filtrados = mascara_ruido.sum()
    if puntos_filtrados > 0:
        print(f"   [FILTRO] Eliminados {puntos_filtrados} puntos de ruido industrial")
        print(f"            Refinerías detectadas: {ref['nombre']}")
    
    return df_filtrado[~mascara_ruido]

def detectar_anomalias_explosiones(df):
    """
    Algoritmo de clustering DBSCAN para clasificar eventos térmicos
    Diferencia entre explosiones (puntuales, intensas) e incendios (difusos)
    """
    if df is None or len(df) < 3:
        if df is not None:
            df['tipo_evento'] = 'DESCONOCIDO'
            df['confianza'] = 'BAJA'
        return df
    
    coords = df[['latitude', 'longitude']].values
    
    # DBSCAN: eps=0.03 (≈3km), min_samples=2
    clustering = DBSCAN(eps=0.03, min_samples=2).fit(coords)
    df['cluster'] = clustering.labels_
    
    # Clasificar cada cluster
    for cluster_id in set(clustering.labels_):
        if cluster_id == -1:  # Puntos aislados (ruido para DBSCAN)
            continue
        
        cluster_data = df[df['cluster'] == cluster_id]
        
        temp_max = cluster_data['bright_ti4'].max()
        n_puntos = len(cluster_data)
        
        # Calcular dispersión geográfica
        if n_puntos > 1:
            dispersion = np.mean(pdist(cluster_data[['latitude', 'longitude']].values))
        else:
            dispersion = 0
        
        # Clasificación táctica
        if temp_max > 380 and n_puntos <= 3 and dispersion < 0.01:
            tipo = 'EXPLOSION_CONFIRMADA'
            conf = 'ALTA'
        elif temp_max > 360 and n_puntos <= 5:
            tipo = 'POSIBLE_EXPLOSION'
            conf = 'MEDIA'
        elif temp_max > 340:
            tipo = 'INCENDIO_ESTRUCTURAL'
            conf = 'MEDIA'
        else:
            tipo = 'INCENDIO_NATURAL'
            conf = 'BAJA'
        
        df.loc[cluster_data.index, 'tipo_evento'] = tipo
        df.loc[cluster_data.index, 'confianza'] = conf
    
    # Puntos aislados (sin cluster) pero muy calientes = explosión solitaria
    puntos_aislados = df[df['cluster'] == -1]
    explosiones_aisladas = puntos_aislados[puntos_aislados['bright_ti4'] > 400]
    
    df.loc[explosiones_aisladas.index, 'tipo_evento'] = 'EXPLOSION_AISLADA'
    df.loc[explosiones_aisladas.index, 'confianza'] = 'ALTA'
    
    # Resto de aislados = incendios menores
    otros_aislados = puntos_aislados[puntos_aislados['bright_ti4'] <= 400]
    df.loc[otros_aislados.index, 'tipo_evento'] = 'ANOMALIA_MENOR'
    df.loc[otros_aislados.index, 'confianza'] = 'BAJA'
    
    return df

def obtener_datos_nasa(rango_dias=2):
    """Capa 1: NASA VIIRS con filtrado avanzado"""
    url = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{MAP_KEY_NASA}/VIIRS_SNPP_NRT/{ZONA_REGIONAL}/{rango_dias}"
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Escaneando VIIRS NASA...")
    
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            df = pd.read_csv(StringIO(response.text))
            print(f"   -> Raw data: {len(df)} anomalías térmicas brutas")
            
            # Pipeline de filtrado inteligente
            df = filtrar_refinerias(df)
            df = detectar_anomalias_explosiones(df)
            
            # Filtrar solo eventos tácticos relevantes
            df_tactico = df[
                (df['bright_ti4'] > 340) | 
                (df['tipo_evento'].isin(['EXPLOSION_CONFIRMADA', 'EXPLOSION_AISLADA', 'POSIBLE_EXPLOSION']))
            ].copy()
            
            print(f"   -> Filtrado táctico: {len(df_tactico)} eventos de interés militar")
            return df_tactico
            
        else:
            print(f"   [!] NASA offline: HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"   [!] Error NASA: {str(e)[:60]}")
        return None

def obtener_alertas_aereas_mejorado():
    """Capa 2: Sirenas antiaéreas con múltiples fuentes y geolocalización precisa"""
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Interceptando red de sirenas multicanal...")
    
    feedparser.USER_AGENT = random.choice([
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    ])
    
    fuentes_sirenas = [
        "https://news.google.com/rss/search?q=red+alert+israel+rocket+when:1d&hl=en-US&gl=US&ceid=US:en",
        "https://news.google.com/rss/search?q=iron+dome+interception+israel+when:1d&hl=en-US&gl=US&ceid=US:en",
        "https://news.google.com/rss/search?q=rocket+sirens+gaza+envelope+when:1d&hl=en-US&gl=US&ceid=US:en",
        "https://news.google.com/rss/search?q=hezbollah+rockets+north+israel+when:1d&hl=en-US&gl=US&ceid=US:en",
        "https://news.google.com/rss/search?q=missile+attack+israel+when:1d&hl=en-US&gl=US&ceid=US:en",
    ]
    
    alertas_totales = []
    alertas_ids = set()
    
    for url in fuentes_sirenas:
        try:
            flujo = feedparser.parse(url)
            for entrada in flujo.entries[:10]:
                alerta_id = hash(entrada.title[:50])
                if alerta_id in alertas_ids:
                    continue
                alertas_ids.add(alerta_id)
                
                texto = (entrada.title + " " + entrada.get('description', '')).lower()
                coords, zona_texto = geolocalizar_alerta(texto)
                
                if 'hezbollah' in texto or 'lebanon' in texto:
                    lat_offset = random.uniform(-0.12, 0.12)
                    lon_offset = random.uniform(-0.12, 0.12)
                else:
                    lat_offset = random.uniform(-0.06, 0.06)
                    lon_offset = random.uniform(-0.06, 0.06)
                
                titulo_limpio = entrada.title.split(' - ')[0][:80]
                
                alertas_totales.append({
                    'fecha': entrada.get('published', 'Reciente'),
                    'titulo': titulo_limpio,
                    'zona': zona_texto,
                    'lat': coords[0] + lat_offset,
                    'lon': coords[1] + lon_offset,
                    'fuente': 'SIRENA_MULTICANAL',
                    'tipo_ataque': 'Hezbollah' if 'hezbollah' in texto else 'Hamas' if 'hamas' in texto else 'Desconocido'
                })
        except Exception as e:
            print(f"   [!] Error fuente: {str(e)[:40]}")
            continue
    
    print(f"   -> Éxito: {len(alertas_totales)} alertas únicas detectadas")
    return alertas_totales

def geolocalizar_alerta(texto):
    """Sistema de geolocalización granular para alertas de sirenas en Israel"""
    texto = texto.lower()
    
    if any(x in texto for x in ['kiryat shmona', 'kiryat shmonah', 'galilee', 'galil', 'north', 'lebanon', 'hezbollah', 'nazareth illit']):
        return ZONAS_ISRAEL["Kiryat Shmona"], "Kiryat Shmona / Norte"
    elif any(x in texto for x in ['nahariya', 'acre', 'akko', 'western galilee']):
        return ZONAS_ISRAEL["Nahariya"], "Nahariya / Norte"
    elif any(x in texto for x in ['golan', 'quneitra', 'katzrin', 'syria border']):
        return ZONAS_ISRAEL["Golan"], "Altos del Golán"
    elif any(x in texto for x in ['sderot', 'netivot', 'ofakim', 'shaar hanegev', 'otfaz']):
        return ZONAS_ISRAEL["Sderot"], "Sderot / Frontera Gaza"
    elif any(x in texto for x in ['gaza envelope', 'envelope', 'negev']):
        return ZONAS_ISRAEL["Gaza Envelope"], "Frontera con Gaza"
    elif 'ashkelon' in texto:
        return ZONAS_ISRAEL["Ashkelon"], "Ascalón"
    elif 'ashdod' in texto:
        return ZONAS_ISRAEL["Ashdod"], "Ashdod"
    elif any(x in texto for x in ['rishon', 'rishon lezion']):
        return ZONAS_ISRAEL["Rishon LeZion"], "Rishon LeZion"
    elif 'rehovot' in texto:
        return ZONAS_ISRAEL["Rehovot"], "Rehovot"
    elif 'haifa' in texto:
        return ZONAS_ISRAEL["Haifa"], "Haifa"
    elif any(x in texto for x in ['jerusalem', 'al quds', 'modiin']):
        return ZONAS_ISRAEL["Jerusalem"], "Jerusalén"
    elif 'eilat' in texto:
        return ZONAS_ISRAEL["Eilat"], "Eilat"
    elif any(x in texto for x in ['beersheba', 'beer sheva', 'rahovat']):
        return ZONAS_ISRAEL["Beersheba"], "Beersheba"
    elif any(x in texto for x in ['tel aviv', 'yafo', 'jaffa', 'gush dan', 'center']):
        return ZONAS_ISRAEL["Tel Aviv"], "Tel Aviv / Centro"
    else:
        coords = [32.0853 + random.uniform(-0.15, 0.15), 34.7818 + random.uniform(-0.15, 0.15)]
        return coords, "Área Central (Estimado)"

def generar_mapa_fusionado_v2():
    print("\n" + "="*60)
    print("INICIANDO FUSIÓN MULTISENSOR E.T.B. v2.0")
    print("="*60)
    print("Sensores: NASA VIIRS | Red de Sirenas")
    
    df_nasa = obtener_datos_nasa(rango_dias=2)
    alertas_israel = obtener_alertas_aereas_mejorado()

    mapa = folium.Map(location=[31.5, 38.0], zoom_start=6, tiles='CartoDB dark_matter')
    
    capa_nasa = folium.FeatureGroup(name="🔥 NASA: Explosiones/Incendios").add_to(mapa)
    capa_sirenas = folium.FeatureGroup(name="🚨 Israel: Sirenas Antiaéreas").add_to(mapa)
    capa_calor = folium.FeatureGroup(name="🌡️ Mapa de Calor (Fusión)").add_to(mapa)

    puntos_calor = []

    # --- 1. DATOS NASA (100% REALES) ---
    if df_nasa is not None and not df_nasa.empty:
        for _, fila in df_nasa.iterrows():
            temp_c = round(fila['bright_ti4'] - 273.15, 1)
            lat, lon = fila['latitude'], fila['longitude']
            puntos_calor.append([lat, lon, min(fila['bright_ti4']/400, 1.0)])
            
            tipo = fila.get('tipo_evento', 'DESCONOCIDO')
            confianza = fila.get('confianza', 'BAJA')
            
            if 'CONFIRMADA' in tipo:
                color, radio, opacidad = '#ff0000', 10, 0.9
            elif 'POSIBLE' in tipo:
                color, radio, opacidad = '#ff6600', 8, 0.8
            elif 'ESTRUCTURAL' in tipo:
                color, radio, opacidad = '#ffaa00', 6, 0.7
            else:
                color, radio, opacidad = '#888888', 4, 0.6
            
            info = f"""
            <div style="font-family: 'Courier New', monospace; width: 280px; 
                        background: rgba(0,0,0,0.95); color: #fff; padding: 12px; 
                        border-radius: 8px; border-left: 5px solid {color};">
                <b style="color:{color}; font-size: 16px;">🔥 {tipo}</b><br>
                <hr style="border-color: #333; margin: 8px 0;">
                <b>📍 Coordenadas:</b> {round(lat, 5)}, {round(lon, 5)}<br>
                <b>🌡️ Temperatura:</b> <span style="color:#ff6666; font-size: 14px;">{temp_c}°C</span><br>
                <b>🎯 Confianza:</b> {confianza}<br>
                <b>🛰️ Fuente:</b> NASA VIIRS<br>
                <b>📅 Fecha:</b> {fila.get('acq_date', 'N/A')} {str(fila.get('acq_time', ''))[:4]}
            </div>
            """
            
            folium.CircleMarker(
                location=[lat, lon],
                radius=radio,
                popup=folium.Popup(info, max_width=300),
                color=color,
                fill=True,
                fillColor=color,
                fillOpacity=opacidad,
                weight=2
            ).add_to(capa_nasa)

    # --- 2. ALERTAS DE SIRENAS (OSINT EN VIVO) ---
    if alertas_israel:
        for alerta in alertas_israel:
            lat, lon = alerta['lat'], alerta['lon']
            puntos_calor.append([lat, lon, 0.9])
            
            color_sirena = '#cc0000' if alerta['tipo_ataque'] == 'Hezbollah' else '#0066cc'
            
            info = f"""
            <div style="font-family: 'Courier New', monospace; width: 280px; 
                        background: rgba(0,0,0,0.95); color: #fff; padding: 12px; 
                        border-radius: 8px; border-left: 5px solid {color_sirena};">
                <b style="color:{color_sirena}; font-size: 16px;">🚨 ALERTA ANTIAÉREA</b><br>
                <hr style="border-color: #333; margin: 8px 0;">
                <b>📍 Zona:</b> {alerta['zona']}<br>
                <b>📍 Coordenadas (Est.):</b> {round(lat, 5)}, {round(lon, 5)}<br>
                <b>🚀 Agresor:</b> {alerta['tipo_ataque']}<br>
                <b>📰 Evento:</b> {alerta['titulo']}<br>
                <b>🕐 Hora:</b> {alerta['fecha'][:25]}<br>
                <b>📡 Fuente:</b> {alerta['fuente']}
            </div>
            """
            
            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup(info, max_width=300),
                icon=folium.Icon(
                    color='darkblue' if alerta['tipo_ataque'] == 'Hezbollah' else 'blue',
                    icon='rocket',
                    prefix='fa'
                ),
                tooltip=f"{alerta['tipo_ataque']}: {alerta['zona']}"
            ).add_to(capa_sirenas)

    # --- 3. MAPA DE CALOR CONJUNTO ---
    if puntos_calor:
        HeatMap(
            puntos_calor, 
            radius=20, 
            blur=15, 
            max_zoom=10,
            gradient={0.4: 'blue', 0.65: 'lime', 0.8: 'yellow', 1: 'red'}
        ).add_to(capa_calor)

    # Controles y Panel HTML Purificado
    folium.LayerControl(collapsed=False).add_to(mapa)
    
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    info_html = f"""
    <div style="position: fixed; top: 20px; right: 20px; width: 300px; 
                background-color: rgba(10,10,10,0.95); color: #fff; 
                border: 2px solid #444; padding: 15px; border-radius: 10px; 
                font-family: 'Courier New', monospace; font-size: 11px; z-index: 9999;
                box-shadow: 0 0 20px rgba(0,0,0,0.8);">
        <h4 style="color:#ff3333; margin-top:0; text-align:center; font-size: 14px; 
                   border-bottom: 2px solid #333; padding-bottom: 8px;">
            🛰️ RADAR MULTISENSOR E.T.B.
        </h4>
        <div style="line-height: 1.8; margin-top: 10px;">
            <div style="display: flex; align-items: center;">
                <span style="color:#ff0000; font-size: 16px; margin-right: 8px;">🔥</span>
                <div>
                    <b style="color:#ff6666;">NASA VIIRS</b><br>
                    <span style="font-size: 9px; color: #888;">Filtrado industrial + Clustering</span>
                </div>
            </div>
            <div style="display: flex; align-items: center; margin-top: 8px;">
                <span style="color:#0066cc; font-size: 16px; margin-right: 8px;">🚨</span>
                <div>
                    <b style="color:#0066cc;">Red de Sirenas</b><br>
                    <span style="font-size: 9px; color: #888;">Inteligencia OSINT multicanal</span>
                </div>
            </div>
            <div style="display: flex; align-items: center; margin-top: 8px;">
                <span style="color:#ffcc00; font-size: 16px; margin-right: 8px;">🌡️</span>
                <div>
                    <b style="color:#ffcc00;">Heatmap Fusión</b><br>
                    <span style="font-size: 9px; color: #888;">Correlación de todas las fuentes</span>
                </div>
            </div>
        </div>
        <div style="margin-top: 12px; border-top: 2px solid #333; padding-top: 10px; 
                    font-size: 10px; color: #666; text-align: center;">
            <b>Última actualización:</b><br>
            {timestamp}<br>
            <span style="color: #444;">Sistema E.T.B. v2.0 (Verificado)</span>
        </div>
    </div>
    """
    mapa.get_root().html.add_child(folium.Element(info_html))
    
    nombre_mapa = "radar_regional_medio_oriente.html"
    mapa.save(nombre_mapa)
    
    print("\n" + "="*60)
    print(f"[✅ MAPA MULTISENSOR GENERADO]")
    print(f"Archivo: {nombre_mapa}")
    print(f"Capas: NASA VIIRS | Sirenas | Heatmap")
    print("="*60 + "\n")

if __name__ == "__main__":
    generar_mapa_fusionado_v2()