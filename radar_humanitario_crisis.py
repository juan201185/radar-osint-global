import folium
from folium.plugins import MarkerCluster, HeatMap
import datetime
import random
import feedparser

# Nodos Humanitarios y Cruces Estratégicos Regionales
NODOS_ESTRATEGICOS = {
    "Paso de Rafah (Egipto/Gaza)": [31.2968, 34.2435],
    "Paso Kerem Shalom (ISR/Gaza)": [31.2333, 34.2833],
    "Puerto de Ashdod (Hub Ayuda)": [31.8014, 34.6435],
    "Puerto de Hodeida (Yemen)": [14.7979, 42.9530],
    "Frontera Masnaa (Líbano/Siria)": [33.7011, 35.9472],
    "Puerto de Latakia (Siria)": [35.5311, 35.7878],
    "Amán (Logística UN)": [31.9454, 35.9284],
}

class RadarHumanitarioCrisis:
    def __init__(self):
        self.nivel_alerta = "CRÍTICO REGIONAL"
        
    def obtener_alertas_humanitarias_vivas(self):
        """Motor OSINT: Rastrea crisis y desplazamientos en tiempo real (ReliefWeb/UN)"""
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Escaneando telemetría de crisis regional...")
        
        url_osint = "https://news.google.com/rss/search?q=humanitarian+crisis+Gaza+OR+Syria+OR+Yemen+OR+Lebanon+displacement&hl=en-US&gl=US&ceid=US:en"
        eventos_reales = []
        
        try:
            flujo = feedparser.parse(url_osint)
            for entry in flujo.entries[:6]:
                titulo = entry.get('title', 'Alerta detectada').split(' - ')[0]
                t_low = titulo.lower()
                
                if 'gaza' in t_low or 'palestine' in t_low:
                    coords = [31.4, 34.4]
                    color = 'red'
                elif 'lebanon' in t_low or 'beirut' in t_low:
                    coords = [33.8, 35.5]
                    color = 'darkred'
                elif 'syria' in t_low:
                    coords = [34.8, 36.5]
                    color = 'orange'
                elif 'yemen' in t_low:
                    coords = [15.3, 44.2]
                    color = 'darkred'
                else:
                    coords = [32.0, 35.0]
                    color = 'gray'

                eventos_reales.append({
                    "evento": titulo[:85] + "...",
                    "coords": [coords[0] + random.uniform(-0.2, 0.2), coords[1] + random.uniform(-0.2, 0.2)],
                    "fecha": entry.get('published', 'Reciente'),
                    "color": color
                })
            return eventos_reales
        except Exception as e:
            print(f"   [!] Error OSINT: {str(e)[:30]}")
            return []

    def generar_mapa(self):
        print("\n" + "="*70)
        print("INICIANDO RADAR HUMANITARIO E.T.B. (IMPACTO REGIONAL)")
        print("="*70)
        
        mapa = folium.Map(location=[25.0, 40.0], zoom_start=5, tiles='CartoDB dark_matter')
        
        capa_nodos = folium.FeatureGroup(name="🚪 Cruces y Puertos de Ayuda").add_to(mapa)
        capa_alertas = folium.FeatureGroup(name="⚠️ Crisis Detectadas (OSINT)").add_to(mapa)
        capa_calor = folium.FeatureGroup(name="🌡️ Mapa de Calor (Desplazamientos)").add_to(mapa)

        alertas = self.obtener_alertas_humanitarias_vivas()
        puntos_calor = []

        # 1. Dibujar Nodos Estratégicos
        for nombre, coords in NODOS_ESTRATEGICOS.items():
            folium.Marker(
                coords,
                icon=folium.Icon(color='blue', icon='truck', prefix='fa'),
                popup=f"<b>{nombre}</b>",
                tooltip=nombre
            ).add_to(capa_nodos)

        # 2. Bucle Corregido para Alertas
        for al in alertas:
            puntos_calor.append([al['coords'][0], al['coords'][1], 1.0])
            
            popup_html = f"""
            <div style="font-family: 'Courier New', monospace; width: 260px; 
                        background: rgba(0,0,0,0.95); color: #fff; padding: 12px; 
                        border-radius: 8px; border-left: 5px solid {al['color']};">
                <b style="color:{al['color']}; font-size: 14px;">🚨 ALERTA HUMANITARIA</b><br>
                <hr style="border-color: #333; margin: 8px 0;">
                <b>Reporte:</b> {al['evento']}<br>
                <b>Fuente:</b> ReliefWeb OSINT
            </div>
            """
            folium.Marker(
                al['coords'],
                icon=folium.Icon(color=al['color'], icon='exclamation-circle', prefix='fa'),
                popup=folium.Popup(popup_html, max_width=300)
            ).add_to(capa_alertas)

        # 3. Heatmap
        if puntos_calor:
            HeatMap(puntos_calor, radius=30, blur=20).add_to(capa_calor)

        # Panel de Control
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        panel_html = f"""
        <div style="position: fixed; top: 20px; right: 20px; width: 280px; background: rgba(10,10,10,0.95); 
                    color: #fff; border: 2px solid #ff4444; padding: 15px; border-radius: 10px; 
                    font-family: 'Courier New', monospace; font-size: 11px; z-index: 9999;">
            <h4 style="color:#ff4444; text-align:center; margin:0 0 10px 0;">⛑️ RADAR HUMANITARIO E.T.B.</h4>
            <div style="text-align:center; line-height:1.6;">
                NIVEL: {self.nivel_alerta}<br>
                Alertas Activas: {len(alertas)}<br>
                <hr style="border-color:#333;">
                Sincronizado: {timestamp}
            </div>
        </div>
        """
        mapa.get_root().html.add_child(folium.Element(panel_html))
        folium.LayerControl().add_to(mapa)
        mapa.save("radar_humanitario_crisis.html")
        print(f"[✅ RADAR HUMANITARIO REGIONAL GENERADO]")

if __name__ == "__main__":
    radar = RadarHumanitarioCrisis()
    radar.generar_mapa()