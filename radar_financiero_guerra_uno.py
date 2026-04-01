import folium
from folium.plugins import MarkerCluster, AntPath
import requests
import datetime
import json
import random
import feedparser

class RadarFinancieroGuerra:
    def __init__(self):
        self.transacciones_detectadas = []
        
    def obtener_precios_tiempo_real(self):
        """Motor de Mercados E.T.B.: Extrae Petróleo y Gas desde Yahoo Finance"""
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Sincronizando mercados (Petróleo/Gas)...")
        activos = {
            "Brent": "BZ=F",
            "WTI": "CL=F",
            "Natural_Gas": "NG=F"
        }
        precios_vivos = {}
        headers = {'User-Agent': 'Mozilla/5.0'}

        for nombre, ticker in activos.items():
            try:
                url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
                resp = requests.get(url, headers=headers, timeout=10)
                if resp.status_code == 200:
                    data = resp.json()
                    precio = data['chart']['result'][0]['meta']['regularMarketPrice']
                    precios_vivos[nombre] = round(precio, 2)
                else:
                    precios_vivos[nombre] = 0.0
            except:
                precios_vivos[nombre] = 0.0

        # Cálculo de crudos regionales con diferencial técnico (Sancionados)
        precios_vivos["Iran_Heavy"] = round(precios_vivos.get("Brent", 0) * 0.85, 2)
        precios_vivos["Ural"] = round(precios_vivos.get("Brent", 0) * 0.90, 2)
        
        return precios_vivos

    def rastrear_flujos_osint(self):
        """Motor OSINT: Detecta rutas de exportación reales mediante noticias de última hora"""
        print(f"   [!] Analizando vectores de evasión y flujos Dark Fleet...")
        
        url_osint = "https://news.google.com/rss/search?q=iran+oil+export+china+OR+venezuela+tanker+OR+russia+oil+shadow+fleet&hl=es-419&gl=CO&ceid=CO:es-419"
        flujos_reales = []
        
        try:
            flujo = feedparser.parse(url_osint)
            for entry in flujo.entries[:3]:
                titulo = entry.get('title', 'Flujo Detectado').split(' - ')[0]
                t_low = titulo.lower()
                
                # Georeferenciación dinámica según inteligencia de la noticia
                if 'china' in t_low:
                    orig, dest = [27.18, 56.26], [29.86, 121.54]
                    desc = "Ruta Irán-China (Bypass SWIFT)"
                elif 'venezuela' in t_low:
                    orig, dest = [25.63, 57.76], [10.06, -64.83]
                    desc = "Ruta Transatlántica (Trueque/Barter)"
                else:
                    orig, dest = [35.18, 35.93], [34.73, 36.70]
                    desc = "Suministro Regional Eje Resistencia"

                flujos_reales.append({
                    "origen": "Nodo Sancionado", 
                    "destino": "Receptor Final",
                    "coord_origen": orig, 
                    "coord_destino": dest,
                    "alerta": titulo[:75] + "...",
                    "descripcion": desc
                })
            return flujos_reales
        except:
            return []

    def generar_mapa(self):
        print("\n" + "="*70)
        print("INICIANDO RADAR FINANCIERO E.T.B. (PETRÓLEO, GAS Y SANCIONES)")
        print("="*70)
        
        precios = self.obtener_precios_tiempo_real()
        
        mapa = folium.Map(
            location=[20.0, 40.0],
            zoom_start=3,
            tiles='CartoDB dark_matter'
        )
        
        capa_flujos = folium.FeatureGroup(name="🛢️ Flujos Energéticos (OSINT)").add_to(mapa)
        capa_sanciones = folium.FeatureGroup(name="💰 Nodos de Evasión SWIFT").add_to(mapa)
        
        # 1. Flujos Dinámicos (AntPath)
        flujos = self.rastrear_flujos_osint()
        for f in flujos:
            AntPath(
                locations=[f['coord_origen'], f['coord_destino']],
                color='#ffcc00', weight=3, opacity=0.8, delay=1000,
                tooltip=f.get('descripcion')
            ).add_to(capa_flujos)
            
            popup_html = f"""
            <div style="font-family: 'Courier New', monospace; width: 250px; background: #000; color: #fff; padding: 10px; border-left: 4px solid #ffcc00;">
                <b style="color:#ffcc00;">DETECCIÓN DE FLUJO</b><br><br>
                <b>Estatus:</b> {f['descripcion']}<br>
                <b>Reporte:</b> {f['alerta']}
            </div>
            """
            folium.Marker(f['coord_origen'], icon=folium.Icon(color='red', icon='oil-can', prefix='fa'), popup=popup_html).add_to(capa_flujos)
            folium.Marker(f['coord_destino'], icon=folium.Icon(color='orange', icon='industry', prefix='fa')).add_to(capa_flujos)

        # 2. Nodos Financieros Estratégicos
        centros = {"Dubai (Hawala)": [25.2, 55.2], "Moscú (SPFS)": [55.7, 37.6], "Pekín (CIPS)": [39.9, 116.4]}
        for nom, coor in centros.items():
            folium.CircleMarker(coor, radius=10, color='purple', fill=True, popup=nom).add_to(capa_sanciones)

        # Panel Informativo E.T.B. con GAS NATURAL
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        panel_html = f"""
        <div style="position: fixed; top: 20px; right: 20px; width: 300px; background: rgba(10,10,10,0.95); 
                    color: #fff; border: 2px solid #ffcc00; padding: 15px; border-radius: 10px; 
                    font-family: 'Courier New', monospace; font-size: 11px; z-index: 9999;">
            <h4 style="color:#ffcc00; text-align:center; margin:0 0 10px 0;">💰 RADAR FINANCIERO E.T.B.</h4>
            <div style="border-bottom: 1px solid #333; padding-bottom: 8px; margin-bottom: 10px;">
                <b>MERCADO EN VIVO:</b><br>
                <div style="display:flex; justify-content:space-between; margin-top:5px;">
                    <span>🛢️ Brent:</span> <span style="color:#00ff41;">${precios.get('Brent')}</span>
                </div>
                <div style="display:flex; justify-content:space-between;">
                    <span>🔥 Gas Natural:</span> <span style="color:#00ff41;">${precios.get('Natural_Gas')}</span>
                </div>
                <div style="display:flex; justify-content:space-between;">
                    <span>🇮🇷 Iran Heavy:</span> <span style="color:#ff4444;">${precios.get('Iran_Heavy')}</span>
                </div>
            </div>
            <div style="font-size: 10px; line-height: 1.4;">
                <b>ESTADO DE SANCIONES:</b><br>
                Rutas Activas: {len(flujos)} detectadas<br>
                Sistema Evasión: Activo (Bypass SWIFT)<br>
                Actualizado: {timestamp}
            </div>
        </div>
        """
        mapa.get_root().html.add_child(folium.Element(panel_html))
        folium.LayerControl().add_to(mapa)
        mapa.save("radar_financiero_guerra.html")
        print(f"[✅ RADAR FINANCIERO GENERADO]")

if __name__ == "__main__":
    radar = RadarFinancieroGuerra()
    radar.generar_mapa()