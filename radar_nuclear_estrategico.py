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

# --- MATRIZ ESTRATÉGICA v9.0 (CLASIFICACIÓN GEOLÓGICA) ---
INSTALACIONES_NUCLEAR_ME = {
    # Nodos Subterráneos (Cúpula de Roca) -> "sub": 1
    "Natanz (SUB)": {"coords": [33.7233, 51.7267], "pais": "Irán", "sub": 1},
    "Fordow (SUB)": {"coords": [34.8858, 50.9958], "pais": "Irán", "sub": 1},
    "Parchin (SUB)": {"coords": [35.5156, 51.8311], "pais": "Irán", "sub": 1},
    
    # Nodos de Superficie -> "sub": 0
    "Isfahan": {"coords": [32.6804, 51.6861], "pais": "Irán", "sub": 0},
    "Bushehr": {"coords": [28.8283, 50.8839], "pais": "Irán", "sub": 0},
    "Dimona (NNRC)": {"coords": [31.0011, 35.1469], "pais": "Israel", "sub": 0},
    "Soreq": {"coords": [31.9054, 34.7820], "pais": "Israel", "sub": 0},
    "Akkuyu NPP": {"coords": [36.1436, 33.5411], "pais": "Turquía", "sub": 0}
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
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 🧠 Inicializando IA v9.0 (Física de Atenuación y Venting)...")
        self.modelo = MLPClassifier(hidden_layer_sizes=(32, 16), activation='relu', max_iter=3000, random_state=42)
        self.scaler = StandardScaler()
        self.entrenar_ia()

    def entrenar_ia(self):
        # 5 Variables: [Magnitud, Profundidad_km, Distancia_Nodo, Rad_uSv, Es_Subterraneo(1/0)]
        X_train = np.array([
            # 🔵 Sismos Naturales
            [4.5, 15.0, 10.0, 0.15, 1], [5.1, 20.0, 5.0, 0.12, 0], [6.0, 30.0, 100.0, 0.11, 0],
            
            # 🟠 Impactos Cinéticos (Bunker Busters en Montaña - Rad Normal porque la roca escuda)
            [3.5, 0.0, 2.0, 0.15, 1], [4.2, 0.5, 1.0, 0.16, 1], [2.8, 0.0, 0.5, 0.14, 1],
            
            # 🟠 Impactos en Superficie (Sismo superficial, Rad normal)
            [3.0, 0.0, 1.0, 0.15, 0], 
            
            # 🔴 Detonaciones/Fugas Activas (Venting detectado o Brecha estructural)
            [4.3, 0.0, 2.0, 5.5, 1], [6.3, 0.0, 0.0, 45.0, 1], # Penetración + Fuga
            [4.0, 0.0, 1.0, 12.0, 0], # Impacto en superficie con fuga
            [0.0, 0.0, 2.0, 8.5, 0]   # Fuga sin sismo (Sabotaje interno)
        ])
        
        # 0 = Natural | 1 = Cinético/BunkerBuster (Activa Venting) | 2 = Nuclear/Fuga Confirmada
        y_train = np.array([0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2])
        
        self.X_train_scaled = self.scaler.fit_transform(X_train)
        self.modelo.fit(self.X_train_scaled, y_train)
        print("   [✓] IA calibrada: Entiende el retraso de filtración de gases nobles (Xenón/Kriptón).")

    def predecir_amenaza(self, mag, prof, lat, lon, rad):
        # Buscar el nodo más cercano para saber si es subterráneo
        nodo_cercano = None
        dist_minima = 99999
        es_sub = 0
        
        for nom, d in INSTALACIONES_NUCLEAR_ME.items():
            dist = calcular_distancia(lat, lon, d['coords'][0], d['coords'][1])
            if dist < dist_minima:
                dist_minima = dist
                nodo_cercano = nom
                es_sub = d['sub']

        datos = self.scaler.transform([[mag, prof, dist_minima, rad, es_sub]])
        tipo = self.modelo.predict(datos)[0]
        certeza = max(self.modelo.predict_proba(datos)[0]) * 100
        
        return tipo, round(certeza, 2), round(dist_minima, 2), es_sub

class RadarInteligenciaAvanzada:
    def __init__(self):
        self.ia = CerebroNeuronalETB()
        
    def obtener_datos_osint(self):
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] ☢️ Escaneando red SafeCast Global...")
        url_rad = "https://api.safecast.org/measurements.json?limit=300&min_latitude=25&max_latitude=40&min_longitude=33&max_longitude=60"
        return url_rad

    def generar_mapa(self):
        print("\n" + "="*70)
        print("INICIANDO RADAR E.T.B. v9.0 (PROTOCOLO FORENSE VENTING 72H)")
        print("="*70)
        
        url_rad = self.obtener_datos_osint()
        mapa = folium.Map(location=[32.0, 48.0], zoom_start=5, tiles='CartoDB dark_matter')
        
        capa_nodos = folium.FeatureGroup(name="🏗️ Cúpulas y Reactores").add_to(mapa)
        capa_rad = folium.FeatureGroup(name="🟢 Sensores OSINT").add_to(mapa)
        capa_alertas = folium.FeatureGroup(name="🔴 Motor IA (Crisis & Venting)").add_to(mapa)

        # 1. Nodos
        for nom, d in INSTALACIONES_NUCLEAR_ME.items():
            color = "darkred" if d['sub'] == 1 else "blue"
            icono = "mountain" if d['sub'] == 1 else "radiation"
            folium.Marker(
                location=d['coords'], icon=folium.Icon(color=color, icon=icono, prefix="fa"),
                tooltip=f"<b>{nom}</b> ({'SUBTERRÁNEO' if d['sub']==1 else 'SUPERFICIE'})"
            ).add_to(capa_nodos)

        # 2. Radiación
        rad_data = []
        try:
            rad_resp = requests.get(url_rad, timeout=10).json()
            estaciones_unicas = {}
            for r in rad_resp:
                sid = f"{round(r['latitude'],2)}_{round(r['longitude'],2)}"
                if sid not in estaciones_unicas:
                    estaciones_unicas[sid] = r
                    folium.CircleMarker([r['latitude'], r['longitude']], radius=3, color="lime", fill=True).add_to(capa_rad)
            rad_data = list(estaciones_unicas.values())
        except: print("   [!] Api OSINT Rad saturada.")

        # 3. Sismos e IA (Evaluación Venting)
        alertas_total = 0
        venting_activos = 0
        
        try:
            start = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
            url_sismos = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={start}&minmagnitude=3.0&minlatitude=25&maxlatitude=40&minlongitude=33&maxlongitude=60"
            sismos_data = requests.get(url_sismos, timeout=10).json()
            
            ahora = datetime.datetime.now()
            
            for f in sismos_data['features']:
                geom = f['geometry']
                lat, lon, prof = geom['coordinates'][1], geom['coordinates'][0], geom['coordinates'][2]
                mag = f['properties']['mag']
                
                # Calcular horas transcurridas
                tiempo_sismo = datetime.datetime.fromtimestamp(f['properties']['time']/1000)
                horas_pasadas = (ahora - tiempo_sismo).total_seconds() / 3600
                
                tipo, certeza, dist, es_sub = self.ia.predecir_amenaza(mag, prof, lat, lon, 0.15)
                
                if tipo > 0:
                    alertas_total += 1
                    
                    # LOGICA DEL PROTOCOLO VENTING
                    if tipo == 1 and es_sub == 1 and horas_pasadas <= 72:
                        color = "darkorange"
                        clasif = "⚠️ PROTOCOLO VENTING (72H)"
                        estado = f"Vigilando filtración de gases. T-{round(horas_pasadas, 1)} horas."
                        venting_activos += 1
                    elif tipo == 1:
                        color = "orange"
                        clasif = "IMPACTO CINÉTICO"
                        estado = "Impacto en superficie detectado."
                    else: # tipo == 2
                        color = "red"
                        clasif = "☢️ ALERTA: FUGA / DETONACIÓN"
                        estado = "Radiación anómala confirmada."

                    html = f"""
                    <div style="font-family:monospace; width:240px; background:#111; color:#fff; padding:10px; border:1px solid {color}; border-radius:4px;">
                        <b style="color:{color}; font-size:12px;">{clasif}</b><hr style="border-color:#333; margin:6px 0;">
                        <b>Mag:</b> {mag} | <b>Prof:</b> {prof}km<br>
                        <b>Dist. a Nodo:</b> {dist}km<br>
                        <span style="color:#aaa; font-size:10px;">{estado}</span><br>
                        <div style="background:{color}; color:#fff; text-align:center; padding:4px; margin-top:6px; font-weight:bold;">
                            CERTEZA IA: {certeza}%
                        </div>
                    </div>
                    """
                    folium.CircleMarker(
                        location=[lat, lon], radius=mag*4, color=color, fill=True, fillOpacity=0.8,
                        popup=folium.Popup(html, max_width=260)
                    ).add_to(capa_alertas)
        except Exception as e: print(f"   [!] Error de procesamiento: {e}")

        # HUD Táctico
        color_hud = "#ff0000" if alertas_total > 0 else "#00ff41"
        if venting_activos > 0 and alertas_total == venting_activos: color_hud = "darkorange" # Predomina el naranja si solo hay Venting
        
        panel_html = f"""
        <div style="position: fixed; top: 20px; right: 20px; width: 340px; background: rgba(0,0,0,0.92); 
                    border: 2px solid {color_hud}; padding: 15px; color: #fff; font-family: monospace; z-index: 9999;">
            <b style="font-size:15px; color:{color_hud};">🌐 E.T.B. v9.0 - SISMOLOGÍA FORENSE</b><br>
            <span style="font-size:10px; color:#aaa;">MONITOR DE ATENUACIÓN Y VENTING ACTIVO</span><hr style="border-color:#444;">
            <span style="color:darkorange;">Protocolos Venting (72h):</span> <b>{venting_activos}</b><br>
            Amenazas Activas (IA): <b style="color:red;">{alertas_total}</b><br>
            <div style="margin-top: 10px; border-top: 1px solid #333; padding-top: 8px; font-size: 9px; color: #888; text-align: center;">
                Sincronizado: {datetime.datetime.now().strftime('%H:%M')} | GitHub Branch: Main
            </div>
        </div>
        """
        mapa.get_root().html.add_child(folium.Element(panel_html))
        folium.LayerControl(collapsed=False).add_to(mapa)
        mapa.save("radar_nuclear_estrategico.html")
        print(f"[✅ RADAR FORENSE v9.0 GENERADO PARA PATÍA GLOBAL]")

if __name__ == "__main__":
    radar = RadarInteligenciaAvanzada()
    radar.generar_mapa()