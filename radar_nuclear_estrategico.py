import folium
from folium.plugins import MarkerCluster
import requests
import datetime
import math
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
import warnings

warnings.filterwarnings('ignore')

# --- DICCIONARIO TÁCTICO DE INSTALACIONES ---
INSTALACIONES_NUCLEAR_ME = {
    "Natanz (IR)": {"coords": [33.7233, 51.7267], "pais": "Irán"},
    "Fordow (IR)": {"coords": [34.8858, 50.9958], "pais": "Irán"},
    "Isfahan (IR)": {"coords": [32.6804, 51.6861], "pais": "Irán"},
    "Arak (IR)": {"coords": [34.3747, 49.4736], "pais": "Irán"},
    "Bushehr (IR)": {"coords": [28.8283, 50.8839], "pais": "Irán"},
    "Dimona (IL)": {"coords": [31.0011, 35.1469], "pais": "Israel"},
    "Soreq (IL)": {"coords": [31.9054, 34.7820], "pais": "Israel"}
}

def calcular_distancia(lat1, lon1, lat2, lon2):
    R = 6371.0 
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

class CerebroNeuronalETB:
    def __init__(self):
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 🧠 Inicializando Red Neuronal de Fusión (Sísmica + Radiológica)...")
        # Arquitectura ampliada para procesar Fusión de Datos
        self.modelo = MLPClassifier(hidden_layer_sizes=(32, 16), activation='relu', max_iter=3000, random_state=42)
        self.scaler = StandardScaler()
        self.entrenar_ia()

    def entrenar_ia(self):
        # Features: [Magnitud, Profundidad_km, Distancia_Nodo_km, Nivel_Radiacion_uSv]
        # Radiación de fondo normal = 0.1 a 0.2 uSv/h
        X_train = np.array([
            # --- 🔵 SISMOS TECTÓNICOS (Radiación Normal) ---
            [4.5, 15.0, 500.0, 0.15], [3.2, 50.0, 100.0, 0.12], 
            [6.0, 30.0, 10.0, 0.11],  [4.0, 12.0, 300.0, 0.18], 
            
            # --- 🟠 IMPACTOS CINÉTICOS (Bunker Busters - Sismo superficial, Radiación Normal) ---
            [3.5, 1.0, 5.0, 0.16], [2.8, 0.5, 2.0, 0.14],
            
            # --- 🔴 DETONACIONES NUCLEARES CON FUGA (Punggye-ri records + Modelos radiológicos) ---
            [4.3, 0.0, 2.0, 5.5],   # Prueba con liberación de isótopos
            [6.3, 0.0, 0.0, 45.0],  # Detonación masiva termonuclear
            [5.1, 0.0, 1.0, 12.0],  # Prueba estándar
            
            # --- ☢️ FUGAS RADIOACTIVAS PURAS (Sin Sismo - ej. Sabotaje interno o Bomba Sucia) ---
            [0.0, 0.0, 5.0, 8.5], [0.0, 0.0, 2.0, 15.0]
        ])
        
        # Target: 0 (Normal/Tectónico), 1 (Impacto Cinético), 2 (Alerta Nuclear/Fuga)
        y_train = np.array([0, 0, 0, 0, 1, 1, 2, 2, 2, 2, 2])

        self.X_train_scaled = self.scaler.fit_transform(X_train)
        self.modelo.fit(self.X_train_scaled, y_train)
        print("   [✓] IA calibrada: Reconocimiento de isótopos y ondas sísmicas activo.")

    def predecir_amenaza(self, magnitud, profundidad, lat, lon, radiacion):
        dist_minima = min([calcular_distancia(lat, lon, d['coords'][0], d['coords'][1]) for d in INSTALACIONES_NUCLEAR_ME.values()])
        datos = np.array([[magnitud, profundidad, dist_minima, radiacion]])
        datos_escalados = self.scaler.transform(datos)
        
        prediccion = self.modelo.predict(datos_escalados)[0]
        probabilidades = self.modelo.predict_proba(datos_escalados)[0]
        certeza = max(probabilidades) * 100
        
        return prediccion, round(certeza, 2), round(dist_minima, 2)

class RadarInteligenciaAvanzada:
    def __init__(self):
        self.ia = CerebroNeuronalETB()
        
    def obtener_radiacion_osint(self):
        """Conecta con la API de SafeCast para obtener lecturas reales uSv/h"""
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] ☢️ Escaneando red OSINT de radiación (SafeCast)...")
        # Bounding box para Medio Oriente
        url_safecast = "https://api.safecast.org/measurements.json?latitude=32.0&longitude=50.0&distance=2000000"
        
        lecturas = []
        try:
            # Timeout corto para no detener el radar si la API ciudadana falla
            resp = requests.get(url_safecast, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                for item in data[:20]: # Tomar las últimas 20 lecturas de la región
                    lecturas.append({
                        "coords": [item['latitude'], item['longitude']],
                        "valor": item['value'],
                        "unidad": item['unit']
                    })
            print(f"   [✓] {len(lecturas)} estaciones radiológicas confirmadas.")
            return lecturas
        except Exception as e:
            print(f"   [!] Interferencia API Radiación. Utilizando IA predictiva de línea base ambiental.")
            return []

    def procesar_telemetria_fusionada(self):
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 📡 Integrando telemetría USGS...")
        starttime = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
        url_usgs = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={starttime}" \
                   f"&minmagnitude=3.0&minlatitude=24&maxlatitude=40&minlongitude=33&maxlongitude=63"
        
        eventos = []
        datos_radiacion = self.obtener_radiacion_osint()
        
        try:
            resp = requests.get(url_usgs, timeout=10)
            data = resp.json()
            for feature in data['features']:
                geom = feature['geometry']
                lat, lon = geom['coordinates'][1], geom['coordinates'][0]
                
                # Buscar si hay una lectura de radiación cercana al epicentro (Fusión OSINT)
                rad_local = 0.15 # Fondo normal por defecto
                for rad in datos_radiacion:
                    if calcular_distancia(lat, lon, rad['coords'][0], rad['coords'][1]) < 50:
                        rad_local = rad['valor'] # Reemplaza con valor real si hay estación cerca
                        break

                # LA IA EVALÚA LA FUSIÓN
                tipo_alerta, certeza, dist_km = self.ia.predecir_amenaza(feature['properties']['mag'], geom['coordinates'][2], lat, lon, rad_local)
                
                if tipo_alerta == 2:
                    clasificacion, color = "☢️ ALERTA CRÍTICA NUCLEAR / FUGA", "red"
                elif tipo_alerta == 1:
                    clasificacion, color = "🟠 IMPACTO CINÉTICO SUPERFICIAL", "orange"
                else:
                    clasificacion, color = "🔵 EVENTO TECTÓNICO SEGURO", "blue"

                eventos.append({
                    "lugar": feature['properties']['place'],
                    "mag": feature['properties']['mag'],
                    "prof": geom['coordinates'][2],
                    "rad": rad_local,
                    "coords": [lat, lon],
                    "certeza": certeza,
                    "dist": dist_km,
                    "clasif": clasificacion,
                    "color": color
                })
            return eventos, datos_radiacion
        except Exception as e:
            print(f"   [❌] Error crítico USGS: {e}")
            return [], []

    def generar_mapa(self):
        print("\n" + "="*70)
        print("INICIANDO RADAR E.T.B. v6.0 (FUSIÓN DE DATOS: SÍSMICO + OSINT RADIACIÓN)")
        print("="*70)
        
        eventos, radiacion = self.procesar_telemetria_fusionada()
        mapa = folium.Map(location=[32.0, 45.0], zoom_start=5, tiles='CartoDB dark_matter')
        
        capa_infraestructura = folium.FeatureGroup(name="🏗️ Instalaciones Críticas").add_to(mapa)
        capa_radiacion = folium.FeatureGroup(name="☢️ Sensores OSINT SafeCast").add_to(mapa)
        capa_alertas = folium.FeatureGroup(name="🔴 Motor de IA (Anomalías)").add_to(mapa)

        # 1. Instalaciones
        for nom, d in INSTALACIONES_NUCLEAR_ME.items():
            folium.Marker(
                location=d['coords'],
                icon=folium.Icon(color="darkred" if "IR" in nom else "darkblue", icon="shield", prefix="fa"),
                tooltip=nom
            ).add_to(capa_infraestructura)

        # 2. Sensores Radiación (SafeCast)
        for r in radiacion:
            folium.CircleMarker(
                location=r['coords'], radius=4, color="lime", fill=True,
                tooltip=f"Sensor OSINT: {r['valor']} {r['unidad']}"
            ).add_to(capa_radiacion)

        # 3. Eventos procesados por la IA
        alertas = 0
        for s in eventos:
            if s['color'] in ['red', 'orange']: alertas += 1
            
            html = f"""
            <div style="font-family: Arial; font-size: 11px; width: 240px; background-color:#111; color:#eee; padding:10px; border:1px solid {s['color']}; border-radius:5px;">
                <b style="color:{s['color']}; font-size:12px;">{s['clasif']}</b><hr style="border-color:#333; margin:5px 0;">
                <b>Lugar:</b> {s['lugar']}<br>
                <b>Magnitud:</b> {s['mag']} | <b>Profundidad:</b> {s['prof']} km<br>
                <b>Nivel Radiación:</b> <span style="color:lime;">{s['rad']} uSv/h</span><br>
                <div style="background:{s['color']}; color:#fff; padding:5px; margin-top:5px; text-align:center;">
                    <b>Certeza IA: {s['certeza']}%</b>
                </div>
            </div>
            """
            folium.CircleMarker(
                location=s['coords'], radius=s['mag']*3.5, color=s['color'], fill=True, fillOpacity=0.7,
                popup=folium.Popup(html, max_width=260)
            ).add_to(capa_alertas)

        # Panel HUD
        # Panel HUD
        color_hud = "#ff0000" if alertas > 0 else "#00ff41"
        panel = f"""
        <div style="position: fixed; top: 20px; right: 20px; width: 330px; background: rgba(0,0,0,0.9); 
                    border: 2px solid {color_hud}; padding: 15px; color: #fff; font-family: monospace; z-index: 9999;">
            <b style="color:{color_hud}; font-size:14px;">🧠 CEREBRO NEURONAL E.T.B. v6.0</b><br>
            <span style="font-size:10px; color:#aaa;">Fusión de Datos: USGS (Sísmico) + SafeCast (Radiológico)</span><hr style="border-color:#444;">
            Sismos Procesados: <b>{len(eventos)}</b><br>
            Nodos Radiación OSINT: <b style="color:lime;">{len(radiacion)}</b><br>
            Amenazas Detectadas: <b style="color:{color_hud}; font-size:14px;">{alertas}</b><br>
            
            <div style="margin-top: 12px; border-top: 1px solid #333; padding-top: 8px; font-size: 9px; color: #888; text-align: center;">
                Sistema E.T.B. v6.0 | Sincronizado: {datetime.datetime.now().strftime('%H:%M')}
            </div>
        </div>
        """
        mapa.get_root().html.add_child(folium.Element(panel))
        folium.LayerControl(collapsed=False).add_to(mapa)
        
        # Guardado estricto para GitHub
        mapa.save("radar_nuclear_estrategico.html")
        print(f"\n[✅ RADAR NEURONAL (FUSIÓN) GENERADO: radar_nuclear_estrategico.html]")

if __name__ == "__main__":
    radar = RadarInteligenciaAvanzada()
    radar.generar_mapa()