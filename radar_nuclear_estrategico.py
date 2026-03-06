import folium
from folium.plugins import MarkerCluster
import requests
import datetime
import json
import random

# Instalaciones nucleares iraníes (IAEA y OSINT)
INSTALACIONES_NUCLEAR_IRAN = {
    "Natanz": {
        "coords": [33.7233, 51.7267],
        "tipo": "Enriquecimiento Uranio",
        "estado": "Activo - Subterráneo fortificado",
        "enriquecimiento": "60% (cerca de armas)",
        "centrifugas": "~5,000 IR-2m/IR-4",
        "proteccion": "AA S-300, búnker subterráneo",
        "riesgo": "CRITICO",
        "ultimo_ataque": "2021-04-11 (Sabotaje)"
    },
    "Fordow": {
        "coords": [34.8858, 50.9958],
        "tipo": "Enriquecimiento altamente enriquecido",
        "estado": "Activo - Montaña fortificada",
        "enriquecimiento": "20% y 60%",
        "centrifugas": "~1,000 IR-6",
        "proteccion": "Inexpugnable aéreo (montaña)",
        "riesgo": "CRITICO",
        "ultimo_ataque": "Ninguno"
    },
    "Isfahan": {
        "coords": [32.6804, 51.6861],
        "tipo": "Conversión y laboratorios",
        "estado": "Activo",
        "enriquecimiento": "N/A (investigación)",
        "riesgo": "ALTO",
        "ultimo_ataque": "Ninguno"
    },
    "Arak": {
        "coords": [34.3747, 49.4736],
        "tipo": "Reactor agua pesada (plutonio)",
        "estado": "Rediseñado (JCPOA)",
        "enriquecimiento": "N/A",
        "riesgo": "MEDIO",
        "ultimo_ataque": "Ninguno"
    },
    "Parchin": {
        "coords": [35.5156, 51.8311],
        "tipo": "Investigación explosivos nucleares",
        "estado": "Sospechoso - Limpieza IAEA",
        "enriquecimiento": "Desconocido",
        "riesgo": "ALTO",
        "ultimo_ataque": "Ninguno"
    },
    "Bushehr": {
        "coords": [28.8283, 50.8839],
        "tipo": "Reactor nuclear civil (Rusia)",
        "estado": "Operativo",
        "enriquecimiento": "Combustible ruso",
        "riesgo": "BAJO",
        "ultimo_ataque": "Ninguno"
    }
}

# Submarinos nucleares israelíes (clase Dolphin - presunto armamento nuclear)
SUBMARINOS_ISRAEL = {
    "Dolphin": {
        "base": "Haifa",
        "coords": [32.8184, 35.0019],
        "estado": "En patrulla (presunto)",
        "armamento": "Popeye Turbo SLCM (nuclear)",
        "alcance": "1,500 km",
        "ultimo_avistamiento": "2024-01-15"
    },
    "Leviathan": {
        "base": "Haifa",
        "coords": [32.8184, 35.0019],
        "estado": "En mantenimiento",
        "armamento": "Popeye Turbo SLCM",
        "alcance": "1,500 km",
        "ultimo_avistamiento": "2023-12-20"
    },
    "Tekumah": {
        "base": "Haifa",
        "coords": [32.8184, 35.0019],
        "estado": "Desplegado Mar Rojo",
        "armamento": "Popeye Turbo SLCM",
        "alcance": "1,500 km",
        "ultimo_avistamiento": "2024-02-10"
    }
}

# Eventos sísmicos sospechosos (pruebas nucleares subterráneas)
EVENTOS_SISMICOS = [
    {"fecha": "2024-01-05", "magnitud": 4.2, "coords": [33.5, 51.5], "sospecha": "Test subterráneo Irán", "profundidad": "0km (superficial)"},
    {"fecha": "2023-11-12", "magnitud": 3.8, "coords": [35.0, 50.0], "sospecha": "Explosión túnel", "profundidad": "5km"},
]

class RadarNuclearEstrategico:
    def __init__(self):
        self.nivel_alerta = "AMARILLO"  # ROJO, NARANJA, AMARILLO, VERDE
        self.tiempo_breakout = "1-2 semanas"  # Tiempo estimado para arma
        
    def simular_inteligencia_iaea(self):
        """Simula datos de reportes IAEA y satélites"""
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Escaneando matrices de inteligencia IAEA...")
        
        reporte = {
            "uranio_enriquecido_total": "121.5 kg",
            "uranio_60_porciento": "87.5 kg",
            "suficiente_para_bombas": "2-3 dispositivos",
            "ultima_inspeccion_iaea": "2024-02-15",
            "cooperacion_iran": "Mínima - Bloqueo a sitios militares"
        }
        
        print(f"   -> Stockpile Detectado: {reporte['uranio_enriquecido_total']}")
        print(f"   -> Capacidad Material: {reporte['suficiente_para_bombas']}")
        return reporte
    
    def obtener_submarinos_activos(self):
        """Simula posiciones de submarinos israelíes (ultrasecreto)"""
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Rastreando red de disuasión estratégica (Clase Dolphin)...")
        
        posiciones_estimadas = [
            {
                "nombre": "Dolphin",
                "posicion_estimada": [25.0, 55.0],  # Golfo Pérsico
                "estado": "Patrulla disuasión",
                "mensaje": "Capacidad de Segundo Ataque (Second Strike)",
                "armamento": "Popeye Turbo SLCM (Nuclear)", # <- DATO AGREGADO
                "alcance": "1,500 km"                       # <- DATO AGREGADO
            },
            {
                "nombre": "Tekumah",
                "posicion_estimada": [20.0, 38.0],  # Mar Rojo
                "estado": "Cubriendo flanco Sur (Yemen/Irán)",
                "mensaje": "Alcance balístico a Teherán confirmado",
                "armamento": "Popeye Turbo SLCM (Nuclear)", # <- DATO AGREGADO
                "alcance": "1,500 km"                       # <- DATO AGREGADO
            }
        ]
        
        print(f"   -> {len(posiciones_estimadas)} submarinos con capacidad nuclear en patrulla")
        return posiciones_estimadas
    
    def generar_mapa(self):
        print("\n" + "="*70)
        print("INICIANDO RADAR NUCLEAR ESTRATÉGICO E.T.B.")
        print("="*70)
        
        mapa = folium.Map(
            location=[30.0, 45.0],
            zoom_start=5,
            tiles='CartoDB dark_matter'
        )
        
        # Capas Tácticas
        capa_enriquecimiento = folium.FeatureGroup(name="☢️ Nodos de Enriquecimiento (Uranio)").add_to(mapa)
        capa_reactores = folium.FeatureGroup(name="⚛️ Reactores de Agua Pesada/Investigación").add_to(mapa)
        capa_submarinos = folium.FeatureGroup(name="🚀 Disuasión Naval Israelí").add_to(mapa)
        capa_sismicos = folium.FeatureGroup(name="💥 Anomalías Sísmicas (Pruebas)").add_to(mapa)
        capa_alcance = folium.FeatureGroup(name="🎯 Radios de Cobertura (SLCM)").add_to(mapa)
        
        # 1. Instalaciones iraníes
        for nombre, datos in INSTALACIONES_NUCLEAR_IRAN.items():
            color = {
                "CRITICO": "red",
                "ALTO": "orange",
                "MEDIO": "beige", # <- CORRECCIÓN DE COLOR (Adiós yellow)
                "BAJO": "green"
            }.get(datos.get('riesgo'), 'gray')
            
            popup_html = f"""
            <div style="font-family: 'Courier New', monospace; width: 300px; 
                        background: rgba(0,0,0,0.95); color: #fff; padding: 12px; 
                        border-radius: 8px; border-left: 5px solid {color};">
                <b style="color:{color}; font-size: 16px;">☢️ {nombre.upper()}</b><br>
                <hr style="border-color: #333; margin: 8px 0;">
                <b>Perfil:</b> {datos.get('tipo', 'Desconocido')}<br>
                <b>Estado:</b> {datos.get('estado', 'Desconocido')}<br>
                <b>Nivel Enriquecimiento:</b> <span style="color:#ffcc00;">{datos.get('enriquecimiento', 'N/A')}</span><br>
                <b>Vector (Centrífugas):</b> {datos.get('centrifugas', 'Desconocido')}<br>
                <b>Blindaje/Defensa:</b> {datos.get('proteccion', 'Clasificado / No Determinado')}<br>
                <b>Nivel de Riesgo:</b> <span style="color:{color}; font-weight:bold;">{datos.get('riesgo', 'Desconocido')}</span><br>
                <b>Último Sabotaje:</b> {datos.get('ultimo_ataque', 'Ninguno')}
            </div>
            """
            
            folium.Marker(
                datos['coords'],
                popup=folium.Popup(popup_html, max_width=320),
                icon=folium.Icon(color=color, icon='radiation', prefix='fa'),
                tooltip=f"INSTALACIÓN: {nombre} - Riesgo: {datos.get('riesgo', 'Desconocido')}"
            ).add_to(capa_enriquecimiento if "Enriquecimiento" in datos.get('tipo', '') else capa_reactores)
            
            # Círculo de protección AA
            folium.Circle(
                datos['coords'],
                radius=15000,
                color=color,
                fill=True,
                fillOpacity=0.15,
                weight=1
            ).add_to(capa_enriquecimiento)
        
        # 2. Submarinos israelíes (posiciones estimadas)
        subs = self.obtener_submarinos_activos()
        for sub in subs:
            folium.Circle(
                sub['posicion_estimada'],
                radius=400000,  # 400km incertidumbre
                color='#0066cc',
                fill=True,
                fillColor='#0066cc',
                fillOpacity=0.1,
                popup=f"Zona de Patrulla Estimada: {sub['nombre']}"
            ).add_to(capa_submarinos)
            
            # <- PROTECCIÓN GET APLICADA AQUÍ PARA EVITAR KEYERRORS
            popup_sub = f"""
            <div style="font-family: 'Courier New', monospace; width: 280px; 
                        background: rgba(0,0,0,0.95); color: #fff; padding: 12px; 
                        border-radius: 8px; border-left: 5px solid #0066cc;">
                <b style="color:#00aaff; font-size: 16px;">🚀 CLASE DOLPHIN ({sub.get('nombre', 'Desconocido')})</b><br>
                <hr style="border-color: #333; margin: 8px 0;">
                <b>Estado:</b> {sub.get('estado', 'Desconocido')}<br>
                <b>Carga Bélica:</b> <span style="color:#ff4444;">{sub.get('armamento', 'Clasificada')}</span><br>
                <b>Radio de Acción:</b> {sub.get('alcance', 'Desconocido')}<br>
                <b>Doctrina:</b> <i>{sub.get('mensaje', 'Desconocida')}</i>
            </div>
            """
            
            folium.Marker(
                sub['posicion_estimada'],
                popup=folium.Popup(popup_sub, max_width=300),
                icon=folium.Icon(color='darkblue', icon='submarine', prefix='fa'),
                tooltip="DISUASIÓN ACTIVA"
            ).add_to(capa_submarinos)
            
            # Alcance de misiles (1,500 km)
            folium.Circle(
                sub['posicion_estimada'],
                radius=1500000,
                color='red',
                fill=False,
                weight=2,
                dash_array='10, 15',
                popup=f"Envolvente Táctica SLCM ({sub.get('nombre', 'Desconocido')})"
            ).add_to(capa_alcance)
        
        # 3. Eventos sísmicos sospechosos
        for evento in EVENTOS_SISMICOS:
            popup_sismo = f"""
            <div style="font-family: 'Courier New', monospace; width: 250px; 
                        background: rgba(0,0,0,0.95); color: #fff; padding: 12px; 
                        border-radius: 8px; border-left: 5px solid purple;">
                <b style="color:#cc66ff; font-size: 14px;">💥 ANOMALÍA SÍSMICA</b><br>
                <hr style="border-color: #333; margin: 8px 0;">
                <b>Fecha:</b> {evento.get('fecha', 'Desconocida')}<br>
                <b>Escala Richter:</b> {evento.get('magnitud', 'N/A')}<br>
                <b>Profundidad:</b> {evento.get('profundidad', 'Desconocida')}<br>
                <b>Evaluación de Inteligencia:</b><br>
                <span style="color:#ffcc00;">{evento.get('sospecha', 'Desconocida')}</span>
            </div>
            """
            folium.CircleMarker(
                evento['coords'],
                radius=evento['magnitud'] * 4,
                color='purple',
                fill=True,
                fillColor='purple',
                fillOpacity=0.6,
                popup=folium.Popup(popup_sismo, max_width=280)
            ).add_to(capa_sismicos)
        
        # Reporte IAEA
        reporte = self.simular_inteligencia_iaea()
        
        # Colores dinámicos del panel según la alerta
        color_alerta = '#ff0000' if self.nivel_alerta == 'ROJO' else '#ffaa00' if self.nivel_alerta == 'AMARILLO' else '#00ff41'
        shadow_alerta = 'rgba(255,0,0,0.5)' if self.nivel_alerta == 'ROJO' else 'rgba(255,170,0,0.4)' if self.nivel_alerta == 'AMARILLO' else 'rgba(0,255,65,0.3)'
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Panel de alerta nuclear E.T.B.
        panel = f"""
        <div style="position: fixed; top: 20px; right: 20px; width: 320px; 
                    background-color: rgba(10,10,10,0.95); color: #fff; 
                    border: 2px solid {color_alerta}; 
                    padding: 15px; border-radius: 10px; 
                    font-family: 'Courier New', monospace; font-size: 11px; z-index: 9999;
                    box-shadow: 0 0 25px {shadow_alerta};">
            <h4 style="color:{color_alerta}; margin-top:0; text-align:center; font-size: 14px;
                       border-bottom: 2px solid #333; padding-bottom: 8px;">
                ☢️ ALERTA ESTRATÉGICA: {self.nivel_alerta}
            </h4>
            <div style="background: rgba(255,255,255,0.05); padding: 8px; border-radius: 5px; 
                        margin-bottom: 10px; text-align: center; border: 1px solid {color_alerta};">
                <b style="color:{color_alerta}; font-size: 12px; letter-spacing: 1px;">BREAKOUT TIME: {self.tiempo_breakout}</b>
            </div>
            <div style="line-height: 1.6;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span>Inventario Uranio 60%:</span>
                    <span style="color:#ff6666; font-weight:bold;">{reporte.get('uranio_60_porciento', 'N/A')}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span>Enriquecido Total:</span>
                    <span style="color:#ffcc00;">{reporte.get('uranio_enriquecido_total', 'N/A')}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span>Capacidad Teórica:</span>
                    <span style="color:#ff4444; font-weight:bold;">{reporte.get('suficiente_para_bombas', 'N/A')}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span>Instalaciones Críticas:</span>
                    <span style="color:#ff4444;">{len([i for i in INSTALACIONES_NUCLEAR_IRAN.values() if i.get('riesgo') == 'CRITICO'])} Sitios</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span>Disuasión Naval (Subs):</span>
                    <span style="color:#4488ff;">{len(subs)} en Patrulla</span>
                </div>
            </div>
            <div style="margin-top: 12px; border-top: 2px solid #333; padding-top: 10px; 
                        font-size: 10px; color: #aaa;">
                <b>Acceso IAEA:</b> {reporte.get('cooperacion_iran', 'N/A')}<br>
                <b>Inspección OIEA:</b> {reporte.get('ultima_inspeccion_iaea', 'N/A')}
            </div>
            <div style="margin-top: 10px; text-align: center; color: #666; font-size: 9px;">
                Actualizado: {timestamp}<br>
                Sistema E.T.B. v2.0
            </div>
        </div>
        """
        mapa.get_root().html.add_child(folium.Element(panel))
        
        folium.LayerControl(collapsed=False).add_to(mapa)
        
        nombre_mapa = "radar_nuclear_estrategico.html"
        mapa.save(nombre_mapa)
        
        print(f"\n{'='*70}")
        print(f"[✅ MAPA NUCLEAR ESTRATÉGICO GENERADO]")
        print(f"Archivo: {nombre_mapa}")
        print(f"Estado de red: {self.nivel_alerta} | Breakout: {self.tiempo_breakout}")
        print(f"{'='*70}\n")

if __name__ == "__main__":
    radar = RadarNuclearEstrategico()
    radar.generar_mapa()