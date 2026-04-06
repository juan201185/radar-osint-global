import folium
import requests
import datetime

# Instalaciones nucleares iraníes (IAEA y OSINT)
INSTALACIONES_NUCLEAR_IRAN = {
    "Natanz": {"coords": [33.7233, 51.7267], "tipo": "Enriquecimiento Uranio", "estado": "Activo - Subterráneo fortificado", "riesgo": "CRITICO", "ultimo_ataque": "2021-04-11"},
    "Fordow": {"coords": [34.8858, 50.9958], "tipo": "Enriquecimiento", "estado": "Activo - Montaña fortificada", "riesgo": "CRITICO", "ultimo_ataque": "Ninguno"},
    "Isfahan": {"coords": [32.6804, 51.6861], "tipo": "Conversión", "estado": "Activo", "riesgo": "ALTO", "ultimo_ataque": "Ninguno"},
    "Arak": {"coords": [34.3747, 49.4736], "tipo": "Reactor", "estado": "Rediseñado", "riesgo": "MEDIO", "ultimo_ataque": "Ninguno"},
    "Parchin": {"coords": [35.5156, 51.8311], "tipo": "Investigación", "estado": "Sospechoso", "riesgo": "ALTO", "ultimo_ataque": "Ninguno"},
    "Bushehr": {"coords": [28.8283, 50.8839], "tipo": "Reactor civil", "estado": "Operativo", "riesgo": "BAJO", "ultimo_ataque": "Ninguno"}
}

# Submarinos israelíes (Simulación)
SUBMARINOS_ISRAEL = {
    "Dolphin": {"base": "Haifa", "coords": [32.8184, 35.0019], "estado": "En patrulla", "armamento": "Popeye Turbo SLCM"}
}

# ¡AQUÍ ESTABA LA LISTA DE JUGUETE QUE ELIMINAMOS!
# EVENTOS_SISMICOS = [...] <- BORRADO

class RadarNuclearEstrategico:
    def __init__(self):
        self.nivel_alerta = "AMARILLO"
        self.tiempo_breakout = "1-2 semanas"
        
    def generar_mapa(self):
        print("\n" + "="*70)
        print("RADAR NUCLEAR ESTRATÉGICO - MODO OSINT EN VIVO V1")
        print("="*70)
        
        mapa = folium.Map(location=[32.0, 50.0], zoom_start=6, tiles='CartoDB dark_matter')
        
        # Capas
        capa_enriquecimiento = folium.FeatureGroup(name="☢️ Enriquecimiento Uranio").add_to(mapa)
        capa_sismicos = folium.FeatureGroup(name="💥 Sismos USGS (EN VIVO)").add_to(mapa)
        
        # 1. Pintar Instalaciones Iraníes
        for nombre, datos in INSTALACIONES_NUCLEAR_IRAN.items():
            color = "red" if datos['riesgo'] == "CRITICO" else "orange"
            folium.Marker(
                datos['coords'],
                popup=f"<b>{nombre}</b><br>Riesgo: {datos['riesgo']}",
                icon=folium.Icon(color=color, icon='radiation', prefix='fa')
            ).add_to(capa_enriquecimiento)

        # 2. SISMOS - RED EUROPEA (EMSC) ANTI-CENSURA
        sismos_total = 0
        try:
            start = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
            # CAMBIAMOS LA URL AL SERVIDOR EUROPEO
            url_sismos = f"https://www.seismicportal.eu/fdsnws/event/1/query?format=json&starttime={start}&minmag=1.5&minlat=20&maxlat=45&minlon=25&maxlon=65"
            
            print("-> Evadiendo USGS... Conectando a la red Europea EMSC...")
            respuesta = requests.get(url_sismos, timeout=15)
            datos_emsc = respuesta.json()
            
            for sismo in datos_emsc.get('features', []):
                try:
                    coords = sismo['geometry']['coordinates']
                    lon, lat = coords[0], coords[1]
                    prof = coords[2] if len(coords) > 2 else 0.0 
                    
                    props = sismo['properties']
                    mag = props.get('mag')
                    if mag is None: continue
                    
                    # Europa usa 'flynn_region' en lugar de 'place' a veces
                    lugar = str(props.get('flynn_region', 'Región de Medio Oriente')).replace("'", "´").replace('"', '“')

                    if prof < 5.0:
                        color_sismo, etiqueta, capa = ('purple', "⚠️ ANOMALÍA SUPERFICIAL", capa_alertas)
                    else:
                        color_sismo, etiqueta, capa = ('blue', "🔵 Sismo Tectónico (EMSC)", capa_tectonica)

                    popup_html = f"<b>{etiqueta}</b><br>Mag: {mag}<br>Prof: {prof} km<br>Lugar: {lugar}"
                    
                    folium.CircleMarker(
                        location=[lat, lon], radius=mag * 3, color=color_sismo, fill=True, fillOpacity=0.6,
                        popup=folium.Popup(popup_html, max_width=250)
                    ).add_to(capa)
                    sismos_total += 1
                except Exception: continue

            print(f"-> EXITO EMSC: {sismos_total} sismos marcados en el terreno.")
        except Exception as e:
            print(f"-> ERROR DE ENLACE EMSC: {e}")

        # HUD Básico original
        panel = f"""
        <div style="position: fixed; top: 20px; right: 20px; width: 280px; 
                    background-color: rgba(10,10,10,0.9); color: #fff; 
                    border: 2px solid #ffaa00; padding: 15px; z-index: 9999;">
            <b style="color:#ffaa00;">☢️ ALERTA: {self.nivel_alerta}</b><hr>
            Sismos detectados (30d): {sismos_total}
        </div>
        """
        mapa.get_root().html.add_child(folium.Element(panel))
        
        folium.LayerControl().add_to(mapa)
        mapa.save("radar_nuclear_estrategico.html")
        print(f"\n[✅ Mapa generado: radar_nuclear_estrategico.html]")

if __name__ == "__main__":
    radar = RadarNuclearEstrategico()
    radar.generar_mapa()