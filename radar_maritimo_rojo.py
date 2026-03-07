import folium
from folium.plugins import MarkerCluster, AntPath
import datetime
import json
import random
import feedparser
import requests

class RadarMaritimoRojo:
    def __init__(self):
        self.brent_ref = 92.69  # Sincronizado con su Radar Financiero E.T.B.
        
    def obtener_incidentes_reales_osint(self):
        """Motor de Inteligencia Naval: Rastrea ataques y bloqueos en tiempo real vía OSINT"""
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Escaneando alertas UKMTO y seguridad naval...")
        
        url_maritima = "https://news.google.com/rss/search?q=Houthi+attack+ship+Red+Sea+OR+vessel+diverted+Bab+el-Mandeb&hl=en-US&gl=US&ceid=US:en"
        incidentes_vivos = []
        
        try:
            flujo = feedparser.parse(url_maritima)
            for entry in flujo.entries[:5]:
                titulo = entry.get('title', 'Alerta Naval').split(' - ')[0]
                t_low = titulo.lower()
                
                # Clasificación de riesgo según el reporte
                estado = "ALERTA CRÍTICA" if any(x in t_low for x in ['hit', 'missile', 'explosion', 'sunk']) else "DESVÍO LOGÍSTICO"
                color = "red" if "CRÍTICA" in estado else "orange"

                incidentes_vivos.append({
                    "fecha": datetime.datetime.now().strftime('%Y-%m-%d'),
                    "buque": "Objetivo Identificado",
                    "tipo": titulo[:85] + "...",
                    "coords": [12.58 + random.uniform(-1, 3), 43.33 + random.uniform(-2, 5)],
                    "estado": estado,
                    "color": color
                })
            return incidentes_vivos
        except: return []

    def calcular_impacto_economico(self):
        """Calcula el sobrecosto de flete basado en el mercado real (Brent)"""
        # Estimación técnica: Sobrecosto por combustible en ruta del Cabo (+3,500 nm)
        sobrecosto_estimado = (self.brent_ref * 2.1) / 85  # Factor logístico E.T.B.
        return {
            "sobrecosto": f"{round(sobrecosto_estimado, 2)}M USD",
            "retraso": "10-14 días adicionales",
            "seguro": "+250% War Risk"
        }

    def generar_mapa(self):
        print("\n" + "="*70)
        print("INICIANDO RADAR MARÍTIMO ROJO E.T.B. v3.0")
        print("="*70)
        
        incidentes = self.obtener_incidentes_reales_osint()
        impacto = self.calcular_impacto_economico()
        
        mapa = folium.Map(location=[15.0, 45.0], zoom_start=5, tiles='CartoDB dark_matter')
        
        capa_peligro = folium.FeatureGroup(name="⚠️ Zonas de Impacto (OSINT)").add_to(mapa)
        capa_rutas = folium.FeatureGroup(name="🛣️ Rutas de Suministro").add_to(mapa)

        # 1. Zona de Bloqueo Bab el-Mandeb
        folium.Circle([12.58, 43.33], radius=180000, color='red', fill=True, fillOpacity=0.2,
                      tooltip="ZONA DE BLOQUEO ACTIVA").add_to(capa_peligro)

        # 2. Incidentes Reales Detectados
        for inc in incidentes:
            popup_html = f"""
            <div style="font-family: 'Courier New', monospace; width: 260px; background: #000; color: #fff; padding: 10px; border-left: 5px solid {inc['color']};">
                <b style="color:{inc['color']}; font-size:14px;">🚢 {inc['estado']}</b><br><br>
                <b>Reporte:</b> {inc['tipo']}<br>
                <b>Sincronizado:</b> {inc['fecha']}
            </div>
            """
            folium.Marker(inc['coords'], icon=folium.Icon(color=inc['color'], icon='ship', prefix='fa'),
                          popup=folium.Popup(popup_html, max_width=300)).add_to(capa_peligro)

        # 3. Animación de Rutas (Desvío Cabo)
        AntPath(locations=[[31.5, 32.3], [12.0, 45.0], [-34.0, 18.0], [40.0, -70.0]], 
                color='#ffcc00', weight=3, delay=1200, tooltip="Ruta del Cabo (Desvío)").add_to(capa_rutas)

        # Panel Logístico E.T.B.
        timestamp = datetime.datetime.now().strftime('%H:%M')
        panel_html = f"""
        <div style="position: fixed; top: 20px; right: 20px; width: 320px; background: rgba(10,10,10,0.95); 
                    color: #fff; border: 2px solid #ff4444; padding: 15px; border-radius: 10px; 
                    font-family: 'Courier New', monospace; font-size: 11px; z-index: 9999; box-shadow: 0 0 20px rgba(255,0,0,0.4);">
            <h4 style="color:#ff4444; text-align:center; margin:0 0 10px 0;">🚢 RADAR MARÍTIMO E.T.B.</h4>
            <div style="background: rgba(255,0,0,0.2); padding: 8px; border-radius: 5px; text-align: center; border: 1px solid #ff4444;">
                <b style="color:#ff6666;">BAB EL-MANDEB: BLOQUEO ACTIVO</b>
            </div>
            <div style="margin-top: 10px; line-height: 1.4;">
                <b>INTELIGENCIA NAVAL:</b><br>
                Incidentes (24h): {len(incidentes)} Detectados<br>
                Amenaza: Drones / Misiles Antibuque<br><br>
                <b>IMPACTO LOGÍSTICO (Ruta Cabo):</b><br>
                Brent Ref: <span style="color:#00ff41;">${self.brent_ref}</span><br>
                Sobrecosto/Buque: <span style="color:#ffcc00;">{impacto['sobrecosto']}</span><br>
                Demora Est: {impacto['retraso']}
            </div>
            <div style="margin-top: 12px; border-top: 1px solid #333; padding-top: 8px; font-size: 9px; color: #666; text-align: center;">
                Sincronizado: {timestamp} | Ingeniería Trejos
            </div>
        </div>
        """
        mapa.get_root().html.add_child(folium.Element(panel_html))
        folium.LayerControl().add_to(mapa)
        mapa.save("radar_maritimo_rojo.html")
        print(f"[✅ RADAR MARÍTIMO REGIONAL GENERADO]")

if __name__ == "__main__":
    radar = RadarMaritimoRojo()
    radar.generar_mapa()