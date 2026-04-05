import folium
import requests
import datetime
import math
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
import warnings

warnings.filterwarnings('ignore')

# --- LA GEOGRAFÍA DE LAS SOMBRAS: TODAS LAS CENTRALES Y CIUDADELAS ---
INSTALACIONES_NUCLEAR_ME = {
    "Natanz (SUB)": {"coords": [33.7233, 51.7267], "pais": "Irán", "sub": 1, "desc": "Enriquecimiento Subterráneo"},
    "Fordow (SUB)": {"coords": [34.8858, 50.9958], "pais": "Irán", "sub": 1, "desc": "Centrifugadoras de Montaña (80m)"},
    "Parchin (SUB)": {"coords": [35.5156, 51.8311], "pais": "Irán", "sub": 1, "desc": "Complejo Militar / Pruebas"},
    "Mes-e Sarcheshmeh": {"coords": [29.9692, 55.8719], "pais": "Irán", "sub": 1, "desc": "Mina / Túneles Logísticos"},
    "Isfahan": {"coords": [32.6804, 51.6861], "pais": "Irán", "sub": 0, "desc": "Conversión de Uranio"},
    "Bushehr": {"coords": [28.8283, 50.8839], "pais": "Irán", "sub": 0, "desc": "Reactor de Potencia Civil"},
    "Arak": {"coords": [34.3747, 49.4736], "pais": "Irán", "sub": 0, "desc": "Reactor de Agua Pesada"},
    "Dimona (NNRC)": {"coords": [31.0011, 35.1469], "pais": "Israel", "sub": 0, "desc": "Centro de Investigación Nuclear (Armas)"},
    "Soreq": {"coords": [31.9054, 34.7820], "pais": "Israel", "sub": 0, "desc": "Centro Nuclear de Soreq"},
    "Akkuyu NPP": {"coords": [36.1436, 33.5411], "pais": "Turquía", "sub": 0, "desc": "Central Nuclear (Rusa)"},
    "Barakah NPP": {"coords": [23.9781, 52.2353], "pais": "EAU", "sub": 0, "desc": "Central Nuclear Civil"}
}

def calcular_distancia(lat1, lon1, lat2, lon2):
    R = 6371.0 
    dlat, dlon = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))

class CerebroNeuronalETB:
    def __init__(self):
        self.modelo = MLPClassifier(hidden_layer_sizes=(32, 16), activation='relu', max_iter=3000, random_state=42)
        self.scaler = StandardScaler()
        self.entrenar_ia()

    def entrenar_ia(self):
        # [Magnitud, Profundidad_km, Distancia_Nodo, Rad_uSv, Es_Subterraneo(1/0)]
        X_train = np.array([
            [4.5, 15.0, 10.0, 0.15, 1], [5.1, 20.0, 5.0, 0.12, 0], [6.0, 30.0, 100.0, 0.11, 0], # Naturales
            [3.5, 0.0, 2.0, 0.15, 1], [4.2, 0.5, 1.0, 0.16, 1], # Cinético Bunker Buster
            [5.3, 0.0, 0.2, 45.0, 1], [0.0, 0.0, 2.0, 15.0, 0] # Fuga/Nuclear
        ])
        y_train = np.array([0, 0, 0, 1, 1, 2, 2])
        self.X_train_scaled = self.scaler.fit_transform(X_train)
        self.modelo.fit(self.X_train_scaled, y_train)

    def evaluar(self, mag, prof, lat, lon):
        dist_min, es_sub = 9999, 0
        for d in INSTALACIONES_NUCLEAR_ME.values():
            dist = calcular_distancia(lat, lon, d['coords'][0], d['coords'][1])
            if dist < dist_min: dist_min, es_sub = dist, d['sub']
        datos = self.scaler.transform([[mag, prof, dist_min, 0.15, es_sub]])
        return self.modelo.predict(datos)[0], round(max(self.modelo.predict_proba(datos)[0])*100, 2), round(dist_min, 2)

class RadarVisiónTotal:
    def __init__(self):
        self.ia = CerebroNeuronalETB()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json'
        })
        
    def generar_mapa(self):
        print("\n" + "="*70 + "\nRADAR E.T.B. v10.4 - SATÉLITE + HUD REUBICADO\n" + "="*70)
        
        mapa = folium.Map(location=[31.0, 45.0], zoom_start=5, tiles='CartoDB dark_matter')
        
        capa_ciudadelas = folium.FeatureGroup(name="🏗️ Ciudadelas y Reactores").add_to(mapa)
        capa_sensores = folium.FeatureGroup(name="🟢 Datos Brutos: Sensores SafeCast").add_to(mapa)
        capa_tectonica = folium.FeatureGroup(name="🔵 Datos Brutos: Sismos USGS").add_to(mapa)
        capa_alertas = folium.FeatureGroup(name="🔴 Análisis IA (Anomalías)").add_to(mapa)

        # 1. PINTAR TODAS LAS CIUDADELAS Y CENTRALES
        for nom, d in INSTALACIONES_NUCLEAR_ME.items():
            color_icono = "darkred" if d['sub'] == 1 else "blue"
            icono_fa = "mountain" if d['sub'] == 1 else "radiation"
            html_nodo = f"<div style='width:200px; font-family:Arial;'><b>{nom}</b><hr><b>País:</b> {d['pais']}<br><b>Tipo:</b> {d['desc']}</div>"
            folium.Marker(
                location=d['coords'], 
                icon=folium.Icon(color=color_icono, icon=icono_fa, prefix="fa"),
                popup=folium.Popup(html_nodo, max_width=250)
            ).add_to(capa_ciudadelas)

        # 2. PINTAR DATOS BRUTOS: SENSORES DE RADIACIÓN (CORREGIDO PARA TIEMPO REAL)
        rad_count = 0
        try:
            print("Descargando telemetría de radiación OSINT (Filtro Reciente)...")
            coordenadas_tacticas = [
                (31.7, 35.2), # Israel
                (32.0, 50.0), # Centro Irán
                (24.0, 54.0), # Golfo / Omán
                (39.0, 35.0)  # Turquía
            ]
            
            estaciones = {}
            for lat_base, lon_base in coordenadas_tacticas:
                # --- AQUÍ ESTÁ LA MAGIA: order=captured_at+desc ---
                url_rad = f"https://api.safecast.org/measurements.json?latitude={lat_base}&longitude={lon_base}&distance=1000000&order=captured_at+desc"
                rad_resp = self.session.get(url_rad, timeout=10)
                
                if rad_resp.status_code == 200:
                    data = rad_resp.json()
                    for r in data[:20]: # Toma los 20 más recientes por zona
                        id_est = f"{round(r['latitude'],3)}_{round(r['longitude'],3)}"
                        if id_est not in estaciones:
                            estaciones[id_est] = r
                            # Destacamos si la radiación es peligrosa (> 1.0 uSv/h)
                            es_peligro = float(r['value']) > 1.0
                            color_rad = "red" if es_peligro else "lime"
                            
                            html_rad = f"<div style='width:180px; font-family:monospace;'><b style='color:{color_rad};'>Sensor OSINT</b><hr><b>Valor:</b> {r['value']} {r['unit']}<br><b>Fecha:</b> {r['captured_at'][:10]}<br><b>Hora:</b> {r['captured_at'][11:19]}</div>"
                            
                            folium.CircleMarker(
                                [r['latitude'], r['longitude']], radius=5, color=color_rad, fill=True, fillOpacity=0.8,
                                popup=folium.Popup(html_rad, max_width=200)
                            ).add_to(capa_sensores)
                
            rad_count = len(estaciones)
            if rad_count > 0:
                print(f"-> EXITO: {rad_count} sensores activos y recientes plasmados en el mapa.")
            else:
                print("-> AVISO: Red SafeCast inactiva en la región actualmente (Devolvió 0 datos).")
                
        except Exception as e: print(f"-> Error crítico cargando radiación: {e}")

        # 3. PINTAR DATOS BRUTOS: MOVIMIENTOS TECTÓNICOS (USGS) + ANÁLISIS IA (BLINDADO)
        sismos_total, alertas_ia = 0, 0
        try:
            print("Descargando telemetría sísmica del USGS (Forzando conexión)...")
            start = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
            # Bajamos la magnitud a 1.5 para detectar "Bunker Busters" pequeños
            url_sismos = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={start}&minmagnitude=1.5&minlatitude=20&maxlatitude=45&minlongitude=25&maxlongitude=65"
            
            # SISTEMA DE REINTENTOS ANTIFALLAS (Bypass de bloqueos temporales)
            intentos = 0
            exito = False
            sismos_data = None
            
            while intentos < 3 and not exito:
                try:
                    sismos_resp = self.session.get(url_sismos, timeout=15)
                    if sismos_resp.status_code == 200:
                        sismos_data = sismos_resp.json()
                        exito = True
                    else:
                        intentos += 1
                        time.sleep(2) # Espera antes de golpear la puerta de nuevo
                except Exception as req_err:
                    print(f"   [!] Falla de red USGS (Intento {intentos+1}/3). Reintentando...")
                    intentos += 1
                    time.sleep(2)

            if exito and sismos_data:
                for f in sismos_data.get('features', []):
                    sismos_total += 1
                    lat, lon, prof = f['geometry']['coordinates'][1], f['geometry']['coordinates'][0], f['geometry']['coordinates'][2]
                    mag = f['properties']['mag']
                    lugar = f['properties']['place']
                    
                    tipo_ia, certeza, dist_nodo = self.ia.evaluar(mag, prof, lat, lon)
                    
                    if tipo_ia > 0:
                        alertas_ia += 1
                        color = "orange" if tipo_ia == 1 else "red"
                        clasif = "⚠️ POSIBLE IMPACTO CINÉTICO" if tipo_ia == 1 else "☢️ ALERTA CRÍTICA (FUGA/NUCLEAR)"
                        capa_destino = capa_alertas
                        radio = max(mag * 4, 5) # Asegura un tamaño mínimo visible
                    else:
                        color = "blue"
                        clasif = "🔵 EVENTO TECTÓNICO (Dato Bruto)"
                        capa_destino = capa_tectonica
                        radio = max(mag * 2.5, 3) 

                    # Etiqueta original con todos los datos brutos + Análisis
                    html_sismo = f"""
                    <div style="font-family:monospace; width:220px; background:#111; color:#fff; padding:10px; border:1px solid {color}; border-radius:4px;">
                        <b style="color:{color}; font-size:12px;">{clasif}</b><hr style="border-color:#333; margin:6px 0;">
                        <b style="color:#aaa;">Ubicación:</b> {lugar}<br>
                        <b style="color:#aaa;">Magnitud:</b> {mag}<br>
                        <b style="color:#aaa;">Profundidad:</b> <span style="color:{'red' if prof < 3 else 'white'};">{prof} km</span><br>
                        <b style="color:#aaa;">Dist. a Nodo Crítico:</b> {dist_nodo} km<br>
                        <div style="background:{color}; color:#fff; text-align:center; padding:4px; margin-top:6px; font-weight:bold;">
                            ANÁLISIS IA: {certeza}% Certeza
                        </div>
                    </div>
                    """
                    folium.CircleMarker(
                        [lat, lon], radius=radio, color=color, fill=True, fillOpacity=0.6,
                        popup=folium.Popup(html_sismo, max_width=250)
                    ).add_to(capa_destino)
                print(f"-> EXITO: {sismos_total} sismos brutos plasmados en el mapa.")
            else:
                print("-> ERROR FATAL: Imposible conectar con la red sísmica (USGS) tras 3 intentos. Posible bloqueo regional o caída de DNS.")
                
        except Exception as e: print(f"-> Error cargando sismos: {e}")

        # 4. CAPA 3: DATOS SATELITALES (NUEVO CÓDIGO INYECTADO Y FORZADO)
        try:
            print("Conectando con órbita: Descargando Capas Satelitales (NASA GIBS)...")
            fecha_segura = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
            
            # Satélite Óptico (Terreno y nubes reales)
            folium.raster_layers.WmsTileLayer(
                url='https://gibs.earthdata.nasa.gov/wms/epsg3857/best/wms.cgi',
                layers='MODIS_Terra_CorrectedReflectance_TrueColor',
                name='🛰️ Satélite Óptico (Terreno Real)',
                fmt='image/jpeg',
                transparent=False,
                overlay=True,
                control=True,
                TIME=fecha_segura,
                attr='NASA GIBS'
            ).add_to(mapa)

            # Capa de Aerosoles (Humo y gases invisibles)
            folium.raster_layers.WmsTileLayer(
                url='https://gibs.earthdata.nasa.gov/wms/epsg3857/best/wms.cgi',
                layers='MODIS_Terra_Aerosol',
                name='☁️ Satélite: Índice de Aerosoles',
                fmt='image/png',
                transparent=True,
                overlay=True,
                control=True,
                TIME=fecha_segura,
                attr='NASA GIBS'
            ).add_to(mapa)
            print("-> EXITO: Satélites enlazados correctamente.")
        except Exception as e: 
            print(f"-> Error crítico cargando telemetría satelital: {e}")

        # --- HUD DE PATÍA GLOBAL REUBICADO ABAJO A LA IZQUIERDA ---
        panel_html = f"""
        <div style="position: fixed; bottom: 20px; left: 20px; width: 340px; background: rgba(0,0,0,0.9); border: 2px solid {'red' if alertas_ia > 0 else 'lime'}; padding: 15px; color: #fff; font-family: monospace; z-index: 9999; border-radius: 5px;">
            <b style="font-size:16px; color:{'red' if alertas_ia > 0 else 'lime'};">🌐 E.T.B. v10.4 - VISIÓN TOTAL</b><br>
            <span style="font-size:10px; color:#aaa;">DATOS BRUTOS + IA + SATÉLITE ESPACIAL</span><hr style="border-color:#444;">
            Nodos Vigilados: <b>{len(INSTALACIONES_NUCLEAR_ME)}</b><br>
            Capa 3 (Satelital): <b style="color:cyan;">ACTIVA (NASA OMPS)</b><br>
            Sensores OSINT: <b style="color:lime;">{rad_count}</b><br>
            Sismos (7 días): <b style="color:#4287f5;">{sismos_total}</b><br>
            Anomalías IA: <b style="color:red; font-size:14px;">{alertas_ia}</b><br>
            <div style="margin-top: 10px; border-top: 1px solid #333; padding-top: 5px; font-size: 9px; color: #888; text-align: center;">
                Sincronizado: {datetime.datetime.now().strftime('%H:%M')}
            </div>
        </div>
        """
        mapa.get_root().html.add_child(folium.Element(panel_html))
        
        folium.LayerControl(collapsed=False).add_to(mapa)
        
        mapa.save("radar_nuclear_estrategico.html")
        print("\n[✅ RADAR VISIÓN TOTAL GENERADO CON ÉXITO: radar_nuclear_estrategico.html]")

if __name__ == "__main__":
    RadarVisiónTotal().generar_mapa()