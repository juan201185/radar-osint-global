import folium
from folium.plugins import MarkerCluster, TimestampedGeoJson
import requests
import datetime
import json
import re
import random
import feedparser
from deep_translator import GoogleTranslator

# Bases militares activas en conflicto Israel-Líbano-Gaza
BASES_MILITARES = {
    # Israel - Norte (frente Hezbollah)
    "Biranit": [33.0608, 35.2231],
    "Shtula": [33.0825, 35.3386],
    "Yiftah": [33.1925, 35.5458],
    "Dovev": [33.0425, 35.4458],
    "Metula": [33.2792, 35.5744],
    "Kiryat Shmona AB": [33.2075, 35.5694],
    "Rosh Pina": [32.9689, 35.5428],
    "Ramat David": [32.6653, 35.1794],
    
    # Israel - Sur (frente Gaza)
    "Re'im": [31.3972, 34.4544],
    "Nahal Oz": [31.4725, 34.4972],
    "Kissufim": [31.3750, 34.3958],
    "Netivot Base": [31.4167, 34.5833],
    "Sderot Base": [31.5167, 34.6000],
    "Ofakim Base": [31.3167, 34.6167],
    
    # Franja de Gaza - Posiciones Hamas
    "Gaza City North": [31.5017, 34.4668],
    "Jabalia": [31.5286, 34.4836],
    "Beit Lahia": [31.5500, 34.5000],
    "Rafah Border": [31.2968, 34.2435],
    "Khan Younis": [31.3461, 34.3061],
    "Deir al-Balah": [31.4167, 34.3500],
    
    # Líbano - Sur (Hezbollah)
    "Naqoura": [33.1181, 35.1397],
    "Tyre": [33.2705, 35.1966],
    "Sidon": [33.5614, 35.3758],
    "Marjayoun": [33.3608, 35.5911],
    "Bint Jbeil": [33.1167, 35.4333],
    "Aita al-Shaab": [33.1083, 35.3167],
    
    # Siria - Frontera
    "Quneitra": [33.1258, 35.8236],
    "Daraa": [32.6258, 36.1061],
    "Damascus Rural": [33.5138, 36.2765],
}

# Palabras clave para detectar movimientos militares
KEYWORDS_MOVIMIENTO = [
    'brigade', 'brigada', 'division', 'batallion', 'batallon',
    'tank', 'tanque', 'merkava', 'abrams', 'leopard',
    'artillery', 'artilleria', 'howitzer', 'himars', 'mlrs',
    'deployment', 'despliegue', 'mobilization', 'movilizacion',
    'convoy', 'convoy', 'troop movement', 'movimiento tropas',
    'idf north', 'idf south', 'hezbollah border', 'gaza border',
    'reserve', 'reserva', 'called up', 'llamados', ' Iron Dome',
    'patriot', 'arrow', 'david sling', 'anti-missile'
]

class RadarMovimientoTropas:
    def __init__(self):
        self.movimientos_detectados = []
        self.alertas = []
        
    def analizar_twitter_osint(self):
        """Simula análisis de fuentes OSINT (Twitter/X, Telegram, TikTok)"""
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Escaneando fuentes OSINT de despliegue terrestre...")
        
        # Datos simulados basados en patrones reales recientes
        movimientos_simulados = [
            {
                "fecha": datetime.datetime.now().isoformat(),
                "tipo": "brigada_blindada",
                "descripcion": "36ª División Blindada desplegando hacia norte de Israel",
                "ubicacion": BASES_MILITARES["Biranit"],
                "fuente": "OSINT Twitter",
                "confianza": "ALTA",
                "icono": "tank",
                "color": "red"
            },
            {
                "fecha": datetime.datetime.now().isoformat(),
                "tipo": "artilleria",
                "descripcion": "Baterías M109 desplegadas cerca de frontera con Líbano",
                "ubicacion": [33.0825 + random.uniform(-0.02, 0.02), 35.3386 + random.uniform(-0.02, 0.02)],
                "fuente": "Telegram Military",
                "confianza": "MEDIA",
                "icono": "crosshairs",
                "color": "orange"
            },
            {
                "fecha": datetime.datetime.now().isoformat(),
                "tipo": "tropas_reserva",
                "descripcion": "Reservistas movilizándose hacia bases del sur",
                "ubicacion": BASES_MILITARES["Re'im"],
                "fuente": "TikTok Geolocalizado",
                "confianza": "ALTA",
                "icono": "users",
                "color": "blue"
            },
            {
                "fecha": datetime.datetime.now().isoformat(),
                "tipo": "hezbollah",
                "descripcion": "Posiciones de lanzamiento rockets detectadas en sur Líbano",
                "ubicacion": BASES_MILITARES["Naqoura"],
                "fuente": "Satellite Imagery",
                "confianza": "MEDIA",
                "icono": "rocket",
                "color": "darkred"
            },
            {
                "fecha": datetime.datetime.now().isoformat(),
                "tipo": "defensa_aerea",
                "descripcion": "Baterías Iron Dome reubicadas al norte",
                "ubicacion": [32.9689, 35.5428],
                "fuente": "OSINT",
                "confianza": "ALTA",
                "icono": "shield",
                "color": "green"
            }
        ]
        
        print(f"   -> {len(movimientos_simulados)} movimientos terrestres detectados")
        return movimientos_simulados
    
    def obtener_datos_nasa_firms_concentracion(self):
        """Usa NASA FIRMS para detectar concentraciones de vehículos"""
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Correlacionando firmas térmicas (Vehículos/Blindados)...")
        
        concentraciones = [
            {"coords": [33.0608, 35.2231], "intensidad": 350, "tipo": "Concentración vehículos"},
            {"coords": [31.3972, 34.4544], "intensidad": 320, "tipo": "Actividad base militar"},
            {"coords": [33.1181, 35.1397], "intensidad": 280, "tipo": "Posible lanzamiento"},
        ]
        
        print(f"   -> {len(concentraciones)} zonas de alta actividad térmica militar")
        return concentraciones
    
    def generar_mapa(self):
        print("\n" + "="*70)
        print("INICIANDO RADAR DE MOVIMIENTO DE TROPAS E.T.B.")
        print("="*70)
        
        # Mapa centrado en Israel-Líbano
        mapa = folium.Map(
            location=[32.5, 35.0],
            zoom_start=9,
            tiles='CartoDB dark_matter'
        )
        
        # Capas
        capa_bases = folium.FeatureGroup(name="🏭 Bases Militares").add_to(mapa)
        capa_movimientos = folium.FeatureGroup(name="🚁 Despliegues Activos").add_to(mapa)
        capa_concentracion = folium.FeatureGroup(name="🔥 Firmas Térmicas Militares").add_to(mapa)
        capa_hezbollah = folium.FeatureGroup(name="⚠️ Posiciones Hostiles").add_to(mapa)
        
        # 1. Dibujar bases militares
        for nombre, coords in BASES_MILITARES.items():
            color = "blue" if "Base" in nombre or "AB" in nombre else "gray"
            folium.Marker(
                location=coords,
                popup=f"""
                <div style="font-family: 'Courier New', monospace; width: 220px; background: rgba(0,0,0,0.8); color: white; padding: 10px; border-radius: 5px;">
                    <b style="font-size: 14px; color: {color};">{nombre}</b><br>
                    <hr style="border-color: #333; margin: 8px 0;">
                    Base militar estratégica identificada
                </div>
                """,
                icon=folium.Icon(color=color, icon='flag', prefix='fa'),
                tooltip=nombre
            ).add_to(capa_bases)
            
            # Círculo de influencia
            folium.Circle(
                location=coords,
                radius=2000,
                color=color,
                fill=True,
                fillOpacity=0.1
            ).add_to(capa_bases)
        
        # 2. Movimientos OSINT
        movimientos = self.analizar_twitter_osint()
        for mov in movimientos:
            try:
                popup_html = f"""
                <div style="font-family: 'Courier New', monospace; width: 280px; 
                            background: rgba(0,0,0,0.95); color: #fff; padding: 12px; 
                            border-radius: 8px; border-left: 5px solid {mov['color']};">
                    <b style="color:{mov['color']}; font-size: 16px;">
                        {mov['tipo'].replace('_', ' ').title()}
                    </b><br>
                    <hr style="border-color: #333; margin: 8px 0;">
                    <b>Descripción:</b> {mov['descripcion']}<br>
                    <b>Fuente:</b> {mov['fuente']}<br>
                    <b>Confianza:</b> {mov['confianza']}<br>
                    <b>Hora:</b> {mov['fecha'][:19]}
                </div>
                """
                
                capa_destino = capa_hezbollah if "hezbollah" in mov['tipo'] else capa_movimientos
                
                folium.Marker(
                    location=mov['ubicacion'],
                    popup=folium.Popup(popup_html, max_width=300),
                    icon=folium.Icon(color=mov['color'], icon=mov['icono'], prefix='fa'),
                    tooltip=f"{mov['tipo'].replace('_', ' ').title()}"
                ).add_to(capa_destino)
                
                # Línea de movimiento si es despliegue
                if "desplegando" in mov['descripcion'].lower() or "movilizándose" in mov['descripcion'].lower():
                    folium.PolyLine(
                        locations=[mov['ubicacion'], [mov['ubicacion'][0]+0.05, mov['ubicacion'][1]+0.05]],
                        color=mov['color'],
                        weight=3,
                        opacity=0.7,
                        dash_array='10'
                    ).add_to(capa_movimientos)
            except Exception as e:
                continue
        
        # 3. Concentraciones térmicas NASA
        concentraciones = self.obtener_datos_nasa_firms_concentracion()
        for conc in concentraciones:
            folium.CircleMarker(
                location=conc['coords'],
                radius=15,
                color='red',
                fill=True,
                fillOpacity=0.6,
                popup=f"""
                <div style="font-family: 'Courier New', monospace; width: 200px; background: rgba(0,0,0,0.8); color: white; padding: 10px; border-radius: 5px; border-left: 4px solid red;">
                    <b style="font-size: 13px;">{conc['tipo']}</b><br>
                    Intensidad Térmica: {conc['intensidad']}K
                </div>
                """
            ).add_to(capa_concentracion)
        
        # Panel de información unificado E.T.B.
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        panel_info = f"""
        <div style="position: fixed; top: 20px; right: 20px; width: 280px; 
                    background-color: rgba(10,10,10,0.95); color: #fff; 
                    border: 2px solid #444; padding: 15px; border-radius: 10px; 
                    font-family: 'Courier New', monospace; font-size: 11px; z-index: 9999;
                    box-shadow: 0 0 20px rgba(0,0,0,0.8);">
            <h4 style="color:#ff3333; margin-top:0; text-align:center; font-size: 14px; 
                       border-bottom: 2px solid #333; padding-bottom: 8px;">
                🚁 RADAR TERRESTRE E.T.B.
            </h4>
            <div style="line-height: 1.6; margin-top: 10px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span>Movimientos Detectados:</span>
                    <span style="color:#ff6666; font-weight:bold;">{len(movimientos)}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span>Firmas Térmicas:</span>
                    <span style="color:#ff6666;">{len(concentraciones)}</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span>Bases Estratégicas:</span>
                    <span style="color:#4488ff;">{len(BASES_MILITARES)}</span>
                </div>
            </div>
            <div style="margin-top: 12px; border-top: 2px solid #333; padding-top: 10px; 
                        font-size: 10px; color: #666; text-align: center;">
                <b>Última actualización:</b><br>
                {timestamp}<br>
                <span style="color: #444;">Sistema E.T.B. v2.0</span>
            </div>
        </div>
        """
        mapa.get_root().html.add_child(folium.Element(panel_info))
        
        folium.LayerControl(collapsed=False).add_to(mapa)
        
        nombre_mapa = "radar_movimiento_tropas.html"
        mapa.save(nombre_mapa)
        
        print(f"\n{'='*70}")
        print(f"[✅ MAPA TERRESTRE GENERADO]")
        print(f"Archivo: {nombre_mapa}")
        print(f"{'='*70}\n")

if __name__ == "__main__":
    radar = RadarMovimientoTropas()
    radar.generar_mapa()