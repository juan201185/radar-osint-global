import folium
from folium.plugins import MarkerCluster
import requests
import datetime
import json
import random
import feedparser

# Instalaciones nucleares iraníes (IAEA y OSINT)
INSTALACIONES_NUCLEAR_IRAN = {
    "Natanz": {"coords": [33.7233, 51.7267], "tipo": "Enriquecimiento Uranio", "riesgo": "CRITICO"},
    "Fordow": {"coords": [34.8858, 50.9958], "tipo": "Enriquecimiento 60%", "riesgo": "CRITICO"},
    "Isfahan": {"coords": [32.6804, 51.6861], "tipo": "Conversión/Lab", "riesgo": "ALTO"},
    "Arak": {"coords": [34.3747, 49.4736], "tipo": "Reactor Agua Pesada", "riesgo": "MEDIO"},
    "Parchin": {"coords": [35.5156, 51.8311], "tipo": "Investigación Explosivos", "riesgo": "ALTO"},
    "Bushehr": {"coords": [28.8283, 50.8839], "tipo": "Reactor Civil", "riesgo": "BAJO"}
}

class RadarNuclearEstrategico:
    def __init__(self):
        self.nivel_alerta = "NARANJA"
        self.tiempo_breakout = "1-2 semanas"
        
    def obtener_eventos_sismicos_reales(self):
        """Conexión en vivo con USGS para detectar anomalías sísmicas/nucleares"""
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Escaneando sismógrafos globales (USGS API)...")
        # Ventana de 7 días, región de Medio Oriente
        url_usgs = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=" + \
                   (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y-%m-%d') + \
                   "&minmagnitude=3.0&minlatitude=24&maxlatitude=40&minlongitude=44&maxlongitude=63"
        
        eventos_reales = []
        try:
            resp = requests.get(url_usgs, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                for feature in data['features']:
                    prop = feature['properties']
                    geom = feature['geometry']
                    # Anomalía sospechosa si profundidad es < 2km cerca de zonas militares
                    sospecha = "ANOMALÍA SUPERFICIAL" if geom['coordinates'][2] < 2 else "Evento Tectónico"
                    eventos_reales.append({
                        "fecha": datetime.datetime.fromtimestamp(prop['time']/1000).strftime('%Y-%m-%d %H:%M'),
                        "magnitud": prop['mag'],
                        "coords": [geom['coordinates'][1], geom['coordinates'][0]],
                        "sospecha": sospecha,
                        "profundidad": f"{geom['coordinates'][2]}km"
                    })
            return eventos_reales
        except: return []

    def simular_inteligencia_iaea(self):
        """Motor OSINT: Extrae el pulso diplomático y técnico nuclear de hoy"""
        print(f"   [!] Triangulando reportes de inspección y breakout time...")
        url_osint = "https://news.google.com/rss/search?q=IAEA+Iran+nuclear+stockpile+60+percent&hl=en-US&gl=US&ceid=US:en"
        try:
            flujo = feedparser.parse(url_osint)
            titular = flujo.entries[0].title if flujo.entries else "Sin cambios recientes"
            if any(x in titular.lower() for x in ['acceleration', 'threat', 'breakthrough']):
                self.nivel_alerta, self.tiempo_breakout = "ROJO", "< 1 semana"
            return {"ultima_alerta": titular[:80] + "...", "inspeccion": "Vigilancia OSINT activa"}
        except: return {"ultima_alerta": "Datos protegidos", "inspeccion": "N/A"}

    def generar_mapa(self):
        print("\n" + "="*70)
        print("INICIANDO RADAR NUCLEAR ESTRATÉGICO E.T.B. v3.0")
        print("="*70)
        
        reporte = self.simular_inteligencia_iaea()
        sismos = self.obtener_eventos_sismicos_reales()
        
        mapa = folium.Map(location=[32.0, 48.0], zoom_start=5, tiles='CartoDB dark_matter')
        
        capa_nuclear = folium.FeatureGroup(name="☢️ Instalaciones Atómicas").add_to(mapa)
        capa_sismica = folium.FeatureGroup(name="💥 Sismógrafos USGS (En Vivo)").add_to(mapa)

        # 1. Instalaciones Iraníes
        for nom, d in INSTALACIONES_NUCLEAR_IRAN.items():
            color = {"CRITICO": "red", "ALTO": "orange", "MEDIO": "beige", "BAJO": "green"}.get(d['riesgo'], 'gray')
            folium.Marker(d['coords'], icon=folium.Icon(color=color, icon='radiation', prefix='fa'),
                          popup=f"<b>{nom}</b><br>Tipo: {d['tipo']}<br>Riesgo: {d['riesgo']}").add_to(capa_nuclear)
            folium.Circle(d['coords'], radius=20000, color=color, fill=True, fillOpacity=0.1).add_to(capa_nuclear)

        # 2. Eventos Sísmicos Reales (USGS)
        for s in sismos:
            color_sismo = 'purple' if s['sospecha'] == "ANOMALÍA SUPERFICIAL" else 'blue'
            popup_sismo = f"<b>{s['sospecha']}</b><br>Mag: {s['magnitud']}<br>Prof: {s['profundidad']}<br>Fecha: {s['fecha']}"
            folium.CircleMarker(s['coords'], radius=s['magnitud']*3, color=color_sismo, fill=True, 
                                popup=folium.Popup(popup_sismo, max_width=200)).add_to(capa_sismica)

        # Panel de Alerta E.T.B.
        color_panel = '#ff0000' if self.nivel_alerta == "ROJO" else '#ffaa00'
        panel_html = f"""
        <div style="position: fixed; top: 20px; right: 20px; width: 300px; background: rgba(10,10,10,0.95); 
                    color: #fff; border: 2px solid {color_panel}; padding: 15px; border-radius: 10px; 
                    font-family: 'Courier New', monospace; font-size: 11px; z-index: 9999; box-shadow: 0 0 20px {color_panel}66;">
            <h4 style="color:{color_panel}; text-align:center; margin:0 0 10px 0;">☢️ ALERTA ESTRATÉGICA: {self.nivel_alerta}</h4>
            <div style="background: {color_panel}33; padding: 8px; border-radius: 5px; text-align: center; border: 1px solid {color_panel};">
                <b style="color:{color_panel};">BREAKOUT TIME: {self.tiempo_breakout}</b>
            </div>
            <div style="margin-top: 10px; line-height: 1.4;">
                <b>INTELIGENCIA OSINT:</b><br>
                {reporte['ultima_alerta']}<br><br>
                <b>MONITOR SÍSMICO:</b><br>
                Eventos Detectados (7d): {len(sismos)}<br>
                Anomalías Superficiales: {len([x for x in sismos if x['sospecha'] == 'ANOMALÍA SUPERFICIAL'])}
            </div>
            <div style="margin-top: 12px; border-top: 1px solid #333; padding-top: 8px; font-size: 9px; color: #666; text-align: center;">
                Sistema E.T.B. v3.0 | Sincronizado: {datetime.datetime.now().strftime('%H:%M')}
            </div>
        </div>
        """
        mapa.get_root().html.add_child(folium.Element(panel_html))
        folium.LayerControl().add_to(mapa)
        mapa.save("radar_nuclear_estrategico.html")
        print(f"[✅ RADAR NUCLEAR ESTRATÉGICO GENERADO]")

if __name__ == "__main__":
    radar = RadarNuclearEstrategico()
    radar.generar_mapa()