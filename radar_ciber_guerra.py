import folium
from folium.plugins import MarkerCluster, AntPath
import datetime
import json
import random

# Grupos de amenazas cibernéticas activos en conflicto
GRUPOS_CIBER = {
    # Irán y proxies
    "APT35 (Charming Kitten)": {
        "pais": "Irán",
        "coords": [35.6892, 51.3890],
        "tipo": "Espionaje",
        "objetivos": "Israel, EEUU, disidentes",
        "tecnicas": "Spear phishing, watering hole",
        "activo": True,
        "color": "red"
    },
    "APT33 (Elfin)": {
        "pais": "Irán",
        "coords": [32.6539, 51.6660],  # Isfahan
        "tipo": "Sabotaje industrial",
        "objetivos": "Energía, defensa",
        "tecnicas": "Shamoon wiper, supply chain",
        "activo": True,
        "color": "red"
    },
    "Emennet Pasargad": {
        "pais": "Irán",
        "coords": [34.6401, 50.8764], # Qom
        "tipo": "Hacktivismo/Sabotaje",
        "objetivos": "Infraestructura crítica Israel",
        "tecnicas": "DDoS, ransomware, defacement",
        "activo": True,
        "color": "darkred"
    },
    # Israel
    "Unit 8200": {
        "pais": "Israel",
        "coords": [32.0853, 34.7818], # Tel Aviv area
        "tipo": "SIGINT/Ciberespionaje",
        "objetivos": "Irán, Hezbollah, Hamas",
        "tecnicas": "Stuxnet, Duqu, Flame",
        "activo": True,
        "color": "blue"
    },
    "Unit 81": {
        "pais": "Israel",
        "coords": [31.7683, 35.2137], # Jerusalem
        "tipo": "Ciberarma física",
        "objetivos": "Instalaciones nucleares iraníes",
        "tecnicas": "Sabotaje SCADA, explosiones",
        "activo": True,
        "color": "darkblue"
    },
    # Hezbollah/Hamas
    "Lebanese Cedar": {
        "pais": "Hezbollah",
        "coords": [33.8938, 35.5018],
        "tipo": "Espionaje telecom",
        "objetivos": "ISP, empresas libanesas",
        "tecnicas": "Backdoors en routers",
        "activo": True,
        "color": "green"
    },
    "Gaza Cybergang": {
        "pais": "Hamas",
        "coords": [31.5017, 34.4668],
        "tipo": "Espionaje militar",
        "objetivos": "IDF, soldados israelíes",
        "tecnicas": "Fake apps, catfishing",
        "activo": True,
        "color": "darkgreen"
    },
    # Grupos hacktivistas
    "Anonymous Sudan": {
        "pais": "Sudán/Rusia",
        "coords": [15.5007, 32.5599],
        "tipo": "Hacktivismo",
        "objetivos": "Israel, EEUU, OTAN",
        "tecnicas": "DDoS masivo",
        "activo": True,
        "color": "orange"
    },
    "KillNet": {
        "pais": "Rusia",
        "coords": [55.7558, 37.6173],
        "tipo": "Hacktivismo pro-ruso",
        "objetivos": "Israel, Ucrania",
        "tecnicas": "DDoS, doxxing",
        "activo": True,
        "color": "purple"
    }
}

# Ataques recientes documentados (Se cruza el atacante con la BD de Grupos)
ATAQUES_CIBER = [
    {
        "fecha": "2024-01-15",
        "atacante": "Emennet Pasargad",
        "victima": "Hospital Ziv (Safed)",
        "tipo": "Ransomware / Data Leak",
        "impacto": "Sistemas offline 6 horas",
        "coords_victima": [32.9642, 35.4984],
        "severidad": "ALTA"
    },
    {
        "fecha": "2024-02-03",
        "atacante": "Unit 8200",
        "victima": "Sistema aduanero puerto Bandar Abbas",
        "tipo": "Sabotaje SCADA",
        "impacto": "Parálisis logística 3 días",
        "coords_victima": [27.1832, 56.2666],
        "severidad": "CRITICA"
    },
    {
        "fecha": "2024-02-20",
        "atacante": "Anonymous Sudan",
        "victima": "Aeropuerto Ben Gurion",
        "tipo": "DDoS Volumétrico",
        "impacto": "Sitios web caídos, check-in lento",
        "coords_victima": [32.0000, 34.8700],
        "severidad": "MEDIA"
    },
    {
        "fecha": "2024-03-01",
        "atacante": "Gaza Cybergang",
        "victima": "Soldados IDF (apps fake de citas)",
        "tipo": "Ingeniería Social / Espionaje",
        "impacto": "Datos de localización robados",
        "coords_victima": [31.5017, 34.4668], # Cerca de la frontera
        "severidad": "ALTA"
    }
]

class RadarCiberGuerra:
    def __init__(self):
        self.estado_red = "AMENAZA ELEVADA"
        
    def simular_trafico_malicioso(self):
        """Simula datos de tráfico malicioso en tiempo real"""
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Escaneando Honeypots y sensores IDS globales...")
        
        metricas = {
            "ataques_dia": random.randint(150, 400),
            "ddos_activos": random.randint(3, 12),
            "phishing_detectado": random.randint(500, 2000),
            "intentos_intrusion": random.randint(1000, 5000)
        }
        
        print(f"   -> Telemetría: {metricas['ataques_dia']} vectores de ataque sostenidos/24h")
        return metricas
    
    def generar_mapa(self):
        print("\n" + "="*70)
        print("INICIANDO RADAR CIBERNÉTICO E.T.B. (APT & CIBERARMAS)")
        print("="*70)
        
        mapa = folium.Map(
            location=[33.0, 45.0],
            zoom_start=5,
            tiles='CartoDB dark_matter'
        )
        
        # Capas
        capa_apt = folium.FeatureGroup(name="🎯 APTs Estatales").add_to(mapa)
        capa_hacktivistas = folium.FeatureGroup(name="🔥 Células Hacktivistas").add_to(mapa)
        capa_ataques = folium.FeatureGroup(name="💥 Ciberataques Confirmados").add_to(mapa)
        capa_vectores = folium.FeatureGroup(name="⚡ Vectores de Ataque").add_to(mapa)
        capa_infraestructura = folium.FeatureGroup(name="🏛️ Infraestructura Crítica").add_to(mapa)
        
        # 1. Grupos de amenazas
        for nombre, datos in GRUPOS_CIBER.items():
            popup_html = f"""
            <div style="font-family: 'Courier New', monospace; width: 280px; 
                        background: rgba(0,0,0,0.95); color: #fff; padding: 12px; 
                        border-radius: 8px; border-left: 5px solid {datos['color']};">
                <b style="color:{datos['color']}; font-size: 16px;">💻 {nombre.upper()}</b><br>
                <hr style="border-color: #333; margin: 8px 0;">
                <b>Afiliación Estatal:</b> {datos['pais']}<br>
                <b>Perfil Operativo:</b> {datos['tipo']}<br>
                <b>Objetivos Primarios:</b> {datos['objetivos']}<br>
                <b>TTPs (Técnicas):</b> {datos['tecnicas']}<br>
                <b>Estado:</b> {'<span style="color:#00ff41; font-weight:bold;">ACTIVO</span>' if datos['activo'] else 'Durmiente'}
            </div>
            """
            
            capa_destino = capa_apt if "APT" in nombre or "Unit" in nombre else capa_hacktivistas
            
            folium.Marker(
                datos['coords'],
                popup=folium.Popup(popup_html, max_width=300),
                icon=folium.Icon(color=datos['color'], icon='user-secret', prefix='fa'),
                tooltip=f"AMENAZA: {nombre} ({datos['pais']})"
            ).add_to(capa_destino)
            
            # Radio de influencia cibernética
            folium.Circle(
                datos['coords'],
                radius=150000,
                color=datos['color'],
                fill=True,
                fillOpacity=0.1,
                weight=1
            ).add_to(capa_destino)
        
        # 2. Ataques recientes y Vectores
        for ataque in ATAQUES_CIBER:
            color_severidad = {"CRITICA": "red", "ALTA": "orange", "MEDIA": "yellow", "BAJA": "green"}.get(ataque['severidad'], 'gray')
            
            # Dibujar el impacto (Víctima)
            folium.CircleMarker(
                ataque['coords_victima'],
                radius=15,
                color=color_severidad,
                fill=True,
                fillColor=color_severidad,
                fillOpacity=0.7,
                popup=f"""
                <div style="font-family: 'Courier New', monospace; width: 250px; background: rgba(0,0,0,0.9); color: white; padding: 10px; border-left: 4px solid {color_severidad};">
                    <b style="color:{color_severidad};">💥 IMPACTO CONFIRMADO</b><br>
                    <b>Vector:</b> {ataque['tipo']}<br>
                    <b>Atacante (Atribución):</b> {ataque['atacante']}<br>
                    <b>Víctima:</b> {ataque['victima']}<br>
                    <b>Daño:</b> {ataque['impacto']}<br>
                    <b>Severidad:</b> {ataque['severidad']}
                </div>
                """
            ).add_to(capa_ataques)
            
            # Dibujar línea desde el atacante hasta la víctima
            if ataque['atacante'] in GRUPOS_CIBER:
                coords_atacante = GRUPOS_CIBER[ataque['atacante']]['coords']
                AntPath(
                    locations=[coords_atacante, ataque['coords_victima']],
                    color=color_severidad,
                    weight=3,
                    opacity=0.6,
                    dash_array=[10, 20],
                    delay=800,
                    tooltip=f"Vector: {ataque['atacante']} -> {ataque['victima']}"
                ).add_to(capa_vectores)

        # 3. Infraestructura crítica israelí (objetivos potenciales)
        infra_objetivos = [
            {"nombre": "Data Center Gov.IL (Jerusalén)", "coords": [31.7683, 35.2137], "tipo": "Gubernamental"},
            {"nombre": "Central Eléctrica Orot Rabin", "coords": [32.4667, 34.8667], "tipo": "Energía (SCADA)"},
            {"nombre": "IXP (Internet Exchange Tel Aviv)", "coords": [32.0853, 34.7818], "tipo": "Telecomunicaciones"},
            {"nombre": "Instalación Portuaria Haifa", "coords": [32.8184, 35.0019], "tipo": "Logística Marítima"},
            {"nombre": "Torre de Control Ben Gurion", "coords": [32.0000, 34.8700], "tipo": "Aviación"},
        ]
        
        for infra in infra_objetivos:
            folium.Marker(
                infra['coords'],
                popup=f"<div style='font-family: Courier New; background:#222; color:#fff; padding:5px;'><b>{infra['nombre']}</b><br>Sector: {infra['tipo']}</div>",
                icon=folium.Icon(color='lightgray', icon='server', prefix='fa'),
                tooltip="Infraestructura Crítica"
            ).add_to(capa_infraestructura)
        
        # Métricas
        metricas = self.simular_trafico_malicioso()
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Panel Informativo Unificado E.T.B.
        panel = f"""
        <div style="position: fixed; top: 20px; right: 20px; width: 320px; 
                    background-color: rgba(10,10,10,0.95); color: #fff; 
                    border: 2px solid #b000ff; padding: 15px; border-radius: 10px; 
                    font-family: 'Courier New', monospace; font-size: 11px; z-index: 9999;
                    box-shadow: 0 0 20px rgba(176,0,255,0.4);">
            <h4 style="color:#b000ff; margin-top:0; text-align:center; font-size: 14px;
                       border-bottom: 2px solid #333; padding-bottom: 8px;">
                💻 RADAR CIBERNÉTICO E.T.B.
            </h4>
            <div style="background: rgba(176,0,255,0.15); padding: 8px; border-radius: 5px; 
                        margin-bottom: 10px; text-align: center; border: 1px solid #b000ff;">
                <b style="color:#e066ff; letter-spacing: 1px;">DEFCON CIBER: {self.estado_red}</b>
            </div>
            <div style="line-height: 1.6;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span>Ataques Severos (24h):</span>
                    <span style="color:#ff6666; font-weight:bold;">{metricas['ataques_dia']}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span>Botnets DDoS Activos:</span>
                    <span style="color:#ffaa00;">{metricas['ddos_activos']}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span>Vectores Phishing:</span>
                    <span style="color:#00ff41;">{metricas['phishing_detectado']}</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span>Pings de Intrusión (IDS):</span>
                    <span style="color:#00aaff;">{metricas['intentos_intrusion']}</span>
                </div>
            </div>
            <div style="margin-top: 12px; border-top: 2px solid #333; padding-top: 10px;">
                <b style="color:#e066ff;">ENTIDADES MONITOREADAS:</b><br>
                Nodos APT (Estatales): {len([n for n in GRUPOS_CIBER.keys() if 'APT' in n or 'Unit' in n])}<br>
                Células Hacktivistas: {len([n for n in GRUPOS_CIBER.keys() if 'APT' not in n and 'Unit' not in n])}<br>
                Infraestructura Riesgo: {len(infra_objetivos)} Sitios
            </div>
            <div style="margin-top: 12px; border-top: 2px solid #333; padding-top: 10px; 
                        font-size: 10px; color: #666; text-align: center;">
                <b>Última actualización:</b><br>
                {timestamp}<br>
                <span style="color: #444;">Sistema E.T.B. v2.0</span>
            </div>
        </div>
        """
        mapa.get_root().html.add_child(folium.Element(panel))
        
        folium.LayerControl(collapsed=False).add_to(mapa)
        
        nombre_mapa = "radar_ciber_guerra.html"
        mapa.save(nombre_mapa)
        
        print(f"\n{'='*70}")
        print(f"[✅ MAPA CIBERNÉTICO GENERADO]")
        print(f"Archivo: {nombre_mapa}")
        print(f"Trazas: Nodos APT, Objetivos SCADA y Vectores de Ransomware")
        print(f"{'='*70}\n")

if __name__ == "__main__":
    radar = RadarCiberGuerra()
    radar.generar_mapa()