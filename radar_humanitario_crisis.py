import folium
from folium.plugins import MarkerCluster, HeatMap
import datetime
import json

# Instalaciones médicas dañadas (datos WHO/UN)
HOSPITALES_DANADOS = [
    {"nombre": "Hospital Al-Shifa", "coords": [31.5017, 34.4668], "estado": "Destruido", "fecha": "2023-11-15", "tipo": "Hospital principal"},
    {"nombre": "Hospital Al-Quds", "coords": [31.5120, 34.4800], "estado": "Fuera de servicio", "fecha": "2023-10-29", "tipo": "Hospital"},
    {"nombre": "Hospital Indonesia", "coords": [31.5200, 34.4900], "estado": "Dañado", "fecha": "2023-11-21", "tipo": "Hospital"},
    {"nombre": "Hospital Al-Ahli", "coords": [31.5117, 34.4608], "estado": "Parcialmente operativo", "fecha": "2023-10-17", "tipo": "Hospital"},
    {"nombre": "Hospital Kamal Adwan", "coords": [31.5500, 34.5200], "estado": "Destruido", "fecha": "2023-12-12", "tipo": "Hospital pediátrico"},
    {"nombre": "Hospital Al-Awda", "coords": [31.5300, 34.5000], "estado": "Fuera de servicio", "fecha": "2023-11-10", "tipo": "Hospital"},
]

# Campos de refugiados/desplazados
CAMPOS_REFUGIADOS = [
    {"nombre": "Campo Rafah", "coords": [31.2968, 34.2435], "poblacion": "1.4M", "condicion": "Sobrepoblado crítico"},
    {"nombre": "Campo Jabalia", "coords": [31.5286, 34.4836], "poblacion": "Desconocido", "condicion": "Sitio de combates"},
    {"nombre": "Campo Khan Younis", "coords": [31.3461, 34.3061], "poblacion": "800K", "condicion": "Inseguridad alimentaria severa"},
    {"nombre": "Zona Deir al-Balah", "coords": [31.4167, 34.3500], "poblacion": "600K", "condicion": "Sin servicios básicos"},
]

# Corredores humanitarios (estado)
CORREDORES = [
    {"nombre": "Rafah Crossing", "coords": [31.2968, 34.2435], "estado": "Cerrado/Intermitente", "tipo": "Salida Gaza"},
    {"nombre": "Kerem Shalom", "coords": [31.2333, 34.2833], "estado": "Operativo limitado", "tipo": "Entrada ayuda"},
    {"nombre": "Erez Crossing", "coords": [31.5667, 34.5500], "estado": "Cerrado", "tipo": "Personal"},
    {"nombre": "Karni Crossing", "coords": [31.4833, 34.4667], "estado": "Destruido", "tipo": "Carga"},
]

# Escuelas UNRWA afectadas
ESCUELAS_UNRWA = [
    {"nombre": "Escuela Al-Fakhura", "coords": [31.5286, 34.4836], "uso": "Refugio desplazados", "estado": "Atacada"},
    {"nombre": "Escuela Jabalia", "coords": [31.5300, 34.4850], "uso": "Refugio", "estado": "Dañada"},
]

class RadarHumanitarioCrisis:
    def __init__(self):
        self.nivel_crisis = "CATASTRÓFICO"
        
    def obtener_metricas_crisis(self):
        """Datos de UN OCHA"""
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Procesando telemetría de crisis humanitaria (UN OCHA)...")
        
        metricas = {
            "desplazados_gaza": "1.9M (85% población)",
            "heridos": "75,000+",
            "muertos_reportados": "30,000+",
            "hambre_aguda": "100% Gaza",
            "acceso_agua": "5% de capacidad normal",
            "electricidad": "0-4 horas/día",
            "hospitales_operativos": "3 de 36",
        }
        
        return metricas
    
    def generar_mapa(self):
        print("\n" + "="*70)
        print("INICIANDO RADAR HUMANITARIO E.T.B. (DAÑO COLATERAL)")
        print("="*70)
        
        mapa = folium.Map(
            location=[31.4, 34.4],
            zoom_start=11,
            tiles='CartoDB dark_matter'
        )
        
        # Capas
        capa_densidad = folium.FeatureGroup(name="👥 Densidad Desplazados (Heatmap)").add_to(mapa)
        capa_hospitales = folium.FeatureGroup(name="🏥 Infraestructura Médica (OMS)").add_to(mapa)
        capa_escuelas = folium.FeatureGroup(name="🏫 Instalaciones UNRWA").add_to(mapa)
        capa_campamentos = folium.FeatureGroup(name="⛺ Campos de Refugiados").add_to(mapa)
        capa_corredores = folium.FeatureGroup(name="🚪 Rutas de Evacuación/Ayuda").add_to(mapa)
        
        # 1. Campos de refugiados y Heatmap
        puntos_calor = []
        for campo in CAMPOS_REFUGIADOS:
            popup_html = f"""
            <div style="font-family: 'Courier New', monospace; width: 250px; 
                        background: rgba(0,0,0,0.95); color: #fff; padding: 12px; 
                        border-radius: 8px; border-left: 5px solid #0066ff;">
                <b style="color:#00aaff; font-size: 14px;">⛺ {campo['nombre'].upper()}</b><br>
                <hr style="border-color: #333; margin: 8px 0;">
                <b>Población Estimada:</b> {campo['poblacion']}<br>
                <b>Condición Actual:</b> <span style="color:#ffcc00;">{campo['condicion']}</span>
            </div>
            """
            
            folium.Marker(
                campo['coords'],
                popup=folium.Popup(popup_html, max_width=280),
                icon=folium.Icon(color='blue', icon='users', prefix='fa'),
                tooltip=f"Campo Desplazados: {campo['nombre']}"
            ).add_to(capa_campamentos)
            
            # Círculo visual para el campo
            folium.Circle(
                campo['coords'],
                radius=2500,
                color='blue',
                fill=True,
                fillColor='blue',
                fillOpacity=0.2,
                weight=1
            ).add_to(capa_campamentos)
            
            # Agregamos al heatmap
            puntos_calor.append([campo['coords'][0], campo['coords'][1], 1.0])
        
        # Añadir Heatmap
        HeatMap(puntos_calor, radius=35, blur=25, min_opacity=0.3).add_to(capa_densidad)
        
        # 2. Hospitales
        for hosp in HOSPITALES_DANADOS:
            color = {"Destruido": "black", "Fuera de servicio": "red", 
                     "Dañado": "orange", "Parcialmente operativo": "beige"}.get(hosp['estado'], 'gray')
            
            popup_html = f"""
            <div style="font-family: 'Courier New', monospace; width: 260px; 
                        background: rgba(0,0,0,0.95); color: #fff; padding: 12px; 
                        border-radius: 8px; border-left: 5px solid {color};">
                <b style="color:{color if color != 'black' else '#888'}; font-size: 14px;">🏥 {hosp['nombre'].upper()}</b><br>
                <hr style="border-color: #333; margin: 8px 0;">
                <b>Perfil:</b> {hosp['tipo']}<br>
                <b>Estado Operativo:</b> <span style="color:{color if color != 'black' else '#888'}; font-weight:bold;">{hosp['estado'].upper()}</span><br>
                <b>Fecha Impacto/Colapso:</b> {hosp['fecha']}
            </div>
            """
            
            folium.Marker(
                hosp['coords'],
                popup=folium.Popup(popup_html, max_width=280),
                icon=folium.Icon(color=color if color != 'black' else 'lightgray', icon='h-square', prefix='fa'),
                tooltip=f"Instalación Médica: {hosp['nombre']}"
            ).add_to(capa_hospitales)
        
        # 3. Corredores
        for corredor in CORREDORES:
            color = {"Cerrado": "red", "Cerrado/Intermitente": "orange", 
                     "Operativo limitado": "green", "Destruido": "black"}.get(corredor['estado'], 'gray')
            
            popup_html = f"""
            <div style="font-family: 'Courier New', monospace; width: 220px; background: rgba(0,0,0,0.9); color: white; padding: 10px; border-left: 4px solid {color if color != 'black' else '#888'};">
                <b style="color:{color if color != 'black' else '#888'};">🚪 {corredor['nombre'].upper()}</b><br>
                <b>Propósito:</b> {corredor['tipo']}<br>
                <b>Estado:</b> {corredor['estado']}
            </div>
            """
            
            folium.Marker(
                corredor['coords'],
                popup=folium.Popup(popup_html, max_width=250),
                icon=folium.Icon(color=color if color != 'black' else 'lightgray', icon='exchange', prefix='fa')
            ).add_to(capa_corredores)
        
        # 4. Escuelas UNRWA
        for escuela in ESCUELAS_UNRWA:
            folium.Marker(
                escuela['coords'],
                popup=f"<div style='font-family: Courier New; background:#222; color:#fff; padding:5px;'><b>{escuela['nombre']}</b><br>Uso: {escuela['uso']}<br>Estado: <span style='color:red;'>{escuela['estado']}</span></div>",
                icon=folium.Icon(color='lightblue', icon='graduation-cap', prefix='fa'),
                tooltip="Instalación UNRWA"
            ).add_to(capa_escuelas)
        
        # Métricas
        metricas = self.obtener_metricas_crisis()
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Panel Informativo Unificado E.T.B.
        panel = f"""
        <div style="position: fixed; top: 20px; right: 20px; width: 320px; 
                    background-color: rgba(10,10,10,0.95); color: #fff; 
                    border: 2px solid #ff0000; padding: 15px; border-radius: 10px; 
                    font-family: 'Courier New', monospace; font-size: 11px; z-index: 9999;
                    box-shadow: 0 0 20px rgba(255,0,0,0.5);">
            <h4 style="color:#ff0000; margin-top:0; text-align:center; font-size: 14px;
                       border-bottom: 2px solid #333; padding-bottom: 8px;">
                ⛑️ IMPACTO HUMANITARIO E.T.B.
            </h4>
            <div style="background: rgba(255,0,0,0.2); padding: 8px; border-radius: 5px; 
                        margin-bottom: 10px; text-align: center; border: 1px solid #ff0000;">
                <b style="color:#ff6666; letter-spacing: 1px;">NIVEL DE CRISIS: {self.nivel_crisis}</b>
            </div>
            <div style="line-height: 1.6;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span>Desplazados Internos:</span>
                    <span style="color:#ff6666; font-weight:bold;">{metricas['desplazados_gaza']}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span>Hospitales Operativos:</span>
                    <span style="color:#ff0000;">{metricas['hospitales_operativos']}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span>Hambre Aguda:</span>
                    <span style="color:#ff0000;">{metricas['hambre_aguda']}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span>Acceso Agua Potable:</span>
                    <span style="color:#ff6666;">{metricas['acceso_agua']}</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span>Suministro Eléctrico:</span>
                    <span style="color:#ffaa00;">{metricas['electricidad']}</span>
                </div>
            </div>
            <div style="margin-top: 12px; border-top: 2px solid #333; padding-top: 10px;">
                <b style="color:#ff6666;">INFRAESTRUCTURA DAÑADA:</b><br>
                Hospitales Colapsados/Destruidos: {len([h for h in HOSPITALES_DANADOS if h['estado'] in ['Destruido', 'Fuera de servicio']])}<br>
                Campos Desbordados: {len(CAMPOS_REFUGIADOS)}<br>
                Corredores Bloqueados: {len([c for c in CORREDORES if 'Cerrado' in c['estado'] or 'Destruido' in c['estado']])}
            </div>
            <div style="margin-top: 12px; border-top: 2px solid #333; padding-top: 10px; 
                        font-size: 10px; color: #666; text-align: center;">
                <b>Fuente de Datos:</b> UN OCHA / WHO<br>
                Actualizado: {timestamp}<br>
                <span style="color: #444;">Sistema E.T.B. v2.0</span>
            </div>
        </div>
        """
        mapa.get_root().html.add_child(folium.Element(panel))
        
        folium.LayerControl(collapsed=False).add_to(mapa)
        
        nombre_mapa = "radar_humanitario_crisis.html"
        mapa.save(nombre_mapa)
        
        print(f"\n{'='*70}")
        print(f"[✅ MAPA HUMANITARIO GENERADO]")
        print(f"Archivo: {nombre_mapa}")
        print(f"Hospitales afectados: {len(HOSPITALES_DANADOS)} | Nivel: {self.nivel_crisis}")
        print(f"{'='*70}\n")

if __name__ == "__main__":
    radar = RadarHumanitarioCrisis()
    radar.generar_mapa()