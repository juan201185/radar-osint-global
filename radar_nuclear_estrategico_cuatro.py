import folium
import requests
import datetime
import math
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
import warnings
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional

warnings.filterwarnings('ignore')

# --- CONFIGURACIÓN ESTRATÉGICA FORENSE ---
INSTALACIONES_NUCLEAR_ME = {
    "Natanz (SUB)": {"coords": [33.7233, 51.7267], "tipo": "enriquecimiento", "profundidad_escudo": 7.6, "subterraneo": True},
    "Fordow (SUB)": {"coords": [34.8858, 50.9958], "tipo": "enriquecimiento", "profundidad_escudo": 80, "subterraneo": True},
    "Parchin (SUB)": {"coords": [35.5156, 51.8311], "tipo": "investigación", "profundidad_escudo": 15, "subterraneo": True},
    "Isfahan": {"coords": [32.6804, 51.6861], "tipo": "conversión", "profundidad_escudo": 0, "subterraneo": False},
    "Bushehr": {"coords": [28.8283, 50.8839], "tipo": "reactor", "profundidad_escudo": 0, "subterraneo": False},
    "Dimona (NNRC)": {"coords": [31.0011, 35.1469], "tipo": "producción armas", "profundidad_escudo": 0, "subterraneo": False},
    "Soreq": {"coords": [31.9054, 34.7820], "tipo": "centro nuclear", "profundidad_escudo": 0, "subterraneo": False},
    "Barakah NPP": {"coords": [23.9781, 52.2353], "tipo": "reactor civil", "profundidad_escudo": 0, "subterraneo": False}
}

COEF_ATENUACION_GRANITO = 0.15  # cm^-1

@dataclass
class EventoSismico:
    id: str
    lat: float
    lon: float
    profundidad: float
    magnitud: float
    tiempo: datetime.datetime
    lugar: str

@dataclass
class MedicionRadiacion:
    lat: float
    lon: float
    valor: float
    unidad: str
    tiempo: Optional[datetime.datetime]

@dataclass
class AlertaForense:
    nivel: int  # 0: Normal, 1: Cinética Pura, 2: Brecha, 3: Venting
    tipo: str
    confianza: float
    instalacion: str
    distancia_km: float
    tiempo_retraso: Optional[float]
    evidencia: Dict
    recomendacion: str

def calcular_distancia(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    dlat, dlon = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2)
    return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))

def calcular_atenuacion_radiacion(profundidad_metros: float) -> float:
    profundidad_cm = profundidad_metros * 100
    return math.exp(-COEF_ATENUACION_GRANITO * profundidad_cm)

class CerebroNeuronalETB_v13:
    def __init__(self):
        self.modelo = MLPClassifier(hidden_layer_sizes=(64, 32, 16), activation='relu', max_iter=5000, random_state=42)
        self.scaler = StandardScaler()
        self.vigilancia_activa: Dict[str, Dict] = {}
        self._entrenar_modelo_base()

    def _entrenar_modelo_base(self):
        # [Mag, Prof_km, Dist_km, Rad_uSv, Es_Sub, Horas_Post], Clase
        casos = [
            ([4.5, 0.5, 2.0, 0.15, 1, 0], 1),    # Cinética Pura SUB
            ([3.8, 0.3, 1.5, 2.5, 1, 24], 2),    # Brecha
            ([5.1, 15.0, 50.0, 0.15, 0, 0], 0),  # Sismo natural
            ([4.0, 0.5, 2.0, 0.45, 1, 48], 3),   # Venting tardío
        ]
        X = np.array([c[0] for c in casos])
        y = np.array([c[1] for c in casos])
        self.scaler.fit(X)
        self.modelo.fit(self.scaler.transform(X), y)

    def evaluar_evento(self, sismo: EventoSismico, radiacion_actual: float) -> AlertaForense:
        instalacion_cercana = "Ninguna"
        dist_min = float('inf')
        es_sub = False
        profundidad_escudo = 0
        
        for nombre, datos in INSTALACIONES_NUCLEAR_ME.items():
            dist = calcular_distancia(sismo.lat, sismo.lon, datos['coords'][0], datos['coords'][1])
            if dist < dist_min:
                dist_min = dist
                instalacion_cercana = nombre
                es_sub = datos['subterraneo']
                profundidad_escudo = datos['profundidad_escudo']

        # FASE 1: Firma Cinética
        score_cinetica = 0.0
        if es_sub:
            if 3.0 <= sismo.magnitud <= 5.5: score_cinetica += 0.4
            if sismo.profundidad <= 2.0: score_cinetica += 0.3
            if dist_min <= 5.0: score_cinetica += 0.3
            elif dist_min <= 15.0: score_cinetica += 0.15
        es_cinetica = score_cinetica >= 0.6

        atenuacion = calcular_atenuacion_radiacion(profundidad_escudo)

        # Lógica de Alertas
        if es_cinetica and radiacion_actual < 0.3:
            nivel, tipo = 1, "IMPACTO CINÉTICO ANTIBÚNKER"
            confianza = score_cinetica * 100
            recomendacion = f"VIGILANCIA ACTIVADA: {instalacion_cercana}\nMonitorear venting 72h."
            self.vigilancia_activa[instalacion_cercana] = {'inicio': sismo.tiempo, 'magnitud': sismo.magnitud}
        elif es_cinetica and radiacion_actual >= 0.3:
            nivel, tipo = 2, "BRECHA ESTRUCTURAL POSIBLE"
            confianza = 95.0
            recomendacion = f"ALERTA: Radiación anómala ({radiacion_actual} uSv/h) post-impacto."
        else:
            nivel, tipo = 0, "Evento Tectónico Natural"
            confianza = 100 - (score_cinetica * 100)
            recomendacion = "Sin correlación forense."

        # Predicción ML
        features = np.array([[sismo.magnitud, sismo.profundidad, dist_min, radiacion_actual, int(es_sub), 0]])
        pred_ml = self.modelo.predict(self.scaler.transform(features))[0]

        return AlertaForense(
            nivel=nivel, tipo=tipo, confianza=round(confianza, 1), instalacion=instalacion_cercana,
            distancia_km=round(dist_min, 1), tiempo_retraso=0, 
            evidencia={'atenuacion_teorica': atenuacion, 'score_cinetica': score_cinetica, 'pred_ml': int(pred_ml), 'prof': sismo.profundidad},
            recomendacion=recomendacion
        )

class RadarForense_v13:
    def __init__(self):
        self.ia = CerebroNeuronalETB_v13()
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
        
    def generar_mapa(self):
        print("\n" + "="*70 + "\nRADAR E.T.B. v13.0 - FUSIÓN FORENSE DEFINITIVA\n" + "="*70)
        mapa = folium.Map(location=[31.0, 45.0], zoom_start=5, tiles='CartoDB dark_matter')
        
        capa_inst = folium.FeatureGroup(name="🏭 Instalaciones Nucleares").add_to(mapa)
        capa_rad = folium.FeatureGroup(name="🟢 Sensores OSINT Reales").add_to(mapa)
        capa_sis_nat = folium.FeatureGroup(name="🔵 Sismos Naturales").add_to(mapa)
        capa_alertas = folium.FeatureGroup(name="🟠🔴 Alertas Forenses").add_to(mapa)

        # 1. Nodos
        for nom, d in INSTALACIONES_NUCLEAR_ME.items():
            color = 'darkred' if d['subterraneo'] else 'orange'
            folium.Marker(d['coords'], icon=folium.Icon(color=color, icon='shield', prefix='fa'), tooltip=nom).add_to(capa_inst)
            if d['subterraneo']: folium.Circle(d['coords'], radius=5000, color='red', fill=False, weight=1, dash_array='5, 10').add_to(capa_inst)

        # 2. MOTOR DATOS V10.2: Extracción OSINT Real (Sin simulaciones)
        mediciones_reales = []
        try:
            coordenadas_tacticas = [(31.7, 35.2), (32.0, 50.0), (24.0, 54.0), (39.0, 35.0)]
            estaciones = {}
            for lat, lon in coordenadas_tacticas:
                url_rad = f"https://api.safecast.org/measurements.json?latitude={lat}&longitude={lon}&distance=1000000"
                resp = self.session.get(url_rad, timeout=10)
                if resp.status_code == 200:
                    for r in resp.json()[:25]:
                        sid = f"{round(r['latitude'],3)}_{round(r['longitude'],3)}"
                        if sid not in estaciones:
                            estaciones[sid] = r
                            m = MedicionRadiacion(r['latitude'], r['longitude'], r['value'], r['unit'], None)
                            mediciones_reales.append(m)
                            folium.CircleMarker([m.lat, m.lon], radius=4, color="lime", fill=True, tooltip=f"{m.valor} {m.unidad}").add_to(capa_rad)
            print(f"-> EXITO: {len(mediciones_reales)} sensores SafeCast reales obtenidos.")
        except Exception as e: print(f"-> ERROR RAD: {e}")

        # 3. Sismos y Evaluación Forense
        sismos_totales, alertas_activas = 0, []
        try:
            start = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
            url_sismos = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={start}&minmagnitude=2.5&minlatitude=15&maxlatitude=45&minlongitude=25&maxlongitude=65"
            resp_sis = self.session.get(url_sismos, timeout=10)
            
            if resp_sis.status_code == 200:
                for f in resp_sis.json().get('features', []):
                    sismos_totales += 1
                    props, coords = f['properties'], f['geometry']['coordinates']
                    sismo = EventoSismico(f['id'], coords[1], coords[0], coords[2], props['mag'], datetime.datetime.fromtimestamp(props['time']/1000), props.get('place',''))
                    
                    # Fusión de Radiación Local Real
                    rad_local = 0.15
                    cercanas = [m.valor for m in mediciones_reales if calcular_distancia(sismo.lat, sismo.lon, m.lat, m.lon) <= 50]
                    if cercanas: rad_local = max(cercanas) # Tomamos el pico más alto cercano
                    
                    alerta = self.ia.evaluar_evento(sismo, rad_local)
                    
                    if alerta.nivel == 0:
                        color, capa, radio = 'blue', capa_sis_nat, sismo.magnitud * 2
                    else:
                        alertas_activas.append(alerta)
                        color, capa, radio = ('orange' if alerta.nivel==1 else 'red'), capa_alertas, sismo.magnitud * 4

                    html_popup = f"""<div style='font-family:monospace; min-width:250px;'>
                        <b style='color:{color};'>{alerta.tipo}</b><hr>
                        Mag: {sismo.magnitud} | Prof: {sismo.profundidad}km<br>
                        Rad Local: {rad_local} uSv/h<br>
                        Confianza IA: {alerta.confianza}%<br><hr>
                        <i>Recomendación: {alerta.recomendacion.replace(chr(10), '<br>')}</i></div>"""
                    folium.CircleMarker([sismo.lat, sismo.lon], radius=radio, color=color, fill=True, popup=folium.Popup(html_popup, max_width=300)).add_to(capa)
                print(f"-> EXITO: {sismos_totales} sismos procesados. Alertas: {len(alertas_activas)}")
        except Exception as e: print(f"-> ERROR SISMOS: {e}")

        # HUD v13.0
        vig_html = "".join([f"<div style='color:orange; font-size:10px;'>⏱️ {inst}</div>" for inst in self.ia.vigilancia_activa.keys()])
        panel = f"""
        <div style="position: fixed; top: 20px; right: 20px; width: 320px; background: rgba(0,0,0,0.9); border: 2px solid lime; padding: 15px; color: #fff; font-family: monospace; z-index: 9999;">
            <b style="color:lime; font-size:14px;">🛡️ E.T.B. v13.0 - FUSIÓN FORENSE</b><hr>
            Sensores Reales: <b style="color:lime;">{len(mediciones_reales)}</b><br>
            Sismos Brutos (7d): <b style="color:cyan;">{sismos_totales}</b><br>
            Alertas Cinéticas/Fuga: <b style="color:red;">{len(alertas_activas)}</b><br>
            <div style="margin-top:8px; border-top:1px solid #333; padding-top:4px;">
                <span style="color:#aaa; font-size:11px;">Vigilancias 72h Activas:</span><br>
                {vig_html if vig_html else '<span style="color:#666; font-size:10px;">Ninguna</span>'}
            </div>
            <div style="margin-top: 10px; font-size: 9px; color: #888; text-align: center;">Sincronizado: {datetime.datetime.now().strftime('%H:%M')}</div>
        </div>
        """
        mapa.get_root().html.add_child(folium.Element(panel))
        folium.LayerControl(collapsed=False).add_to(mapa)
        mapa.save("radar_nuclear_estrategico.html")
        print("[✅ MAPA FORENSE v13.0 GENERADO CON ÉXITO]")

if __name__ == "__main__":
    RadarForense_v13().generar_mapa()