import folium
from folium.plugins import MarkerCluster, AntPath
import requests
import datetime
import json
import random

# Configuración
MARINE_TRAFFIC_API = "https://www.marinetraffic.com/en/reports?asset_type=vessels&columns=shipname,shiptype,flag,imo,eta"  # Simulado
BAB_EL_MANDEB = [12.5833, 43.3333]  # Estrecho crítico

# Buques de interés estratégico
BUQUES_CLAVE = {
    # Portaaviones y grupos de batalla
    "USS Eisenhower": {"tipo": "portaaviones", "bandera": "EEUU", "velocidad": 30},
    "USS Gerald R. Ford": {"tipo": "portaaviones", "bandera": "EEUU", "velocidad": 30},
    "USS Carney": {"tipo": "destructor", "bandera": "EEUU", "velocidad": 30},
    "USS Mason": {"tipo": "destructor", "bandera": "EEUU", "velocidad": 30},
    
    # Buques israelíes/objetivo
    "ZIM Shanghai": {"tipo": "carga_contenedores", "bandera": "Israel", "riesgo": "ALTO"},
    "ZIM Texas": {"tipo": "carga_contenedores", "bandera": "Israel", "riesgo": "ALTO"},
    "EL-YAM": {"tipo": "petrolero", "bandera": "Israel", "riesgo": "CRITICO"},
    
    # Buques atacados recientemente
    "Galaxy Leader": {"tipo": "carga_vehiculos", "estado": "secuestrado", "bandera": "Bahamas"},
    "Rubymar": {"tipo": "carga", "estado": "hundido", "bandera": "Belice"},
}

# Rutas marítimas críticas
RUTAS = {
    "ruta_cabo": {
        "nombre": "Desvío por Cabo de Buena Esperanza",
        "puntos": [
            [31.5017, 32.3333],  # Puerto Said
            [29.0, 35.0],        # Mar Rojo sur
            [12.0, 45.0],        # Cuerno de África
            [-35.0, 20.0],       # Cabo
            [-25.0, -45.0],      # Atlántico sur
            [40.0, -70.0],       # EEUU
        ],
        "tiempo_dias": 21,
        "costo_extra": "millones USD"
    },
    "ruta_directa": {
        "nombre": "Ruta directa (Bloqueada)",
        "puntos": [
            [31.5017, 32.3333],
            [29.9, 32.5],        # Canal Suez
            [27.0, 34.0],        # Mar Rojo
            [12.5833, 43.3333],  # Bab el-Mandeb
            [15.0, 55.0],        # Golfo Pérsico
        ],
        "tiempo_dias": 12,
        "estado": "INSEGURO"
    }
}

class RadarMaritimoRojo:
    def __init__(self):
        self.buques_activos = []
        self.incidentes = []
        
    def obtener_datos_ais_simulados(self):
        """Simula datos AIS (Automatic Identification System)"""
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Rastreando transpondedores AIS en zona de conflicto...")
        
        buques = [
            {
                "nombre": "ZIM Shanghai",
                "tipo": "Portacontenedores",
                "bandera": "Israel",
                "posicion": [12.8, 44.5],  # Desviado, evitando Bab el-Mandeb
                "destino": "Singapur",
                "velocidad": 18,
                "estado": "DESVIADO - Evadiendo zona de impacto",
                "riesgo": "ALTO",
                "color": "red"
            },
            {
                "nombre": "Maersk Hartford",
                "tipo": "Portacontenedores",
                "bandera": "Dinamarca",
                "posicion": [12.2, 43.8],
                "destino": "Yeda",
                "velocidad": 12,
                "estado": "ESCOLTADO - Operación Prosperity Guardian",
                "riesgo": "MEDIO",
                "color": "orange"
            },
            {
                "nombre": "Ever Given",
                "tipo": "Portacontenedores",
                "bandera": "Panamá",
                "posicion": [30.0, 32.5],  # Canal Suez
                "destino": "Rotterdam",
                "velocidad": 0,
                "estado": "TRANSITANDO CANAL",
                "riesgo": "BAJO",
                "color": "green"
            },
            {
                "nombre": "USS Eisenhower (CVN-69)",
                "tipo": "Portaaviones",
                "bandera": "EEUU",
                "posicion": [13.5, 43.0],
                "destino": "Patrulla de Combate",
                "velocidad": 25,
                "estado": "PROTEGIENDO RUTA",
                "riesgo": "MILITAR",
                "color": "darkblue"
            },
            {
                "nombre": "HMS Diamond",
                "tipo": "Destructor",
                "bandera": "UK",
                "posicion": [13.2, 43.2],
                "destino": "Escolta",
                "velocidad": 28,
                "estado": "DEFENSA AÉREA ACTIVA",
                "riesgo": "MILITAR",
                "color": "darkblue"
            },
            {
                "nombre": "Galaxy Leader (SECUESTRADO)",
                "tipo": "Car carrier",
                "bandera": "Bahamas",
                "posicion": [14.5, 42.9],  # Hodeida, Yemen
                "destino": "RETENIDO",
                "velocidad": 0,
                "estado": "SECUESTRADO POR MILICIAS",
                "riesgo": "CRITICO",
                "color": "black"
            }
        ]
        
        print(f"   -> {len(buques)} buques de interés estratégico localizados")
        return buques
    
    def obtener_incidentes_houthis(self):
        """Lista de ataques recientes"""
        incidentes = [
            {
                "fecha": "2024-01-12",
                "buque": "Gibraltar Eagle",
                "tipo": "Ataque misilístico balístico",
                "coordenadas": [13.0, 43.5],
                "estado": "Dañado, sin víctimas"
            },
            {
                "fecha": "2024-01-17",
                "buque": "Genco Picardy",
                "tipo": "Impacto de Dron Suicida",
                "coordenadas": [12.8, 44.0],
                "estado": "Daño estructural menor"
            },
            {
                "fecha": "2024-02-18",
                "buque": "Rubymar",
                "tipo": "Impacto Misil Anti-Buque",
                "coordenadas": [13.2, 43.1],
                "estado": "HUNDIDO - Riesgo ambiental"
            }
        ]
        return incidentes
    
    def generar_mapa(self):
        print("\n" + "="*70)
        print("INICIANDO RADAR MARÍTIMO ROJO E.T.B. (PROSPERITY GUARDIAN)")
        print("="*70)
        
        # Mapa centrado en Mar Rojo/Bab el-Mandeb
        mapa = folium.Map(
            location=[15.0, 42.0],
            zoom_start=6,
            tiles='CartoDB dark_matter'
        )
        
        # Capas
        capa_comercial = folium.FeatureGroup(name="🚢 Comercial (Carga)").add_to(mapa)
        capa_militar = folium.FeatureGroup(name="⚓ Militar (OTAN/Coalición)").add_to(mapa)
        capa_riesgo = folium.FeatureGroup(name="⚠️ Buques Objetivo (Israel/Afiliados)").add_to(mapa)
        capa_incidentes = folium.FeatureGroup(name="💥 Zonas de Impacto/Ataques").add_to(mapa)
        capa_rutas = folium.FeatureGroup(name="🛣️ Líneas de Suministro").add_to(mapa)
        
        # 1. Zona de peligro (Bab el-Mandeb)
        folium.Circle(
            location=BAB_EL_MANDEB,
            radius=150000,  # 150km radio de peligro
            color='red',
            fill=True,
            fillColor='red',
            fillOpacity=0.15,
            tooltip="ZONA ROJA: Bloqueo activo"
        ).add_to(capa_riesgo)
        
        folium.Marker(
            location=BAB_EL_MANDEB,
            popup="""
            <div style="font-family: 'Courier New', monospace; width: 220px; background: rgba(0,0,0,0.9); color: white; padding: 10px; border-left: 4px solid red;">
                <b style="color:red;">ESTRECHO BAB EL-MANDEB</b><br>
                Chokepoint Estratégico<br>
                Flujo global bloqueado: ~30%
            </div>
            """,
            icon=folium.Icon(color='red', icon='exclamation-triangle', prefix='fa')
        ).add_to(capa_riesgo)
        
        # 2. Buques activos
        buques = self.obtener_datos_ais_simulados()
        for buque in buques:
            popup_html = f"""
            <div style="font-family: 'Courier New', monospace; width: 280px; 
                        background: rgba(0,0,0,0.95); color: #fff; padding: 12px; 
                        border-radius: 8px; border-left: 5px solid {buque['color']};">
                <b style="color:{buque['color']}; font-size: 16px;">
                    {buque['nombre'].upper()}
                </b><br>
                <hr style="border-color: #333; margin: 8px 0;">
                <b>Tipo:</b> {buque['tipo']}<br>
                <b>Bandera:</b> {buque['bandera']}<br>
                <b>Velocidad:</b> {buque['velocidad']} nudos<br>
                <b>Destino:</b> {buque['destino']}<br>
                <b>Estado:</b> <span style="color:{buque['color']}; font-weight:bold;">{buque['estado']}</span><br>
                <b>Perfil de Riesgo:</b> {buque['riesgo']}
            </div>
            """
            
            # Seleccionar capa
            if "MILITAR" in buque['riesgo']:
                capa_destino = capa_militar
            elif buque['riesgo'] in ["ALTO", "CRITICO"]:
                capa_destino = capa_riesgo
            else:
                capa_destino = capa_comercial
            
            folium.Marker(
                location=buque['posicion'],
                popup=folium.Popup(popup_html, max_width=300),
                icon=folium.Icon(
                    color=buque['color'],
                    icon='ship' if 'MILITAR' not in buque['riesgo'] else 'fighter-jet',
                    prefix='fa'
                ),
                tooltip=f"{buque['nombre']} - {buque['velocidad']}kts"
            ).add_to(capa_destino)
            
            # Vector de movimiento
            if buque['velocidad'] > 0:
                folium.PolyLine(
                    locations=[
                        buque['posicion'],
                        [buque['posicion'][0] + 0.3, buque['posicion'][1] + 0.3]
                    ],
                    color=buque['color'],
                    weight=2,
                    opacity=0.6,
                    dash_array='5'
                ).add_to(capa_destino)
        
        # 3. Incidentes
        incidentes = self.obtener_incidentes_houthis()
        for inc in incidentes:
            folium.CircleMarker(
                location=inc['coordenadas'],
                radius=10,
                color='darkred',
                fill=True,
                fillColor='red',
                fillOpacity=0.7,
                popup=f"""
                <div style="font-family: 'Courier New', monospace; width: 220px; background: rgba(0,0,0,0.9); color: white; padding: 10px; border-left: 4px solid red;">
                    <b style="color:red;">💥 IMPACTO CONFIRMADO</b><br>
                    <b>Objetivo:</b> {inc['buque']}<br>
                    <b>Fecha:</b> {inc['fecha']}<br>
                    <b>Arma:</b> {inc['tipo']}<br>
                    <b>Daño:</b> {inc['estado']}
                </div>
                """
            ).add_to(capa_incidentes)
        
        # 4. Rutas alternativas (Usando AntPath para animación de flujo)
        for nombre_ruta, datos in RUTAS.items():
            color_ruta = '#ff9900' if 'cabo' in nombre_ruta else '#ff0000'
            AntPath(
                locations=datos['puntos'],
                color=color_ruta,
                weight=4,
                opacity=0.6,
                dash_array=[15, 30],
                delay=1000,
                tooltip=f"{datos['nombre']} ({datos.get('tiempo_dias', 0)} días)"
            ).add_to(capa_rutas)
        
        # Panel informativo unificado E.T.B.
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        panel_info = f"""
        <div style="position: fixed; top: 20px; right: 20px; width: 300px; 
                    background-color: rgba(10,10,10,0.95); color: #fff; 
                    border: 2px solid #ff4444; padding: 15px; border-radius: 10px; 
                    font-family: 'Courier New', monospace; font-size: 11px; z-index: 9999;
                    box-shadow: 0 0 20px rgba(255,0,0,0.4);">
            <h4 style="color:#ff4444; margin-top:0; text-align:center; font-size: 14px; 
                       border-bottom: 2px solid #333; padding-bottom: 8px;">
                🚢 RADAR MARÍTIMO ROJO E.T.B.
            </h4>
            <div style="background: rgba(255,0,0,0.2); padding: 8px; border-radius: 5px; 
                        margin: 10px 0; text-align: center; border: 1px solid red;">
                <b style="color:#ff6666; letter-spacing: 1px;">BAB EL-MANDEB: BLOQUEADO</b>
            </div>
            <div style="line-height: 1.6;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span>Buques en Radar:</span>
                    <span style="font-weight:bold;">{len(buques)}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span>Escoltas Militares:</span>
                    <span style="color:#4488ff;">2 Activas</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span>Tráfico Desviado:</span>
                    <span style="color:#ffaa00;">~15% Global</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span>Incidentes/Ataques:</span>
                    <span style="color:#ff4444; font-weight:bold;">{len(incidentes)} Históricos</span>
                </div>
            </div>
            <div style="margin-top: 12px; border-top: 2px solid #333; padding-top: 10px;">
                <b style="color:#ffaa00;">IMPACTO LOGÍSTICO (Ruta Cabo):</b><br>
                Sobrecosto: +2-3 Millones USD/Buque<br>
                Retraso Cadena Suministro: +9/14 días
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
        
        nombre_mapa = "radar_maritimo_rojo.html"
        mapa.save(nombre_mapa)
        
        print(f"\n{'='*70}")
        print(f"[✅ MAPA MARÍTIMO GENERADO]")
        print(f"Archivo: {nombre_mapa}")
        print(f"Capas: Tráfico comercial, Escoltas Militares y Amenazas Activas")
        print(f"{'='*70}\n")

if __name__ == "__main__":
    radar = RadarMaritimoRojo()
    radar.generar_mapa()