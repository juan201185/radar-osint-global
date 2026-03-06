import folium
from folium.plugins import MarkerCluster, AntPath
import requests
import datetime
import json
import random

# Datos de buques fantasma iraníes (simulados basados en reportes reales)
BUQUES_FANTASMA = [
    {"nombre": "Adrian Darya 1", "imo": "9115892", "bandera_falsa": "Panamá", "real": "Irán", "carga": "Petróleo", "ruta": ["Bandar Abbas", "Siria"]},
    {"nombre": "Grace 1", "imo": "9119412", "bandera_falsa": "Panamá", "real": "Irán", "carga": "Petróleo", "ruta": ["Gibraltar", "Siria"]},
    {"nombre": "Bella", "imo": "9208102", "bandera_falsa": "Tanzania", "real": "Irán", "carga": "Condensado", "ruta": ["Emiratos", "Venezuela"]},
    {"nombre": "Bering", "imo": "9208126", "bandera_falsa": "Tanzania", "real": "Irán", "carga": "Petróleo", "ruta": ["Omán", "China"]},
    {"nombre": "Pandi", "imo": "9222650", "bandera_falsa": "Albania", "real": "Irán", "carga": "Petróleo", "ruta": ["Irán", "Siria"]},
]

# Sanciones recientes OFAC
SANCIONES_OFAC = [
    {"fecha": "2024-01-18", "entidad": "Red de petróleo iraní", "tipo": "Sanción económica", "impacto": "Bloqueo $100M"},
    {"fecha": "2024-02-06", "entidad": "Houthi financieros", "tipo": "Congelamiento activos", "impacto": "5 individuos sancionados"},
    {"fecha": "2024-03-01", "entidad": "Bancos de Gaza", "tipo": "Investigación", "impacto": "Flujos a Hamas"},
]

# Precios objetivo
PRECIOS_CRUDO = {
    "Brent": 84.50,
    "WTI": 79.20,
    "Iran_Heavy": 72.30,  # Descuento por sanciones
    "Ural": 76.80,        # Rusia
}

class RadarFinancieroGuerra:
    def __init__(self):
        self.transacciones_detectadas = []
        
    def simular_flujo_petroleo(self):
        """Simula flujo de petróleo iraní a China/Siria/Venezuela"""
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Analizando flujos financieros y evasión de sanciones...")
        
        flujos = [
            {
                "origen": "Bandar Abbas, Irán",
                "destino": "Puerto de Ningbo, China",
                "volumen": "2.1M barriles",
                "valor": "$150M USD",
                "metodo_pago": "Yuanes chinos (bypass SWIFT)",
                "coord_origen": [27.1832, 56.2666],
                "coord_destino": [29.8683, 121.5440],
                "riesgo": "Sanciones EEUU"
            },
            {
                "origen": "Kharg Island, Irán",
                "destino": "Baniyas, Siria",
                "volumen": "1M barriles",
                "valor": "$45M USD (subprecio)",
                "metodo_pago": "Efectivo/oro",
                "coord_origen": [29.2333, 50.3167],
                "coord_destino": [35.1833, 35.9333],
                "riesgo": "Financiamiento Hezbollah"
            },
            {
                "origen": "Jask, Irán",
                "destino": "Puerto Jose, Venezuela",
                "volumen": "800K barriles",
                "valor": "Trueque (alimentos/medicinas)",
                "metodo_pago": "Barter",
                "coord_origen": [25.6333, 57.7667],
                "coord_destino": [10.0667, -64.8333],
                "riesgo": "Evasión de Sanciones"
            }
        ]
        
        print(f"   -> {len(flujos)} vectores de exportación iraní detectados")
        return flujos
    
    def obtener_precios_tiempo_real(self):
        """En producción: Yahoo Finance API o similar"""
        return PRECIOS_CRUDO
    
    def generar_mapa(self):
        print("\n" + "="*70)
        print("INICIANDO RADAR FINANCIERO E.T.B. (PETRÓLEO Y SANCIONES)")
        print("="*70)
        
        mapa = folium.Map(
            location=[30.0, 35.0],
            zoom_start=3,
            tiles='CartoDB dark_matter'
        )
        
        # Capas
        capa_flujos = folium.FeatureGroup(name="🛢️ Flujos de Petróleo Irán/Rusia").add_to(mapa)
        capa_buques = folium.FeatureGroup(name="⚠️ Flota Fantasma (Dark Fleet)").add_to(mapa)
        capa_sanciones = folium.FeatureGroup(name="💰 Nodos Financieros / Sanciones").add_to(mapa)
        
        # 1. Flujos de petróleo (usando AntPath para animación visual)
        flujos = self.simular_flujo_petroleo()
        for flujo in flujos:
            AntPath(
                locations=[flujo['coord_origen'], flujo['coord_destino']],
                color='#ffcc00',  # Dorado petróleo
                weight=3,
                opacity=0.7,
                dash_array=[10, 20],
                delay=1200,
                tooltip=f"Flujo Financiero: {flujo['origen']} → {flujo['destino']}"
            ).add_to(capa_flujos)
            
            popup_html = f"""
            <div style="font-family: 'Courier New', monospace; width: 280px; 
                        background: rgba(0,0,0,0.95); color: #fff; padding: 12px; 
                        border-radius: 8px; border-left: 5px solid #ffcc00;">
                <b style="color:#ffcc00; font-size: 14px;">🛢️ VINCULACIÓN COMERCIAL</b><br>
                <hr style="border-color: #333; margin: 8px 0;">
                <b>Origen:</b> {flujo['origen']}<br>
                <b>Destino:</b> {flujo['destino']}<br>
                <b>Volumen:</b> {flujo['volumen']}<br>
                <b>Valor Estimado:</b> {flujo['valor']}<br>
                <b>Estructura de Pago:</b> {flujo['metodo_pago']}<br>
                <b>Alerta Táctica:</b> <span style='color:#ff4444;'>{flujo['riesgo']}</span>
            </div>
            """
            
            # Marcadores en origen y destino
            folium.Marker(
                flujo['coord_origen'],
                icon=folium.Icon(color='red', icon='oil-can', prefix='fa'),
                popup=folium.Popup(popup_html, max_width=300),
                tooltip="Nodo de Extracción Sancionado"
            ).add_to(capa_flujos)
            
            folium.Marker(
                flujo['coord_destino'],
                icon=folium.Icon(color='orange', icon='industry', prefix='fa'),
                popup=folium.Popup(popup_html, max_width=300),
                tooltip="Refinería/Comprador"
            ).add_to(capa_flujos)
        
        # 2. Buques fantasma (posiciones simuladas)
        for buque in BUQUES_FANTASMA:
            if "Siria" in buque['ruta']: pos = [34.0, 30.0]
            elif "China" in buque['ruta']: pos = [25.0, 60.0]
            else: pos = [20.0, 40.0]
            
            popup_html = f"""
            <div style="font-family: 'Courier New', monospace; width: 260px; 
                        background: rgba(0,0,0,0.95); color: #fff; padding: 12px; 
                        border-radius: 8px; border-left: 5px solid #aaaaaa;">
                <b style="color:#aaaaaa; font-size: 14px;">🚢 DARK FLEET (BUQUE FANTASMA)</b><br>
                <hr style="border-color: #333; margin: 8px 0;">
                <b>Nombre AIS:</b> {buque['nombre']}<br>
                <b>IMO Registrado:</b> {buque['imo']}<br>
                <b>Bandera Falsa:</b> <span style="color:#ff4444;">{buque['bandera_falsa']}</span><br>
                <b>Origen Real:</b> {buque['real']}<br>
                <b>Carga Sancionada:</b> {buque['carga']}<br>
                <b>Vector de Ruta:</b> {' → '.join(buque['ruta'])}
            </div>
            """
            
            folium.Marker(
                [pos[0] + random.uniform(-2, 2), pos[1] + random.uniform(-2, 2)],
                popup=folium.Popup(popup_html, max_width=300),
                icon=folium.Icon(color='black', icon='ship', prefix='fa'),
                tooltip=f"AIS APAGADO: {buque['nombre']}"
            ).add_to(capa_buques)
        
        # 3. Centros financieros clave
        centros = {
            "Dubai (Hawala/Oro)": [25.2048, 55.2708],
            "Estambul (Banca)": [41.0082, 28.9784],
            "Moscú (Sistema SPFS)": [55.7558, 37.6173],
            "Pekín (Sistema CIPS)": [39.9042, 116.4074],
            "Caracas (Estructura Trueque)": [10.4806, -66.9036],
        }
        
        for nombre, coords in centros.items():
            folium.CircleMarker(
                coords,
                radius=12,
                color='purple',
                fill=True,
                fillColor='purple',
                fillOpacity=0.4,
                popup=f"""
                <div style="font-family: 'Courier New', monospace; width: 200px; background: rgba(0,0,0,0.9); color: white; padding: 10px; border-left: 4px solid purple;">
                    <b style="color:#cc66ff;">{nombre}</b><br>
                    Nodo de evasión financiera al sistema SWIFT occidental.
                </div>
                """
            ).add_to(capa_sanciones)
        
        # Panel Informativo Unificado E.T.B.
        precios = self.obtener_precios_tiempo_real()
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        panel_info = f"""
        <div style="position: fixed; top: 20px; right: 20px; width: 300px; 
                    background-color: rgba(10,10,10,0.95); color: #fff; 
                    border: 2px solid #ffcc00; padding: 15px; border-radius: 10px; 
                    font-family: 'Courier New', monospace; font-size: 11px; z-index: 9999;
                    box-shadow: 0 0 20px rgba(255,204,0,0.3);">
            <h4 style="color:#ffcc00; margin-top:0; text-align:center; font-size: 14px; 
                       border-bottom: 2px solid #333; padding-bottom: 8px;">
                💰 RADAR FINANCIERO E.T.B.
            </h4>
            <div style="background: rgba(255,204,0,0.1); padding: 8px; border-radius: 5px; 
                        margin-bottom: 10px; text-align: center; border: 1px solid #ffcc00;">
                <b style="color:#ffcc00; letter-spacing: 1px;">PRECIOS GLOBALES DEL CRUDO</b>
            </div>
            <div style="line-height: 1.6;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span>🇺🇸 Brent (Referencia):</span>
                    <span style="color:#00ff41; font-weight:bold;">${precios['Brent']}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span>🇺🇸 WTI (Texas):</span>
                    <span style="color:#00ff41;">${precios['WTI']}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span>🇮🇷 Iran Heavy (Gris):</span>
                    <span style="color:#ff4444; font-weight:bold;">${precios['Iran_Heavy']}</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span>🇷🇺 Ural Ruso (Gris):</span>
                    <span style="color:#ffaa00;">${precios['Ural']}</span>
                </div>
            </div>
            <div style="margin-top: 12px; border-top: 2px solid #333; padding-top: 10px;">
                <b style="color:#cc66ff;">EVASIÓN DE SANCIONES:</b><br>
                Flujos Detectados: <span style="color:#ffcc00;">{len(flujos)} Rutas Activas</span><br>
                Dark Fleet Identificada: <span style="color:#ff4444;">{len(BUQUES_FANTASMA)} Buques</span><br>
                Fuga Financiera Estimada: ~$50M USD/día
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
        
        nombre_mapa = "radar_financiero_guerra.html"
        mapa.save(nombre_mapa)
        
        print(f"\n{'='*70}")
        print(f"[✅ MAPA FINANCIERO GENERADO]")
        print(f"Archivo: {nombre_mapa}")
        print(f"Capas: Rutas Petroleras, Dark Fleet y Nodos de Evasión")
        print(f"{'='*70}\n")

if __name__ == "__main__":
    radar = RadarFinancieroGuerra()
    radar.generar_mapa()