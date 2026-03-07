import folium
from folium.plugins import MarkerCluster, AntPath
import datetime
import json
import random
import feedparser

# Base de datos de Grupos de Amenaza (Perfiles Técnicos)
GRUPOS_CIBER = {
    "APT35 (Charming Kitten)": {"pais": "Irán", "coords": [35.6, 51.3], "color": "red"},
    "APT33 (Elfin - SCADA)": {"pais": "Irán", "coords": [32.6, 51.6], "color": "darkred"},
    "Unit 8200 (ISR)": {"pais": "Israel", "coords": [32.0, 34.7], "color": "blue"},
    "Unit 81 (Ciber-Física)": {"pais": "Israel", "coords": [31.7, 35.2], "color": "darkblue"},
    "KillNet / Anonymous Sudan": {"pais": "Rusia/Pro-Eje", "coords": [55.7, 37.6], "color": "purple"}
}

class RadarCiberGuerra:
    def __init__(self):
        self.estado_red = "AMENAZA ELEVADA"
        
    def analizar_amenazas_vivas(self):
        """Motor de Inteligencia: Rastrea incidentes de ciberseguridad en tiempo real vía OSINT"""
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Escaneando reportes de incidentes (CISA/OSINT)...")
        url_ciber = "https://news.google.com/rss/search?q=cyber+attack+Middle+East+OR+ransomware+Israel+OR+Iran+cyber+sabotage&hl=en-US&gl=US&ceid=US:en"
        
        ataques_hoy = []
        try:
            flujo = feedparser.parse(url_ciber)
            for entry in flujo.entries[:5]:
                titulo = entry.get('title', 'Incidente detectado').split(' - ')[0]
                t_low = titulo.lower()
                
                # Clasificación técnica por objetivo
                if any(x in t_low for x in ['energy', 'scada', 'power', 'water']):
                    tipo, color = "SABOTAJE INDUSTRIAL (SCADA)", "red"
                elif any(x in t_low for x in ['bank', 'financial', 'crypto']):
                    tipo, color = "ATAQUE FINANCIERO", "purple"
                else:
                    tipo, color = "ESPIONAJE / DATA LEAK", "orange"

                ataques_hoy.append({
                    "evento": titulo[:85] + "...",
                    "tipo": tipo,
                    "color": color,
                    "coords": [32.0 + random.uniform(-2, 4), 35.0 + random.uniform(-1, 15)]
                })
            return ataques_hoy
        except: return []

    def simular_trafico_real(self, n_ataques):
        """Calcula el pulso de la red basado en la actividad detectada"""
        nivel = n_ataques * 100 + random.randint(50, 200)
        self.estado_red = "AMENAZA CRÍTICA" if nivel > 450 else "AMENAZA ELEVADA"
        return {
            "ataques_severos": n_ataques,
            "ddos_activos": random.randint(4, 12),
            "phishing": random.randint(1500, 3500),
            "intrusion_ids": nivel * 15
        }

    def generar_mapa(self):
        print("\n" + "="*70)
        print("INICIANDO RADAR CIBERNÉTICO E.T.B. v3.0")
        print("="*70)
        
        ataques = self.analizar_amenazas_vivas()
        metricas = self.simular_trafico_real(len(ataques))
        
        mapa = folium.Map(location=[30.0, 45.0], zoom_start=4, tiles='CartoDB dark_matter')
        
        capa_apt = folium.FeatureGroup(name="🎯 Nodos APT (Estatales)").add_to(mapa)
        capa_impacto = folium.FeatureGroup(name="💥 Impactos Confirmados (OSINT)").add_to(mapa)
        capa_vectores = folium.FeatureGroup(name="⚡ Vectores de Propagación").add_to(mapa)

        # 1. Marcadores de Grupos APT
        for nom, d in GRUPOS_CIBER.items():
            folium.Marker(d['coords'], icon=folium.Icon(color=d['color'], icon='user-secret', prefix='fa'),
                          tooltip=f"GRUPO: {nom}").add_to(capa_apt)

        # 2. Ataques Reales Detectados
        for a in ataques:
            popup_html = f"""
            <div style="font-family: 'Courier New', monospace; width: 280px; background: #000; color: #fff; padding: 10px; border-left: 5px solid {a['color']};">
                <b style="color:{a['color']};">💥 {a['tipo']}</b><br><br>
                <b>Reporte:</b> {a['evento']}<br>
                <b>Estado:</b> Bajo Análisis OSINT
            </div>
            """
            folium.CircleMarker(a['coords'], radius=12, color=a['color'], fill=True, 
                                popup=folium.Popup(popup_html, max_width=300)).add_to(capa_impacto)
            
            # Vector desde un atacante aleatorio para visualización
            atacante_nom = random.choice(list(GRUPOS_CIBER.keys()))
            AntPath(locations=[GRUPOS_CIBER[atacante_nom]['coords'], a['coords']], 
                    color=a['color'], weight=2, delay=600).add_to(capa_vectores)

        # Panel de Ciber-Defensa E.T.B.
        color_panel = '#ff0000' if "CRÍTICA" in self.estado_red else '#b000ff'
        timestamp = datetime.datetime.now().strftime('%H:%M')
        panel_html = f"""
        <div style="position: fixed; top: 20px; right: 20px; width: 320px; background: rgba(10,10,10,0.95); 
                    color: #fff; border: 2px solid {color_panel}; padding: 15px; border-radius: 10px; 
                    font-family: 'Courier New', monospace; font-size: 11px; z-index: 9999; box-shadow: 0 0 20px {color_panel}66;">
            <h4 style="color:{color_panel}; text-align:center; margin:0 0 10px 0;">💻 RADAR CIBERNÉTICO E.T.B.</h4>
            <div style="background: {color_panel}33; padding: 8px; border-radius: 5px; text-align: center; border: 1px solid {color_panel};">
                <b style="color:#fff;">ESTADO RED: {self.estado_red}</b>
            </div>
            <div style="margin-top: 10px; line-height: 1.4;">
                <b>TELEMETRÍA DE ATAQUE:</b><br>
                Incidentes Críticos (24h): {metricas['ataques_severos']}<br>
                Botnets DDoS Activos: {metricas['ddos_activos']}<br>
                Pings de Intrusión: {metricas['intrusion_ids']:,}<br><br>
                <b>INTELIGENCIA TÉCNICA:</b><br>
                Foco: {ataques[0]['tipo'] if ataques else "Escaneo de Red"}<br>
                Infraestructura en Riesgo: SCADA / Energía
            </div>
            <div style="margin-top: 12px; border-top: 1px solid #333; padding-top: 8px; font-size: 9px; color: #666; text-align: center;">
                Sincronizado: {timestamp} | Ingeniería Trejos
            </div>
        </div>
        """
        mapa.get_root().html.add_child(folium.Element(panel_html))
        folium.LayerControl().add_to(mapa)
        mapa.save("radar_ciber_guerra.html")
        print(f"[✅ RADAR CIBERNÉTICO REGIONAL GENERADO]")

if __name__ == "__main__":
    radar = RadarCiberGuerra()
    radar.generar_mapa()