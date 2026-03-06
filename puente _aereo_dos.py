import requests
import folium
import datetime

def rastrear_puente_aereo():
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Escaneando red satelital con filtros de alta eficiencia...")
    
    # Mapa centrado entre EE.UU., Europa y Medio Oriente
    mapa_logistico = folium.Map(location=[40.0, -10.0], zoom_start=3, tiles='CartoDB dark_matter')
    
    # --- 3 CAPAS TÁCTICAS ---
    capa_militar = folium.FeatureGroup(name="🟢 Fuerzas Armadas (EE.UU. / OTAN)").add_to(mapa_logistico)
    capa_craf = folium.FeatureGroup(name="🟠 Contratistas de Defensa (CRAF)").add_to(mapa_logistico)
    capa_israel_aliados = folium.FeatureGroup(name="🔵 Línea de Vida Israel / Logística Global").add_to(mapa_logistico)
    
    url = "https://opensky-network.org/api/states/all"
    
    try:
        respuesta = requests.get(url, timeout=20)
        
        if respuesta.status_code == 200:
            datos = respuesta.json()
            vuelos = datos.get('states', [])
            
            militares = 0
            contratistas = 0
            aliados = 0
            
            # 1. Fuerzas Armadas Oficiales (Verdes)
            prefijos_militares = ('RCH', 'REACH', 'CNV', 'RRR', 'NATO', 'MMF', 'CFC', 'ASY', 'SAM', 'SPAR')
            
            # 2. Contratistas Privados CRAF Ampliado (Naranjas)
            prefijos_craf = ('GTI', 'CKS', 'NCR', 'OAE', 'CMB', 'SOO', 'ABX', 'ATN', 'PAC')
            
            # 3. Puente Aéreo Israelí y Soporte Pesado (Azules)
            prefijos_israel_aliados = ('ELY', 'CAL', 'IAF', 'FDX', 'UPS')
            
            for vuelo in vuelos:
                if vuelo[1]:
                    callsign = vuelo[1].strip().upper()
                    lon = vuelo[5]
                    lat = vuelo[6]
                    altitud = vuelo[7]
                    velocidad = vuelo[9]
                    origen = vuelo[2]
                    
                    if lat and lon: # Si hay coordenadas válidas
                        
                        # Filtro 1: Militares Puros
                        if callsign.startswith(prefijos_militares):
                            info = f"<div style='width:200px; font-family: Courier New;'><b>🟢 MILITAR OTAN/EEUU</b><hr><b>Vuelo:</b> {callsign}<br><b>Origen:</b> {origen}<br><b>Alt:</b> {altitud}m</div>"
                            folium.Marker(location=[lat, lon], popup=info, icon=folium.Icon(color='green', icon='fighter-jet', prefix='fa')).add_to(capa_militar)
                            militares += 1
                            
                        # Filtro 2: Contratistas de Defensa
                        elif callsign.startswith(prefijos_craf):
                            info = f"<div style='width:200px; font-family: Courier New;'><b>🟠 CONTRATISTA (CRAF)</b><hr><b>Vuelo:</b> {callsign}<br><b>Origen:</b> {origen}<br><b>Alt:</b> {altitud}m</div>"
                            folium.Marker(location=[lat, lon], popup=info, icon=folium.Icon(color='orange', icon='plane', prefix='fa')).add_to(capa_craf)
                            contratistas += 1
                            
                        # Filtro 3: Israel & Soporte Logístico Pesado
                        elif callsign.startswith(prefijos_israel_aliados):
                            # Filtramos altitudes mayores a 3000m para no mapear las avionetitas locales de FedEx
                            if altitud and altitud > 3000:
                                info = f"<div style='width:200px; font-family: Courier New;'><b>🔵 LOGÍSTICA ESTRATÉGICA</b><hr><b>Vuelo:</b> {callsign}<br><b>Origen:</b> {origen}<br><b>Alt:</b> {altitud}m</div>"
                                folium.Marker(location=[lat, lon], popup=info, icon=folium.Icon(color='blue', icon='globe', prefix='fa')).add_to(capa_israel_aliados)
                                aliados += 1
                                
            print(f"   -> Radar Táctico: {militares} Militares | {contratistas} Contratistas | {aliados} Apoyo Estratégico.")
        else:
            print(f"   [!] El servidor rechazó la conexión (Error {respuesta.status_code}).")
            
    except Exception as e:
        print(f"   [!] Error de conexión: {e}")

    # Añadir control de capas y guardar
    folium.LayerControl().add_to(mapa_logistico)
    nombre_mapa = "radar_logistico_atlantico.html"
    mapa_logistico.save(nombre_mapa)
    
    print(f"\n[RADAR MULTICAPA GUARDADO EXITOSAMENTE]")
    print("=========================================")

if __name__ == "__main__":
    rastrear_puente_aereo()