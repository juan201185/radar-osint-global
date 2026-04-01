import folium
from folium.plugins import MarkerCluster, AntPath
import requests
import datetime
import random
import feedparser

class RadarFinancieroGuerra:
    def __init__(self):
        self.transacciones_detectadas = []
        self.nodos_hft = {
            "NY-Server (ICE)": {"coords": [40.71, -74.00], "tipo": "Liquidez"},
            "LDN-Server (LME)": {"coords": [51.50, -0.12], "tipo": "Liquidez"},
            "SG-Server (SGX)": {"coords": [1.35, 103.81], "tipo": "Liquidez"}
        }
        
        # Base de datos táctica para geolocalización dinámica (OSINT Básico)
        self.diccionario_puertos = {
            "iran": [32.42, 53.68], "kharg": [29.23, 50.31], "bandar abbas": [27.18, 56.26],
            "china": [35.86, 104.19], "qingdao": [36.06, 120.38], "shandong": [36.65, 117.12],
            "venezuela": [6.42, -66.58], "jose": [10.08, -64.84], "puerto la cruz": [10.22, -64.63],
            "russia": [61.52, 105.31], "primorsk": [60.36, 28.57], "novorossiysk": [44.72, 37.76],
            "india": [20.59, 78.96], "jamnagar": [22.47, 70.07], "sikka": [22.43, 69.83],
            "syria": [34.80, 38.99], "baniyas": [35.18, 35.93], "latakia": [35.53, 35.78]
        }
        
    def obtener_precios_tiempo_real(self):
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Sincronizando mercados y volatilidad...")
        activos = {"Brent": "BZ=F", "WTI": "CL=F", "Natural_Gas": "NG=F"}
        precios_vivos = {}
        headers = {'User-Agent': 'Mozilla/5.0'}

        for nombre, ticker in activos.items():
            try:
                url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
                resp = requests.get(url, headers=headers, timeout=10)
                if resp.status_code == 200:
                    data = resp.json()['chart']['result'][0]['meta']
                    precio = data['regularMarketPrice']
                    prev_close = data.get('previousClose', precio)
                    cambio = ((precio - prev_close) / prev_close) * 100 if prev_close else 0
                    precios_vivos[nombre] = {"precio": round(precio, 2), "cambio": round(cambio, 2)}
                else:
                    precios_vivos[nombre] = {"precio": 0.0, "cambio": 0.0}
            except:
                precios_vivos[nombre] = {"precio": 0.0, "cambio": 0.0}

        precio_brent = precios_vivos.get("Brent", {}).get("precio", 0)
        precios_vivos["Iran_Heavy"] = {"precio": round(precio_brent * 0.85, 2), "cambio": 0}
        precios_vivos["Ural"] = {"precio": round(precio_brent * 0.90, 2), "cambio": 0}
        return precios_vivos

    def extraer_coordenadas_por_entidad(self, texto):
        """Mini-motor NLP: Busca lugares en el texto y devuelve coordenadas únicas"""
        lugares_encontrados = []
        texto_limpio = texto.lower()
        
        for lugar, coords in self.diccionario_puertos.items():
            if lugar in texto_limpio:
                # Agregamos una micro-dispersión aleatoria para evitar que rutas al mismo país se apilen exactamente
                lat_dispersa = coords[0] + random.uniform(-0.5, 0.5)
                lon_dispersa = coords[1] + random.uniform(-0.5, 0.5)
                lugares_encontrados.append((lugar.capitalize(), [lat_dispersa, lon_dispersa]))
        
        # Lógica de asignación origen/destino
        if len(lugares_encontrados) >= 2:
            return lugares_encontrados[0][1], lugares_encontrados[1][1], f"Ruta {lugares_encontrados[0][0]}-{lugares_encontrados[1][0]}"
        elif len(lugares_encontrados) == 1:
            # Si solo encuentra un lugar, asume que es el destino de una carga misteriosa
            origen_fantasma = [lugares_encontrados[0][1][0] - 5, lugares_encontrados[0][1][1] - 10]
            return origen_fantasma, lugares_encontrados[0][1], f"Llegada a {lugares_encontrados[0][0]}"
        else:
            # Fallback si no encuentra nada
            lat_f, lon_f = random.uniform(20, 30), random.uniform(50, 60)
            return [lat_f, lon_f], [lat_f+2, lon_f+5], "Ruta Regional Indetectada"

    def rastrear_flujos_osint(self):
        """Motor OSINT DINÁMICO: Extrae coordenadas directamente del titular"""
        print(f"   [!] Analizando vectores OSINT con Geolocalización Dinámica...")
        url_osint = "https://news.google.com/rss/search?q=iran+oil+export+china+OR+venezuela+tanker+OR+russia+oil+shadow+fleet&hl=es-419&gl=CO&ceid=CO:es-419"
        flujos_reales = []
        
        try:
            flujo = feedparser.parse(url_osint)
            # Tomamos hasta 5 noticias ahora que no se van a superponer
            for entry in flujo.entries[:5]:
                titulo = entry.get('title', 'Flujo Detectado').split(' - ')[0]
                
                # --- NUEVO: Llamada al motor de extracción ---
                orig, dest, desc = self.extraer_coordenadas_por_entidad(titulo)

                flujos_reales.append({
                    "origen": "Punto de Carga", 
                    "destino": "Descarga",
                    "coord_origen": orig, 
                    "coord_destino": dest,
                    "alerta": titulo[:85] + "...",
                    "descripcion": desc
                })
            return flujos_reales
        except:
            print("   [❌] Error leyendo feed OSINT")
            return []

    def generar_mapa(self):
        print("\n" + "="*70)
        print("INICIANDO RADAR FINANCIERO E.T.B. (OSINT DINÁMICO + HFT)")
        print("="*70)
        datos_mercado = self.obtener_precios_tiempo_real()
        mapa = folium.Map(location=[20.0, 40.0], zoom_start=3, tiles='CartoDB dark_matter')
        
        capa_flujos = folium.FeatureGroup(name="🛢️ Flujos Dinámicos (OSINT)").add_to(mapa)
        capa_sanciones = folium.FeatureGroup(name="💰 Nodos de Evasión SWIFT").add_to(mapa)
        capa_hft = folium.FeatureGroup(name="⚡ Servidores Alta Frecuencia (HFT)").add_to(mapa)
        
        # 1. Flujos Dinámicos
        flujos = self.rastrear_flujos_osint()
        for f in flujos:
            AntPath(
                locations=[f['coord_origen'], f['coord_destino']],
                color='#ffcc00', weight=3, opacity=0.8, delay=1000,
                tooltip=f.get('descripcion')
            ).add_to(capa_flujos)
            
            popup_html = f"""
            <div style="font-family: 'Courier New', monospace; width: 250px; background: #000; color: #fff; padding: 10px; border-left: 4px solid #ffcc00;">
                <b style="color:#ffcc00;">DETECCIÓN DINÁMICA</b><br><br>
                <b>Vector:</b> {f['descripcion']}<br>
                <b>Reporte:</b> {f['alerta']}
            </div>
            """
            folium.Marker(f['coord_origen'], icon=folium.Icon(color='red', icon='oil-can', prefix='fa'), popup=popup_html).add_to(capa_flujos)
            folium.Marker(f['coord_destino'], icon=folium.Icon(color='orange', icon='industry', prefix='fa')).add_to(capa_flujos)

        # 2. Nodos Estratégicos
        centros = {"Dubai (Hawala)": [25.2, 55.2], "Moscú (SPFS)": [55.7, 37.6], "Pekín (CIPS)": [39.9, 116.4]}
        for nom, coor in centros.items():
            folium.CircleMarker(coor, radius=10, color='purple', fill=True, popup=nom).add_to(capa_sanciones)

        # 3. Nodos HFT
        for nom, info in self.nodos_hft.items():
            folium.CircleMarker(info['coords'], radius=6, color='#00ff41', fill=True, fill_opacity=0.7, popup=f"<b>SERVIDOR HFT:</b> {nom}").add_to(capa_hft)

        # Panel Informativo
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        volatilidad_brent = datos_mercado.get('Brent', {}).get('cambio', 0)
        color_borde = "#00ff41" if abs(volatilidad_brent) < 1.5 else "#ff4444"
        estatus_hft = "NORMAL" if abs(volatilidad_brent) < 1.5 else "ESTRÉS ALGORÍTMICO"

        panel_html = f"""
        <div style="position: fixed; top: 20px; right: 20px; width: 320px; background: rgba(10,10,10,0.95); 
                    color: #fff; border: 2px solid {color_borde}; padding: 15px; border-radius: 10px; 
                    font-family: 'Courier New', monospace; font-size: 11px; z-index: 9999;">
            <h4 style="color:#ffcc00; text-align:center; margin:0 0 10px 0;">💰 RADAR FINANCIERO E.T.B.</h4>
            <div style="border-bottom: 1px solid #333; padding-bottom: 8px; margin-bottom: 10px;">
                <b>MERCADO EN VIVO (HFT SENSOR):</b><br>
                <div style="display:flex; justify-content:space-between; margin-top:5px;">
                    <span>🛢️ Brent:</span> <span style="color:#00ff41;">${datos_mercado.get('Brent', {}).get('precio', 0)} <small style="color:{color_borde};">({datos_mercado.get('Brent', {}).get('cambio', 0)}%)</small></span>
                </div>
                <div style="display:flex; justify-content:space-between;">
                    <span>🔥 Gas Natural:</span> <span style="color:#00ff41;">${datos_mercado.get('Natural_Gas', {}).get('precio', 0)} <small>({datos_mercado.get('Natural_Gas', {}).get('cambio', 0)}%)</small></span>
                </div>
                <div style="display:flex; justify-content:space-between;">
                    <span>🇮🇷 Iran Heavy:</span> <span style="color:#ff4444;">${datos_mercado.get('Iran_Heavy', {}).get('precio', 0)}</span>
                </div>
            </div>
            <div style="font-size: 10px; line-height: 1.4;">
                <b>ESTADO SISTÉMICO:</b><br>
                Volatilidad HFT: <span style="color:{color_borde}; font-weight:bold;">{estatus_hft}</span><br>
                Rutas OSINT Activas: {len(flujos)} vectores únicos<br>
                Actualizado: {timestamp}
            </div>
        </div>
        """
        mapa.get_root().html.add_child(folium.Element(panel_html))
        folium.LayerControl(position='bottomleft').add_to(mapa)
        
        # Archivo guardado correctamente con el nombre original
        mapa.save("radar_financiero_guerra.html")
        print(f"[✅ RADAR FINANCIERO + HFT GENERADO]")

if __name__ == "__main__":
    radar = RadarFinancieroGuerra()
    radar.generar_mapa()