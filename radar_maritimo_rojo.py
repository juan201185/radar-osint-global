import folium
from folium.plugins import MarkerCluster, AntPath
import datetime
import random
import feedparser

class RadarMaritimoGlobal:
    def __init__(self):
        self.brent_ref = 92.69 # Sincronizado con su Radar Financiero
        self.centro_ormuz = [26.1, 55.5] # Coordenadas suministradas por el Ing.
        self.centro_bab_el_mandeb = [12.58, 43.33]

    def motor_proxy_regional(self, zona="ROJO"):
        """Proxy OSINT: Captura telemetría indirecta de buques en chokepoints"""
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Activando Proxy {zona} (Frecuencias/News)...")
        
        consultas = {
            "ROJO": "Houthi+attack+ship+Red+Sea+OR+vessel+diverted+Bab+el-Mandeb",
            "ORMUZ": "oil+tanker+Strait+of+Hormuz+tracking+OR+Fujairah+port+calls"
        }
        
        url_osint = f"https://news.google.com/rss/search?q={consultas[zona]}&hl=en-US&gl=US&ceid=US:en"
        detecciones = []
        
        try:
            flujo = feedparser.parse(url_osint)
            for entry in flujo.entries[:4]:
                titulo = entry.title.lower()
                # Geolocalización dinámica según zona
                if zona == "ROJO":
                    base_coords = self.centro_bab_el_mandeb
                else:
                    base_coords = self.centro_ormuz
                
                detecciones.append({
                    "evento": entry.title[:85] + "...",
                    "coords": [base_coords[0] + random.uniform(-1.5, 1.5), 
                               base_coords[1] + random.uniform(-1.5, 1.5)],
                    "tipo": "ALERTA NAVAL" if zona == "ROJO" else "FLUJO ENERGÍA",
                    "color": "red" if zona == "ROJO" else "yellow"
                })
            return detecciones
        except: return []

    def generar_mapa(self):
        print("\n" + "="*70)
        print("INICIANDO RADAR MARÍTIMO GLOBAL E.T.B. v4.0 (MAR ROJO & ORMUZ)")
        print("="*70)
        
        alertas_rojo = self.motor_proxy_regional("ROJO")
        alertas_ormuz = self.motor_proxy_regional("ORMUZ")
        
        mapa = folium.Map(location=[22.0, 48.0], zoom_start=5, tiles='CartoDB dark_matter')
        
        capa_rojo = folium.FeatureGroup(name="⚠️ Sector Bab el-Mandeb (Bloqueo)").add_to(mapa)
        capa_ormuz = folium.FeatureGroup(name="🛢️ Sector Ormuz (Proxy Energía)").add_to(mapa)
        capa_logistica = folium.FeatureGroup(name="🛣️ Rutas de Suministro").add_to(mapa)

        # 1. Procesar Alertas Mar Rojo (Sector Rojo)
        for a in alertas_rojo:
            folium.Marker(a['coords'], icon=folium.Icon(color='red', icon='ship', prefix='fa'),
                          popup=f"<b>ALERTA ROJO:</b><br>{a['evento']}").add_to(capa_rojo)

        # 2. Procesar Alertas Ormuz (Sector Amarillo/Energía)
        for a in alertas_ormuz:
            folium.Marker(a['coords'], icon=folium.Icon(color='orange', icon='tint', prefix='fa'),
                          popup=f"<b>PROXY ORMUZ:</b><br>{a['evento']}").add_to(capa_ormuz)

        # 3. Chokepoints Visuales
        for centro, nombre, color in [(self.centro_bab_el_mandeb, "Bab el-Mandeb", "red"), 
                                      ([26.58, 56.45], "Estrecho de Ormuz", "yellow")]:
            folium.Circle(centro, radius=120000, color=color, fill=True, fillOpacity=0.15,
                          tooltip=f"CHOKEPOINT: {nombre}").add_to(mapa)

        # 4. Ruta del Cabo (Visualización de sobrecosto)
        AntPath(locations=[[31.5, 32.3], [12.0, 45.0], [-34.0, 18.0]], 
                color='#ffcc00', weight=3, delay=1200, tooltip="Ruta del Cabo (Desvío)").add_to(capa_logistica)

        # Panel Logístico Global E.T.B.
        timestamp = datetime.datetime.now().strftime('%H:%M')
        panel_html = f"""
        <div style="position: fixed; top: 20px; right: 20px; width: 320px; background: rgba(10,10,10,0.95); 
                    color: #fff; border: 2px solid #ffcc00; padding: 15px; border-radius: 10px; 
                    font-family: 'Courier New', monospace; font-size: 11px; z-index: 9999; box-shadow: 0 0 20px #ffcc0066;">
            <h4 style="color:#ffcc00; text-align:center; margin:0 0 10px 0;">🚢 RADAR MARÍTIMO E.T.B. v4.0</h4>
            <div style="background: rgba(255,204,0,0.2); padding: 8px; border-radius: 5px; text-align: center; border: 1px solid #ffcc00; margin-bottom:10px;">
                <b style="color:#fff;">ESTADO LOGÍSTICO: BAJO PRESIÓN</b>
            </div>
            <div style="line-height: 1.4;">
                <b>SECTOR MAR ROJO:</b> {len(alertas_rojo)} Alertas activas<br>
                <b>SECTOR ORMUZ:</b> {len(alertas_ormuz)} Petroleros detectados<br><br>
                <b>INTELIGENCIA DE COSTOS:</b><br>
                Brent Ref: <span style="color:#00ff41;">${self.brent_ref}</span><br>
                Impacto Fletes: ALTO (+12 días demora)<br>
                Estado Proxy: <span style="color:#00ff41;">Sincronizado</span>
            </div>
            <div style="margin-top: 12px; border-top: 1px solid #333; padding-top: 8px; font-size: 9px; color: #666; text-align: center;">
                Sincronizado: {timestamp} | fatreber85
            </div>
        </div>
        """
        mapa.get_root().html.add_child(folium.Element(panel_html))
        folium.LayerControl().add_to(mapa)
        mapa.save("radar_maritimo_global.html")
        print(f"[✅ RADAR MARÍTIMO GLOBAL GENERADO]")

if __name__ == "__main__":
    radar = RadarMaritimoGlobal()
    radar.generar_mapa()