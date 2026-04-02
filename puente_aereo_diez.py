import requests
import folium
from folium.plugins import MarkerCluster, PolyLineTextPath, AntPath
import datetime
import json
import time
from collections import defaultdict
import random

# --- BASES LOGÍSTICAS ESTRATÉGICAS (Nodos del Puente Aéreo) ---
BASES_LOGISTICAS = {
    # Estados Unidos - Origen
    "DOV": {"nombre": "Dover AFB", "coords": [39.1295, -75.4659], "tipo": "origen", "pais": "EEUU"},
    "CHS": {"nombre": "Charleston AFB", "coords": [32.8986, -80.0405], "tipo": "origen", "pais": "EEUU"},
    "TYS": {"nombre": "McGhee Tyson ANGB", "coords": [35.8110, -83.9940], "tipo": "origen", "pais": "EEUU"},
    "BWI": {"nombre": "Baltimore (Martin)", "coords": [39.1754, -76.6683], "tipo": "origen", "pais": "EEUU"},
    
    # Europa - Escalas y Forward Operating Bases
    "RMS": {"nombre": "Ramstein AB", "coords": [49.4369, 7.6003], "tipo": "escala_europa", "pais": "Alemania"},
    "SPM": {"nombre": "Spangdahlem AB", "coords": [49.9727, 6.6925], "tipo": "escala_europa", "pais": "Alemania"},
    "AVB": {"nombre": "Aviano AB", "coords": [46.0319, 12.5965], "tipo": "escala_europa", "pais": "Italia"},
    "Souda": {"nombre": "Souda Bay", "coords": [35.5317, 24.1490], "tipo": "escala_europa", "pais": "Grecia"},
    "LUX": {"nombre": "Luxembourg (NATO)", "coords": [49.6233, 6.2044], "tipo": "escala_europa", "pais": "Luxemburgo"},
    
    # África y Medio Oriente - Forward Arming and Refueling Points
    "DNA": {"nombre": "Al Udeid AB", "coords": [25.1171, 51.3150], "tipo": "farp", "pais": "Qatar"},
    "AUH": {"nombre": "Al Dhafra AB", "coords": [24.2483, 54.5477], "tipo": "farp", "pais": "EAU"},
    "MSH": {"nombre": "Masirah AB", "coords": [20.6754, 58.8905], "tipo": "farp", "pais": "Omán"},
    "DJI": {"nombre": "Camp Lemonnier", "coords": [11.5473, 43.1594], "tipo": "farp", "pais": "Yibuti"},
    
    # Israel - Destino final
    "TLV": {"nombre": "Tel Aviv (Ben Gurion)", "coords": [32.0000, 34.8700], "tipo": "destino", "pais": "Israel"},
    "LLBG": {"nombre": "Tel Aviv (Civil/Mil)", "coords": [32.0117, 34.8861], "tipo": "destino", "pais": "Israel"},
    "Ovda": {"nombre": "Ovda AB", "coords": [29.9403, 34.9358], "tipo": "destino", "pais": "Israel"},
    "Nevatim": {"nombre": "Nevatim AB", "coords": [31.2083, 35.0125], "tipo": "destino", "pais": "Israel"},
    
    # UK - Soporte NATO
    "MHZ": {"nombre": "Mildenhall RAF", "coords": [52.3619, 0.4864], "tipo": "escala_europa", "pais": "UK"},
    "FFD": {"nombre": "Fairford RAF", "coords": [51.6822, -1.7900], "tipo": "escala_europa", "pais": "UK"},
    
    # Asia - Ruta del Pacífico (alternativa)
    "DNA_P": {"nombre": "Diego García", "coords": [-7.3133, 72.4111], "tipo": "farp", "pais": "UK/Indico"},
}

# Callsigns ampliados por tipo de misión
CALLSIGNS_POR_MISION = {
    "carga_pesada": {
        "prefijos": ("RCH", "REACH", "CMB", "CFC", "HERKY", "YANK"),
        "descripcion": "C-5 Galaxy, C-17 Globemaster - Armas pesadas, vehículos, helicópteros",
        "color": "darkgreen",
        "icono": "truck",
        "peso": 5
    },
    "carga_tactica": {
        "prefijos": ("CNV", "NVY", "CONVOY"),
        "descripcion": "C-130 Hercules, C-27J - Munición, suministros tácticos, tropas",
        "color": "green",
        "icono": "fighter-jet",
        "peso": 3
    },
    "repostaje": {
        "prefijos": ("QID", "QUID", "NITRO", "TEXACO", "SHELL"),
        "descripcion": "KC-135, KC-10, KC-46 - Combustible para operaciones aéreas",
        "color": "orange",
        "icono": "tint",
        "peso": 4
    },
    "inteligencia": {
        "prefijos": ("SAM", "SPAR", "COBRA", "DRAGN", "SNOOP"),
        "descripcion": "RC-135, E-8 JSTARS, AWACS - ISR y comando",
        "color": "purple",
        "icono": "eye",
        "peso": 2
    },
    "contratistas_armas": {
        "prefijos": ("GTI", "CKS", "NCR", "OAE", "SOO", "ABX"),
        "descripcion": "Kalitta, Southern Air, National - Munición clasificada (programa CRAF)",
        "color": "red",
        "icono": "warning",
        "peso": 5
    },
    "contratistas_logistica": {
        "prefijos": ("ATN", "PAC", "FDX", "UPS"),
        "descripcion": "FedEx, UPS Military - Repuestos, equipo no letal, contratos DOD",
        "color": "blue",
        "icono": "plane",
        "peso": 2
    },
    "israel_directo": {
        "prefijos": ("ELY", "CAL", "IAF", "ZAK"),
        "descripcion": "El Al Cargo, CAL Cargo, Fuerza Aérea Israelí - Suministro directo",
        "color": "darkblue",
        "icono": "star",
        "peso": 5
    },
    "otan_multinacional": {
        "prefijos": ("NATO", "MMF", "RRR", "BAF", "GAF", "LUF"),
        "descripcion": "AWACS NATO, repostaje multinacional, misiones OTAN",
        "color": "cadetblue",
        "icono": "globe",
        "peso": 3
    }
}

# Aeropuertos de origen sospechosos (indicadores de carga bélica)
AEROPUERTOS_ARMAS = {
    "KDOV": "Dover AFB - Principal hub de carga militar EEUU",
    "KCHS": "Charleston AFB - C-17 base",
    "KTYS": "McGhee Tyson - ANGB operaciones especiales",
    "KBWI": "Baltimore - Carga naval/Marines",
    "KGSB": "Seymour Johnson - F-15E base",
    "KPOB": "Pope AFB - Fuerzas especiales/Airborne",
    "KBLD": "Boulder City - Contratistas área 51/test",
}

class AnalizadorPuenteAereo:
    def __init__(self):
        self.vuelos_detectados = []
        self.patrones_ruta = defaultdict(list)
        self.alertas_activas = []
        
    def clasificar_vuelo(self, callsign, origen, destino, altitud, velocidad):
        callsign_upper = callsign.upper()
        
        # Prioridad 1: Callsign conocido
        for tipo, datos in CALLSIGNS_POR_MISION.items():
            if callsign_upper.startswith(datos["prefijos"]):
                es_ruta_estrategica = self.es_ruta_estrategica(origen, destino)
                confianza = "ALTA" if es_ruta_estrategica else "MEDIA"
                return tipo, confianza, datos
        
        # Prioridad 2: Origen en bases de armas
        if origen in AEROPUERTOS_ARMAS:
            return "carga_probable", "MEDIA", {
                "descripcion": f"Origen militar sospechoso: {AEROPUERTOS_ARMAS.get(origen, 'Desconocido')}",
                "color": "orange",
                "icono": "question",
                "peso": 3
            }
        
        # Prioridad 3: Altitud y velocidad indicativa de carga pesada
        if altitud and altitud > 8000 and altitud < 11000:
            if velocidad and velocidad < 250:
                return "carga_posible", "BAJA", {
                    "descripcion": "Perfil de vuelo compatible con transporte pesado",
                    "color": "lightgray",
                    "icono": "plane",
                    "peso": 1
                }
        
        return None, None, None
    
    def es_ruta_estrategica(self, origen, destino):
        bases_clave = set(BASES_LOGISTICAS.keys())
        if origen in bases_clave or destino in bases_clave:
            return True
        if origen and destino:
            if origen.startswith("K") and destino in bases_clave:
                return True
        return False
    
    def detectar_patron_sospechoso(self, vuelo_actual):
        alertas = []
        
        # Patrón 1: Múltiples C-17/C-5 saliendo de Dover/Charleston hacia Ramstein
        if vuelo_actual["tipo"] in ["carga_pesada", "carga_tactica"]:
            if vuelo_actual.get("origen") in ["KDOV", "KCHS"]:
                if vuelo_actual.get("destino") in ["RMS", "SPM", "AVB"]:
                    alertas.append({
                        "nivel": "CRITICO",
                        "mensaje": f"🔴 PUENTE AÉREO ACTIVO: {vuelo_actual['callsign']} saliendo de {vuelo_actual['origen']} hacia Europa",
                        "hora": datetime.datetime.now().strftime("%H:%M:%S")
                    })
        
        # Patrón 2: Contratistas CRAF rumbo a Medio Oriente
        if vuelo_actual["tipo"] == "contratistas_armas":
            if vuelo_actual.get("destino") in ["DNA", "AUH", "TLV", "LLBG"]:
                alertas.append({
                    "nivel": "ALTO",
                    "mensaje": f"🟠 CARGA CLASIFICADA: {vuelo_actual['callsign']} contratista rumbo a zona de conflicto",
                    "hora": datetime.datetime.now().strftime("%H:%M:%S")
                })
        
        # Patrón 3: El Al/IAF en ruta transatlántica
        if vuelo_actual["tipo"] == "israel_directo":
            if vuelo_actual.get("altitud", 0) > 5000:
                alertas.append({
                    "nivel": "MEDIO",
                    "mensaje": f"🔵 SUMINISTRO ISRAELÍ: {vuelo_actual['callsign']} en ruta internacional",
                    "hora": datetime.datetime.now().strftime("%H:%M:%S")
                })
        
        return alertas

def obtener_datos_opensky():
    url = "https://opensky-network.org/api/states/all"
    try:
        response = requests.get(url, timeout=25)
        if response.status_code == 200:
            return response.json().get('states', [])
        else:
            print(f"   [!] OpenSky Error HTTP {response.status_code}")
            return []
    except requests.exceptions.Timeout:
        print("   [!] Timeout OpenSky - Servidor sobrecargado")
        return []
    except Exception as e:
        print(f"   [!] Error conexión OpenSky: {str(e)[:50]}")
        return []

def generar_mapa_puente_aereo():
    print(f"\n[{datetime.datetime.now().strftime('%H:%M:%S')}] INICIANDO ANÁLISIS DE PUENTE AÉREO ESTRATÉGICO")
    print("=" * 70)
    print("Fuentes: OpenSky Network | Análisis de patrones | Bases logísticas")
    print("=" * 70)
    
    analizador = AnalizadorPuenteAereo()
    
    mapa = folium.Map(
        location=[45.0, -30.0],
        zoom_start=4,
        tiles='CartoDB dark_matter'
    )
    
    capa_bases = folium.FeatureGroup(name="🏭 Bases Logísticas Estratégicas").add_to(mapa)
    capa_carga_pesada = folium.FeatureGroup(name="🟢 Carga Pesada (C-5/C-17)").add_to(mapa)
    capa_carga_tac = folium.FeatureGroup(name="🟩 Carga Táctica (C-130)").add_to(mapa)
    capa_repuesto = folium.FeatureGroup(name="🟠 Repostaje Aéreo (KC-135)").add_to(mapa)
    capa_craf = folium.FeatureGroup(name="🔴 CRAF/Contratistas Armas").add_to(mapa)
    capa_logistica = folium.FeatureGroup(name="🔵 Logística Comercial (FedEx/UPS)").add_to(mapa)
    capa_israel = folium.FeatureGroup(name="⭐ Línea de Vida Israel (El Al/IAF)").add_to(mapa)
    capa_intel = folium.FeatureGroup(name="🟣 Inteligencia/Comando").add_to(mapa)
    capa_otan = folium.FeatureGroup(name="🔵 OTAN Multinacional").add_to(mapa)
    capa_sospechosos = folium.FeatureGroup(name="⚠️ Patrones Sospechosos").add_to(mapa)
    
    for codigo, base in BASES_LOGISTICAS.items():
        color_base = {
            "origen": "green",
            "escala_europa": "blue",
            "farp": "orange",
            "destino": "red"
        }.get(base["tipo"], "gray")
        
        folium.Marker(
            location=base["coords"],
            popup=f"""
            <div style="font-family: 'Courier New', monospace; width: 220px; background: rgba(0,0,0,0.8); color: white; padding: 10px; border-radius: 5px;">
                <b style="font-size: 14px; color: {color_base};">{base['nombre']}</b><br>
                <hr style="border-color: #333; margin: 8px 0;">
                <b>Código:</b> {codigo}<br>
                <b>Tipo:</b> {base['tipo'].replace('_', ' ').title()}<br>
                <b>País:</b> {base['pais']}
            </div>
            """,
            icon=folium.Icon(color=color_base, icon='flag', prefix='fa'),
            tooltip=f"{base['nombre']} ({base['pais']})"
        ).add_to(capa_bases)
        
        folium.Circle(
            location=base["coords"],
            radius=50000,
            color=color_base,
            fill=True,
            fillOpacity=0.1,
            weight=1
        ).add_to(capa_bases)
    
    vuelos = obtener_datos_opensky()
    
    if not vuelos:
        print("   [!] No se obtuvieron datos de vuelo - Generando mapa con bases solamente")
    
    stats = defaultdict(int)
    alertas_globales = []
    
    print(f"   -> Procesando {len(vuelos)} contactos radar...")
    
    for vuelo in vuelos:
        try:
            callsign = vuelo[1].strip().upper() if vuelo[1] else "DESCONOCIDO"
            origen = vuelo[2] if vuelo[2] else None
            lon = vuelo[5]
            lat = vuelo[6]
            altitud = vuelo[7]
            velocidad = vuelo[9]
            rumbo = vuelo[10]
            
            if not lat or not lon:
                continue
            
            tipo_mision, confianza, datos_mision = analizador.clasificar_vuelo(
                callsign, origen, None, altitud, velocidad
            )
            
            if not tipo_mision:
                continue
            
            vuelo_obj = {
                "callsign": callsign,
                "tipo": tipo_mision,
                "origen": origen,
                "lat": lat,
                "lon": lon,
                "altitud": altitud,
                "velocidad": velocidad,
                "rumbo": rumbo,
                "confianza": confianza
            }
            
            alertas = analizador.detectar_patron_sospechoso(vuelo_obj)
            alertas_globales.extend(alertas)
            
            capa_destino = None
            if tipo_mision == "carga_pesada": capa_destino = capa_carga_pesada
            elif tipo_mision == "carga_tactica": capa_destino = capa_carga_tac
            elif tipo_mision == "repostaje": capa_destino = capa_repuesto
            elif tipo_mision == "contratistas_armas": capa_destino = capa_craf
            elif tipo_mision == "contratistas_logistica": capa_destino = capa_logistica
            elif tipo_mision == "israel_directo": capa_destino = capa_israel
            elif tipo_mision == "inteligencia": capa_destino = capa_intel
            elif tipo_mision == "otan_multinacional": capa_destino = capa_otan
            else: capa_destino = capa_sospechosos
            
            vel_nudos = round(velocidad * 1.94384, 0) if velocidad else "N/A"
            alt_pies = round(altitud * 3.28084, 0) if altitud else "N/A"
            
            popup_html = f"""
            <div style="font-family: 'Courier New', monospace; width: 280px; 
                        background: rgba(0,0,0,0.95); color: #fff; padding: 12px; 
                        border-radius: 8px; border-left: 5px solid {datos_mision['color']};">
                <b style="color:{datos_mision['color']}; font-size: 16px;">
                    {callsign}
                </b><br>
                <hr style="border-color: #333; margin: 8px 0;">
                <b>Tipo:</b> {tipo_mision.replace('_', ' ').title()}<br>
                <b>Descripción:</b> {datos_mision['descripcion']}<br>
                <b>Confianza:</b> {confianza}<br>
                <b>Origen:</b> {origen if origen else 'Desconocido'}<br>
                <b>Altitud:</b> {alt_pies} ft / {altitud} m<br>
                <b>Velocidad:</b> {vel_nudos} kts<br>
                <b>Rumbo:</b> {rumbo}°<br>
                <b>Coordenadas:</b> {round(lat, 4)}, {round(lon, 4)}
            </div>
            """
            
            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup(popup_html, max_width=300),
                icon=folium.Icon(
                    color=datos_mision['color'],
                    icon=datos_mision['icono'],
                    prefix='fa'
                ),
                tooltip=f"{callsign} | {tipo_mision.replace('_', ' ').title()}"
            ).add_to(capa_destino)
            
            if any(a["nivel"] == "CRITICO" for a in alertas):
                folium.CircleMarker(
                    location=[lat, lon],
                    radius=15,
                    color='red',
                    fill=True,
                    fillOpacity=0.3,
                    popup=f"ALERTA: {callsign}"
                ).add_to(capa_sospechosos)
            
            stats[tipo_mision] += 1
            
        except Exception as e:
            continue
    
    print(f"\n   -> ANÁLISIS COMPLETADO:")
    print(f"      Carga Pesada (C-5/C-17): {stats.get('carga_pesada', 0)}")
    print(f"      Carga Táctica (C-130): {stats.get('carga_tactica', 0)}")
    print(f"      Repostaje Aéreo: {stats.get('repostaje', 0)}")
    print(f"      CRAF/Contratistas Armas: {stats.get('contratistas_armas', 0)}")
    print(f"      Logística Comercial: {stats.get('contratistas_logistica', 0)}")
    print(f"      Línea Israel: {stats.get('israel_directo', 0)}")
    print(f"      Inteligencia: {stats.get('inteligencia', 0)}")
    print(f"      OTAN: {stats.get('otan_multinacional', 0)}")
    
    if alertas_globales:
        print(f"\n   🚨 ALERTAS DETECTADAS ({len(alertas_globales)}):")
        for alerta in alertas_globales[:5]:
            icono = "🔴" if alerta["nivel"] == "CRITICO" else "🟠" if alerta["nivel"] == "ALTO" else "🔵"
            print(f"      {icono} [{alerta['hora']}] {alerta['mensaje']}")
    
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    panel_info = f"""
    <div style="position: fixed; top: 20px; right: 20px; width: 320px; 
                background-color: rgba(10,10,10,0.95); color: #fff; 
                border: 2px solid #444; padding: 15px; border-radius: 10px; 
                font-family: 'Courier New', monospace; font-size: 11px; z-index: 9999;
                box-shadow: 0 0 20px rgba(0,0,0,0.8); max-height: 500px; overflow-y: auto;">
        <h4 style="color:#00ff41; margin-top:0; text-align:center; font-size: 14px; 
                   border-bottom: 2px solid #333; padding-bottom: 8px;">
            ✈️ PUENTE AÉREO E.T.B.
        </h4>
        <div style="line-height: 1.6; margin-top: 10px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                <span>🟢 Carga Pesada:</span>
                <span style="color:#00ff41; font-weight:bold;">{stats.get('carga_pesada', 0)}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                <span>🟩 Carga Táctica:</span>
                <span style="color:#00ff41;">{stats.get('carga_tactica', 0)}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                <span>🟠 Repostaje:</span>
                <span style="color:#ffa500;">{stats.get('repostaje', 0)}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                <span>🔴 CRAF Armas:</span>
                <span style="color:#ff4444; font-weight:bold;">{stats.get('contratistas_armas', 0)}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                <span>🔵 Logística:</span>
                <span style="color:#4488ff;">{stats.get('contratistas_logistica', 0)}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                <span>⭐ Israel:</span>
                <span style="color:#4488ff; font-weight:bold;">{stats.get('israel_directo', 0)}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                <span>🟣 Inteligencia:</span>
                <span style="color:#aa44aa;">{stats.get('inteligencia', 0)}</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span>🔵 OTAN:</span>
                <span style="color:#44aaaa;">{stats.get('otan_multinacional', 0)}</span>
            </div>
        </div>
        <div style="margin-top: 12px; border-top: 2px solid #333; padding-top: 10px; 
                    font-size: 10px; color: #666;">
            <b>Total contactos:</b> {sum(stats.values())}<br>
            <b>Actualizado:</b> {timestamp}<br>
            <span style="color: #444;">Sistema E.T.B. v2.0</span>
        </div>
    </div>
    """
    mapa.get_root().html.add_child(folium.Element(panel_info))
    
    folium.LayerControl(collapsed=False).add_to(mapa)
    
    nombre_mapa = "radar_logistico_atlantico.html"
    mapa.save(nombre_mapa)
    
    print(f"\n{'='*70}")
    print(f"[✅ MAPA DE PUENTE AÉREO GENERADO]")
    print(f"Archivo: {nombre_mapa}")
    print(f"Capas: 10 categorías tácticas + Bases estratégicas")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    generar_mapa_puente_aereo()