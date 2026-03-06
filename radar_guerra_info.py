import folium
from folium.plugins import MarkerCluster, AntPath
import datetime
import json
import random

# Narrativas contradictorias detectadas (mismo evento, versiones opuestas)
NARRATIVAS_CONFLICTIVAS = [
    {
        "evento": "Explosión hospital Al-Ahli",
        "fecha": "2023-10-17",
        "coords": [31.5117, 34.4608],
        "version_occidente": "Fallo de cohete islamista (PIJ)",
        "version_resistencia": "Bombardeo israelí deliberado",
        "evidencia": "Contradictoria / Guerra de OSINT",
        "impacto": "Alta tensión diplomática"
    },
    {
        "evento": "Reportes Kfar Aza (7 Oct)",
        "fecha": "2023-10-10",
        "coords": [31.5017, 34.4668],
        "version_occidente": "Confirmado por fuentes IDF/Prensa",
        "version_resistencia": "Negado sistemáticamente por Hamas",
        "evidencia": "Alta niebla de guerra / Guerra Psicológica",
        "impacto": "Polarización extrema global"
    },
    {
        "evento": "Ataque Consulado Irán Damasco",
        "fecha": "2024-04-01",
        "coords": [33.5138, 36.2765],
        "version_occidente": "Golpe a generales IRGC (Legítimo)",
        "version_resistencia": "Violación soberanía, acto terrorista",
        "evidencia": "Confirmación tácita de Israel",
        "impacto": "Escalada directa Irán-Israel"
    }
]

# Campañas de bots detectadas (con vectores de propagación)
CAMPANAS_BOTS = [
    {
        "nombre": "Operación Tormenta de Almas",
        "plataforma": "Twitter/X, Telegram",
        "origen_estimado": "Teherán",
        "coords_origen": [35.6892, 51.3890],
        "coords_objetivo": [31.5, 34.5], # Hacia Israel/Gaza
        "objetivo": "Justificar operaciones del Eje de Resistencia",
        "hashtags": ["#PalestinaLibre", "#EjeDeLaResistencia"],
        "volumen": "500K posts/24h",
        "cuentas_suspendidas": 1200
    },
    {
        "nombre": "Campaña Hasbara Digital",
        "plataforma": "Twitter/X, TikTok",
        "origen_estimado": "Jerusalén",
        "coords_origen": [31.7683, 35.2137],
        "coords_objetivo": [48.8566, 2.3522], # Hacia Europa/Occidente
        "objetivo": "Contrarrestar narrativa pro-palestina en Europa",
        "hashtags": ["#IsraelUnderAttack", "#HamasIsISIS"],
        "volumen": "800K posts/24h",
        "cuentas_suspendidas": 800
    },
    {
        "nombre": "Operación Doppelgänger",
        "plataforma": "Facebook, Redes Alt-Tech",
        "origen_estimado": "Moscú",
        "coords_origen": [55.7558, 37.6173],
        "coords_objetivo": [38.9072, -77.0369], # Hacia EEUU
        "objetivo": "Agotamiento de ayuda militar / División política",
        "hashtags": ["#StopTheWar", "#AmericaFirst"],
        "volumen": "1.2M interacciones",
        "cuentas_suspendidas": 2000
    }
]

# Deepfakes y desinformación detectada
DEEPFAKES_DETECTADOS = [
    {
        "titulo": "Audio sintetizado: Negociaciones encubiertas",
        "plataforma": "Telegram",
        "fecha": "2024-02-15",
        "veredicto": "FAKE - Audio clonado por IA",
        "alcance": "2M visualizaciones",
        "coords": [31.5017, 34.4668] # Difundido en Gaza/Cisjordania
    },
    {
        "titulo": "Video CGI: Impacto directo en base aérea",
        "plataforma": "TikTok",
        "fecha": "2024-03-10",
        "veredicto": "FAKE - Imágenes de videojuego ARMA 3",
        "alcance": "5M visualizaciones",
        "coords": [32.6653, 35.1794] # Supuesta base Ramat David
    }
]

class RadarGuerraInfo:
    def __init__(self):
        self.indice_desinformacion = "ELEVADO (NIVEL 4)"
        
    def analizar_tendencias(self):
        """Simula análisis de tendencias virales y NLP"""
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Rastreando granjas de bots y flujos narrativos...")
        
        tendencias = {
            "hashtag_activo": "#EscaladaMedioOriente",
            "volumen_global": "2.3M menciones/hora",
            "sentimiento": "Negativo/Hostil 78%",
            "bots_detectados": random.randint(5000, 15000)
        }
        
        print(f"   -> Telemetría: {tendencias['volumen_global']} con fuerte actividad automatizada.")
        return tendencias
    
    def generar_mapa(self):
        print("\n" + "="*70)
        print("INICIANDO RADAR DE GUERRA INFORMACIONAL E.T.B. (PSYOPs)")
        print("="*70)
        
        mapa = folium.Map(
            location=[35.0, 20.0],
            zoom_start=4,
            tiles='CartoDB dark_matter'
        )
        
        # Capas
        capa_narrativas = folium.FeatureGroup(name="⚔️ Choques Narrativos").add_to(mapa)
        capa_bots = folium.FeatureGroup(name="🤖 Nodos Botnet / Operaciones de Info").add_to(mapa)
        capa_flujos = folium.FeatureGroup(name="📡 Vectores de Propagación Digital").add_to(mapa)
        capa_deepfakes = folium.FeatureGroup(name="🎭 Deepfakes / Desinformación IA").add_to(mapa)
        capa_tendencias = folium.FeatureGroup(name="📈 Medios y Amplificadores").add_to(mapa)
        
        # 1. Eventos con narrativas contradictorias
        for evento in NARRATIVAS_CONFLICTIVAS:
            popup_html = f"""
            <div style="font-family: 'Courier New', monospace; width: 320px; 
                        background: rgba(0,0,0,0.95); color: #fff; padding: 12px; 
                        border-radius: 8px; border-left: 5px solid #ff00ff;">
                <b style="color:#ff00ff; font-size: 16px;">⚔️ BATALLA COGNITIVA</b><br>
                <b style="color:#aaa;">{evento['evento']}</b><br>
                <hr style="border-color: #333; margin: 8px 0;">
                <b>Fecha de Inserción:</b> {evento['fecha']}<br>
                <div style="background: rgba(0,100,255,0.15); padding: 5px; margin: 8px 0; border-radius: 3px; border: 1px solid #0066ff;">
                    <b style="color:#00aaff;">Narrativa Bloque Occidental:</b><br>{evento['version_occidente']}
                </div>
                <div style="background: rgba(255,0,0,0.15); padding: 5px; margin: 8px 0; border-radius: 3px; border: 1px solid #ff0000;">
                    <b style="color:#ff4444;">Narrativa Eje Resistencia:</b><br>{evento['version_resistencia']}
                </div>
                <b>Estado de Evidencia:</b> {evento['evidencia']}<br>
                <b>Impacto Estratégico:</b> <span style="color:#ffaa00; font-weight:bold;">{evento['impacto']}</span>
            </div>
            """
            
            folium.Marker(
                evento['coords'],
                popup=folium.Popup(popup_html, max_width=340),
                icon=folium.Icon(color='purple', icon='bullhorn', prefix='fa'),
                tooltip=f"Fricción Informativa: {evento['evento'][:20]}..."
            ).add_to(capa_narrativas)
        
        # 2. Campañas de bots y sus Vectores
        for campana in CAMPANAS_BOTS:
            popup_html = f"""
            <div style="font-family: 'Courier New', monospace; width: 280px; 
                        background: rgba(0,0,0,0.95); color: #fff; padding: 12px; 
                        border-radius: 8px; border-left: 5px solid #00ffff;">
                <b style="color:#00ffff; font-size: 16px;">🤖 {campana['nombre'].upper()}</b><br>
                <hr style="border-color: #333; margin: 8px 0;">
                <b>Vector Cero:</b> {campana['origen_estimado']}<br>
                <b>Plataformas:</b> {campana['plataforma']}<br>
                <b>Directriz:</b> {campana['objetivo']}<br>
                <b>Carga Viral (Tags):</b> {', '.join(campana['hashtags'])}<br>
                <b>Volumen Inyectado:</b> <span style="color:#ffaa00;">{campana['volumen']}</span><br>
                <b>Bajas (Cuentas Caídas):</b> {campana['cuentas_suspendidas']}
            </div>
            """
            
            # Marcador de origen de la granja de bots
            folium.Marker(
                campana['coords_origen'],
                popup=folium.Popup(popup_html, max_width=300),
                icon=folium.Icon(color='lightblue', icon='robot', prefix='fa'),
                tooltip=f"Botnet Activa: {campana['nombre']}"
            ).add_to(capa_bots)
            
            # Vector de propagación (AntPath simulando datos)
            AntPath(
                locations=[campana['coords_origen'], campana['coords_objetivo']],
                color='#00ffff',
                weight=3,
                opacity=0.6,
                dash_array=[10, 15],
                delay=800,
                tooltip=f"Flujo Botnet: {campana['origen_estimado']} -> Objetivo"
            ).add_to(capa_flujos)
        
        # 3. Deepfakes
        for fake in DEEPFAKES_DETECTADOS:
            folium.Marker(
                fake['coords'],
                popup=f"""
                <div style="font-family: 'Courier New', monospace; width: 220px; background: rgba(0,0,0,0.9); color: white; padding: 10px; border-left: 4px solid #ff66b2;">
                    <b style="color:#ff66b2;">🎭 ENGAÑO GENERATIVO (IA)</b><br>
                    <b>Contenido:</b> {fake['titulo']}<br>
                    <b>Vector:</b> {fake['plataforma']}<br>
                    <b>Análisis OSINT:</b> <span style="color:#ff4444;">{fake['veredicto']}</span><br>
                    <b>Infección:</b> {fake['alcance']}
                </div>
                """,
                icon=folium.Icon(color='pink', icon='microchip', prefix='fa'),
                tooltip="Contenido Sintético Detectado"
            ).add_to(capa_deepfakes)
        
        # 4. Centros de narrativa (sedes de medios)
        centros_narrativa = [
            {"nombre": "Al Jazeera (Hub)", "coords": [25.2854, 51.5310], "inclinacion": "Pro-Eje Resistencia / Qatar"},
            {"nombre": "BBC / Reuters", "coords": [51.5074, -0.1278], "inclinacion": "Visión OTAN / Occidental"},
            {"nombre": "RT / Sputnik", "coords": [55.7558, 37.6173], "inclinacion": "Narrativa Estado Ruso"},
            {"nombre": "Medios Estatales / Hasbara", "coords": [32.0853, 34.7818], "inclinacion": "Doctrina Oficial Israelí"},
            {"nombre": "Press TV / IRIB", "coords": [35.6892, 51.3890], "inclinacion": "Doctrina Estado Iraní"},
        ]
        
        for centro in centros_narrativa:
            folium.CircleMarker(
                centro['coords'],
                radius=10,
                color='white',
                fill=True,
                fillColor='#444',
                fillOpacity=0.8,
                popup=f"<div style='font-family: Courier New; background:#222; color:#fff; padding:5px;'><b>📡 {centro['nombre']}</b><br>Línea Editorial: {centro['inclinacion']}</div>"
            ).add_to(capa_tendencias)
        
        # Análisis y Tendencias
        tendencias = self.analizar_tendencias()
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Panel Informativo Unificado E.T.B.
        panel = f"""
        <div style="position: fixed; top: 20px; right: 20px; width: 320px; 
                    background-color: rgba(10,10,10,0.95); color: #fff; 
                    border: 2px solid #00ffff; padding: 15px; border-radius: 10px; 
                    font-family: 'Courier New', monospace; font-size: 11px; z-index: 9999;
                    box-shadow: 0 0 20px rgba(0,255,255,0.4);">
            <h4 style="color:#00ffff; margin-top:0; text-align:center; font-size: 14px;
                       border-bottom: 2px solid #333; padding-bottom: 8px;">
                👁️‍🗨️ RADAR GUERRA INFORMACIONAL
            </h4>
            <div style="background: rgba(0,255,255,0.15); padding: 8px; border-radius: 5px; 
                        margin-bottom: 10px; text-align: center; border: 1px solid #00ffff;">
                <b style="color:#00ffff; letter-spacing: 1px;">ÍNDICE DESINFORMACIÓN: {self.indice_desinformacion}</b>
            </div>
            <div style="line-height: 1.6;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span>Vector Viral Activo:</span>
                    <span style="color:#ff00ff; font-weight:bold;">{tendencias['hashtag_activo']}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span>Tasa de Propagación:</span>
                    <span style="color:#00ff41;">{tendencias['volumen_global']}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span>Análisis Sentimiento:</span>
                    <span style="color:#ff6666;">{tendencias['sentimiento']}</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span>Cuentas Inauténticas:</span>
                    <span style="color:#ffaa00;">~{tendencias['bots_detectados']:,} Nodos</span>
                </div>
            </div>
            <div style="margin-top: 12px; border-top: 2px solid #333; padding-top: 10px;">
                <b style="color:#00ffff;">ENTIDADES MONITOREADAS:</b><br>
                Zonas de Fricción Narrativa: {len(NARRATIVAS_CONFLICTIVAS)} Eventos<br>
                Granjas de Bots Activas: {len(CAMPANAS_BOTS)} Operaciones<br>
                Ataques Sintéticos (IA): {len(DEEPFAKES_DETECTADOS)} Casos
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
        
        nombre_mapa = "radar_guerra_info.html"
        mapa.save(nombre_mapa)
        
        print(f"\n{'='*70}")
        print(f"[✅ MAPA DE GUERRA INFORMACIONAL GENERADO]")
        print(f"Archivo: {nombre_mapa}")
        print(f"Capas: Nodos Botnet, Fricciones Narrativas y Vectores de IA")
        print(f"{'='*70}\n")

if __name__ == "__main__":
    radar = RadarGuerraInfo()
    radar.generar_mapa()