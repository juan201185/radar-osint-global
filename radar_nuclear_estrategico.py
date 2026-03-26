import folium
import requests
import datetime
import math
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
import warnings

warnings.filterwarnings('ignore')

# --- CONFIGURACIÓN ESTRATÉGICA ---
INSTALACIONES_NUCLEAR_ME = {
    "Natanz (SUB)": {"coords": [33.7233, 51.7267], "sub": 1},
    "Fordow (SUB)": {"coords": [34.8858, 50.9958], "sub": 1},
    "Bushehr": {"coords": [28.8283, 50.8839], "sub": 0},
    "Dimona (IL)": {"coords": [31.0011, 35.1469], "sub": 0},
    "Barakah (EAU)": {"coords": [23.9781, 52.2353], "sub": 0}
}

def calcular_distancia(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat, dlon = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))

class CerebroNeuronalETB:
    def __init__(self):
        self.modelo = MLPClassifier(hidden_layer_sizes=(32, 16), activation='relu', max_iter=3000, random_state=42)
        self.scaler = StandardScaler()
        # Features: [Mag, Prof, Dist, Rad, Sub]
        X = np.array([[4.5, 15, 10, 0.15, 1], [3.5, 0, 2, 0.15, 1], [5.3, 0, 0.2, 45, 1]])
        y = np.array([0, 1, 2])
        self.scaler.fit(X)
        self.modelo.fit(self.scaler.transform(X), y)

    def evaluar(self, mag, prof, lat, lon):
        dist_min, es_sub = 9999, 0
        for d in INSTALACIONES_NUCLEAR_ME.values():
            dist = calcular_distancia(lat, lon, d['coords'][0], d['coords'][1])
            if dist < dist_min: dist_min, es_sub = dist, d['sub']
        datos = self.scaler.transform([[mag, prof, dist_min, 0.15, es_sub]])
        return self.modelo.predict(datos)[0], round(max(self.modelo.predict_proba(datos)[0])*100, 1), round(dist_min, 1)

class RadarETB_v11:
    def __init__(self):
        self.ia = CerebroNeuronalETB()
        
    def generar_mapa(self):
        print("\n" + "="*70 + "\nRADAR E.T.B. v11.0 - FORZANDO TELEMETRÍA RADIACTIVA\n" + "="*70)
        mapa = folium.Map(location=[30.0, 45.0], zoom_start=5, tiles='CartoDB dark_matter')
        
        capa_rad = folium.FeatureGroup(name="🟢 Sensores SafeCast (DATOS BRUTOS)").add_to(mapa)
        capa_tectonica = folium.FeatureGroup(name="🔵 Sismos USGS").add_to(mapa)
        capa_alertas = folium.FeatureGroup(name="🔴 Alertas IA").add_to(mapa)

        # 1. TRACCIÓN FORZADA DE RADIACIÓN
        rad_count = 0
        try:
            # Pedimos más datos (1000) para asegurar que tras el filtro de estaciones únicas queden bastantes
            url_rad = "https://api.safecast.org/measurements.json?limit=1000&min_latitude=15&max_latitude=45&min_longitude=25&max_longitude=65"
            rad_resp = requests.get(url_rad, timeout=15).json()
            estaciones = {}
            for r in rad_resp:
                # Filtro por precisión de 3 decimales para evitar el stacking
                sid = f"{round(r['latitude'],3)}_{round(r['longitude'],3)}"
                if sid not in estaciones:
                    estaciones[sid] = r
                    folium.CircleMarker(
                        [r['latitude'], r['longitude']], radius=4, color="lime", fill=True, fillOpacity=0.8,
                        tooltip=f"{r['value']} {r['unit']}"
                    ).add_to(capa_rad)
            rad_count = len(estaciones)
            print(f"-> EXITO: {rad_count} estaciones de radiación únicas ubicadas.")
        except Exception as e: print(f"-> ERROR API RAD: {e}")

        # 2. SISMOS
        sismos_total, alertas_ia = 0, 0
        try:
            start = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
            url_sismos = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={start}&minmagnitude=2.5&minlatitude=15&maxlatitude=45&minlongitude=25&maxlongitude=65"
            sismos_data = requests.get(url_sismos, timeout=15).json()
            for f in sismos_data['features']:
                sismos_total += 1
                lat, lon, prof = f['geometry']['coordinates'][1], f['geometry']['coordinates'][0], f['geometry']['coordinates'][2]
                mag = f['properties']['mag']
                tipo, cert, dist = self.ia.evaluar(mag, prof, lat, lon)
                
                color = "blue"
                capa = capa_tectonica
                if tipo > 0:
                    alertas_ia += 1
                    color, capa = ("orange", capa_alertas) if tipo == 1 else ("red", capa_alertas)
                
                folium.CircleMarker([lat, lon], radius=mag*3, color=color, fill=True).add_to(capa)
            print(f"-> EXITO: {sismos_total} sismos procesados.")
        except Exception as e: print(f"-> ERROR API SISMOS: {e}")

        # HUD v11.0
        panel = f"""
        <div style="position: fixed; top: 20px; right: 20px; width: 320px; background: rgba(0,0,0,0.9); border: 2px solid lime; padding: 15px; color: #fff; font-family: monospace; z-index: 9999;">
            <b style="color:lime;">🌐 E.T.B. v11.0 - VISIÓN TOTAL</b><hr>
            Sensores OSINT (SafeCast): <b style="color:lime;">{rad_count}</b><br>
            Sismos Brutos (7d): <b style="color:cyan;">{sismos_total}</b><br>
            Alertas IA: <b style="color:red;">{alertas_ia}</b><br>
            <div style="margin-top: 10px; font-size: 9px; color: #888; text-align: center;">
                Sincronizado: {datetime.datetime.now().strftime('%H:%M')}
            </div>
        </div>
        """
        mapa.get_root().html.add_child(folium.Element(panel))
        folium.LayerControl(collapsed=False).add_to(mapa)
        mapa.save("radar_nuclear_estrategico.html")
        print("[✅ MAPA GENERADO]")

if __name__ == "__main__":
    RadarETB_v11().generar_mapa()