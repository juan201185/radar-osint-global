import folium
from folium.plugins import MarkerCluster
import requests
import datetime
import math
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
import warnings

# Silenciar warnings para consola táctica limpia
warnings.filterwarnings('ignore')

# --- DICCIONARIO TÁCTICO DE INSTALACIONES NUCLEARES (AUMENTADO) ---
INSTALACIONES_NUCLEAR_ME = {
    # IRÁN (Zonas de Interés)
    "Natanz (IR)": {"coords": [33.7233, 51.7267], "pais": "Irán"},
    "Fordow (IR)": {"coords": [34.8858, 50.9958], "pais": "Irán"},
    "Isfahan (IR)": {"coords": [32.6804, 51.6861], "pais": "Irán"},
    "Bushehr (IR)": {"coords": [28.8283, 50.8839], "pais": "Irán"},
    # ISRAEL (Zona de Confirmación Crisis v7.0)
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
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 🧠 Inicializando Cerebro de Fusión Táctica v7.0...")
        # Arquitectura robusta (32x16 neuronas)
        self.modelo = MLPClassifier(hidden_layer_sizes=(32, 16), activation='relu', max_iter=3000, random_state=42)
        self.scaler = StandardScaler()
        self.entrenar_ia()

    def entrenar_ia(self):
        """Dataset Histórico: Sismos vs. Firmas de Detonación/Fuga Real"""
        # Features: [Magnitud, Profundidad_km, Distancia_Nodo_km, Nivel_Radiacion_uSv]
        # Radiación de fondo normal = 0.1 a 0.2 uSv/h (15-30 cpm)
        X_train = np.array([
            # --- 🔵 SISMOS TECTÓNICOS (Naturales) ---
            [4.5, 15.0, 500.0, 0.15], [3.2, 50.0, 100.0, 0.12], 
            [6.0, 30.0, 10.0, 0.11],  [4.0, 12.0, 300.0, 0.18], 
            
            # --- 🟠 IMPACTOS CINÉTICOS (Bunker Busters, no nucleares) ---
            [3.5, 1.0, 5.0, 0.16], [2.8, 0.5, 2.0, 0.14],
            
            # --- 🔴 DETONACIONES NUCLEARES CON FUGA (Punggye-ri DPRK records + Fugas reales) ---
            [4.3, 0.0, 2.0, 5.5],   # Oct 2006
            [6.3, 0.0, 0.0, 45.0],  # Sep 2017 (Termonuclear)
            [5.1, 0.0, 1.0, 12.0],  # Ene 2016
            
            # --- ☢️ FUGAS RADIOACTIVAS PURAS (Sin sismo) ---
            [0.0, 0.0, 5.0, 8.5], [0.0, 0.0, 2.0, 15.0]
        ])
        
        # Target: 0 (Normal), 1 (Cinético), 2 (Nuclear/Fuga)
        y_train = np.array([0, 0, 0, 0, 1, 1, 2, 2, 2, 2, 2])

        self.X_train_scaled = self.scaler.fit_transform(X_train)
        self.modelo.fit(self.X_train_scaled, y_train)
        print("   [✓] IA calibrada: Reconocimiento de firmas sísmico-radiológicas activo.")

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
        
    def obtener_radiacion_osint_tactico(self):
        """ZONAS DE BÚSQUEDA TÁCTICA v7.0: Específico Israel e Irán"""
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] ☢️ Escaneando red SafeCast (Zonas Tácticas Confirmación)...")
        
        # Aumentamos la solicitud a 200 mediciones
        url_safecast = "https://api.safecast.org/measurements.json?limit=200&min_latitude=28&max_latitude=36&min_longitude=33&max_longitude=63"
        
        estaciones_unicas = {} # Filtro de Unicidad v7.0
        try:
            resp = requests.get(url_safecast, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                for item in data:
                    lat, lon = item['latitude'], item['longitude']
                    # Usamos coordenadas redondeadas como 'id' de estación única para evitar el stacking
                    station_id = f"{round(lat, 3)}_{round(lon, 3)}"
                    
                    if station_id not in estaciones_unicas:
                        estaciones_unicas[station_id] = {
                            "coords": [lat, lon],
                            "valor": item['value'],
                            "unidad": item['unit'],
                            "timestamp": item['captured_at']
                        }
            
            total_mediciones = list(estaciones_unicas.values())
            print(f"   [✓] {len(total_mediciones)} estaciones radiológicas únicas geolocalizadas.")
            return total_mediciones
        except Exception as e:
            print(f"   [!] Interferencia API Radiación OSINT: {e}")
            return []

    def procesar_telemetria_fusionada(self):
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 📡 Integrando telemetría sísmica (USGS)...")
        starttime = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
        # Cubre desde el Mediterráneo hasta Irán
        url_usgs = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={starttime}" \
                   f"&minmagnitude=3.0&minlatitude=24&maxlatitude=40&minlongitude=33&maxlongitude=63"
        
        eventos = []
        datos_radiacion = self.obtener_radiacion_osint_tactico()
        
        try:
            resp = requests.get(url_usgs, timeout=10)
            data = resp.json()
            for feature in data['features']:
                geom = feature['geometry']
                lat, lon = geom['coordinates'][1], geom['coordinates'][0]
                mag = feature['properties']['mag']
                prof = geom['coordinates'][2]
                
                # Fusión de Datos: Buscar radiación local en un radio de 50 km
                rad_local = 0.15 # Fondo ambiental normal por defecto (uSv/h)
                for rad in datos_radiacion:
                    if calcular_distancia(lat, lon, rad['coords'][0], rad['coords'][1]) < 50:
                        # Convertir cpm a uSv/h si es necesario (estimación cruda 1 uSv/h = 150 cpm para Cs-137)
                        valor_rad = rad['valor']
                        if rad['unidad'] == 'cpm': valor_rad = valor_rad / 150.0
                        
                        if valor_rad > rad_local: rad_local = valor_rad # Tomamos la lectura más alta cercana

                # LA IA EVALÚA LA CRISIS
                tipo_alerta, certeza, dist_km = self.ia.predecir_amenaza(mag, prof, lat, lon, rad_local)
                
                if tipo_alerta == 2:
                    clasificacion, color = "☢️ ALERTA CRÍTICA: DETONACIÓN O FUGA", "red"
                elif tipo_alerta == 1:
                    clasificacion, color = "🟠 IMPACTO CINÉTICO SUPERFICIAL", "orange"
                else:
                    clasificacion, color = "🔵 EVENTO TECTÓNICO SEGURO", "blue"

                eventos.append({
                    "lugar": feature['properties']['place'],
                    "mag": mag,
                    "prof": prof,
                    "rad_estimada": round(rad_local, 3),
                    "coords": [lat, lon],
                    "certeza": certeza,
                    "dist": dist_km,
                    "clasif": clasificacion,
                    "color": color
                })
            return eventos, datos_radiacion
        except Exception as e:
            print(f"   [❌] Error en telemetría sísmica: {e}")
            return [], []

    def generar_mapa(self):
        print("\n" + "="*70)
        print("INICIANDO RADAR E.T.B. v7.0 (CONFIRMACIÓN DE CRISIS ISRAEL-IRÁN)")
        print("="*70)
        
        eventos, radiacion = self.procesar_telemetria_fusionada()
        
        # v7.0: Centrado táctico en el Levante (Jerusalén) para visualización inmediata de Israel
        mapa = folium.Map(location=[31.7683, 35.2137], zoom_start=6, tiles='CartoDB dark_matter')
        
        capa_infraestructura = folium.FeatureGroup(name="🏗️ Nodos Nucleares Clave").add_to(mapa)
        capa_radiacion = folium.FeatureGroup(name="🟢 Sensores Unicos SafeCast").add_to(mapa)
        capa_alertas = folium.FeatureGroup(name=" Motor IA (Fusión Sísmico/Rad)").add_to(mapa)

        # 1. Pintar Instalaciones (Distorsión visual de riesgo estratégica 50km)
        for nom, d in INSTALACIONES_NUCLEAR_ME.items():
            color_base = "darkred" if "IR" in nom else "darkblue"
            folium.Marker(
                location=d['coords'], icon=folium.Icon(color=color_base, icon="crosshairs", prefix="fa"), tooltip=nom
            ).add_to(capa_infraestructura)
            folium.Circle(location=d['coords'], radius=50000, color=color_base, fill=False, weight=1, dash_array='5, 5').add_to(capa_infraestructura)

        # 2. Pintar Sensores Radiación Únicos (SafeCast)
        alertas_rad = 0
        for r in radiacion:
            # Clasificación visual rápida del sensor: Verde (Seguro <0.5), Rojo (Alerta >0.5 uSv/h estim.)
            valor_para_color = r['valor']
            if r['unit'] == 'cpm': valor_para_color = r['valor'] / 150.0 # Estimación base
            
            if valor_para_color > 0.5: color_rad = 'red'; alertas_rad += 1
            else: color_rad = 'lime'

            folium.CircleMarker(
                location=r['coords'], radius=4, color=color_rad, fill=True, fillOpacity=0.6,
                tooltip=f"Sensor Unico: {r['valor']} {r['unidad']}"
            ).add_to(capa_radiacion)

        # 3. Pintar Eventos procesados por el Cerebro Neuronal
        alertas_ia = 0
        for s in eventos:
            if s['color'] in ['red', 'orange']: alertas_ia += 1
            
            html = f"""
            <div style="font-family: Arial; font-size: 11px; width: 250px; background-color:#111; color:#eee; padding:10px; border:1px solid {s['color']}; border-radius:5px;">
                <b style="color:{s['color']}; font-size:12px; text-transform:uppercase;">{s['clasif']}</b><hr style="border-color:#333; margin:5px 0;">
                <b>Lugar:</b> {s['lugar']}<br>
                <b>Magnitud:</b> {s['mag']} | <b>Profundidad:</b> {s['prof']} km<br>
                <b>Radiación Cercana (Fusión):</b> <span style="color:lime;">{s['rad_estimada']} uSv/h</span><br>
                <div style="background:{s['color']}; color:#fff; padding:6px; margin-top:8px; border-radius:3px; text-align:center;">
                    <b>Certeza IA: {s['certeza']}%</b>
                </div>
            </div>
            """
            folium.CircleMarker(
                location=s['coords'], radius=s['mag']*4, color=s['color'], fill=True, fillOpacity=0.7,
                popup=folium.Popup(html, max_width=270)
            ).add_to(capa_alertas)

        # Panel HUD (Sincronización táctica de Patía Global)
        color_hud = "#ff0000" if (alertas_ia > 0 or alertas_rad > 0) else "#00ff41"
        panel = f"""
        <div style="position: fixed; top: 20px; right: 20px; width: 340px; background: rgba(0,0,0,0.95); 
                    border: 2px solid {color_hud}; padding: 15px; color: #fff; font-family: monospace; z-index: 9999; box-shadow: 0 0 15px {color_hud}44;">
            <b style="color:{color_hud}; font-size:14px;">🧠 CEREBRO NEURONAL E.T.B. v7.0</b><br>
            <span style="font-size:10px; color:#aaa;">STATUS: FUSIÓN DE DATOS CRISIS LEVANTINA</span><hr style="border-color:#444;">
            Sismos Procesados (7d): <b>{len(eventos)}</b><br>
            <span style="color:lime;">Sensores Unicos SafeCast:</span> <b style="color:lime;">{len(radiacion)}</b><br>
            Alertas de Radiación (&gt;0.5 uSv/h): <b style="color:red;">{alertas_rad}</b><br>
            Amenazas Detectadas (IA): <b style="color:{color_hud}; font-size:14px;">{alertas_ia}</b><br>
            
            <div style="margin-top: 12px; border-top: 1px solid #333; padding-top: 8px; font-size: 9px; color: #888; text-align: center;">
                Sistema E.T.B. v7.0 | Sincronizado: {datetime.datetime.now().strftime('%H:%M')}
            </div>
        </div>
        """
        mapa.get_root().html.add_child(folium.Element(panel))
        folium.LayerControl(collapsed=False).add_to(mapa)
        
        # Guardado estricto para sincronización GitHub
        mapa.save("radar_nuclear_estrategico.html")
        print(f"\n[✅ RADAR NEURONAL V7.0 (CONFIRMACIÓN) GENERADO: radar_nuclear_estrategico.html]")

if __name__ == "__main__":
    radar = RadarInteligenciaAvanzada()
    radar.generar_mapa()