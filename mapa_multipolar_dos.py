import feedparser
import folium
from folium.plugins import MarkerCluster
import datetime
import requests
from deep_translator import GoogleTranslator

feedparser.USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# --- 1. DICCIONARIO TÁCTICO EXTREMO (MEDIO ORIENTE Y PUNTOS MARÍTIMOS) ---
COORDENADAS_CLAVE = {
    # Israel / Palestina
    "tel aviv": [32.0853, 34.7818], "telavit": [32.0853, 34.7818],
    "jerusalén": [31.7683, 35.2137], "jerusalem": [31.7683, 35.2137],
    "haifa": [32.7940, 34.9896], "gaza": [31.5017, 34.4668],
    "ashkelon": [31.6693, 34.5715], "beersheba": [31.2518, 34.7913],
    "eilat": [29.5577, 34.9519], "rafa": [31.2968, 34.2435],
    
    # Irán
    "teherán": [35.6892, 51.3890], "tehran": [35.6892, 51.3890],
    "isfahán": [32.6539, 51.6660], "shiraz": [29.5918, 52.5837],
    "bandar abbas": [27.1832, 56.2666],
    
    # Líbano y Siria
    "beirut": [33.8938, 35.5018], "tiro": [33.2705, 35.1966],
    "damasco": [33.5138, 36.2765], "damascus": [33.5138, 36.2765],
    "alepo": [36.2021, 37.1343],
    
    # Yemen, Irak y Resto del Golfo
    "saná": [15.3694, 44.2045], "sanaa": [15.3694, 44.2045],
    "hodeida": [14.7979, 42.9530], "bagdad": [33.3152, 44.3661],
    "baghdad": [33.3152, 44.3661], "erbil": [36.1901, 44.0086],
    "basora": [30.5081, 47.7835], "riad": [24.7136, 46.6753],
    "doha": [25.2854, 51.5310], "dubái": [25.2048, 55.2708],
    
    # Puntos Estratégicos Marítimos
    "estrecho de ormuz": [26.56, 56.25], "ormuz": [26.56, 56.25],
    "strait of hormuz": [26.56, 56.25], "mar rojo": [20.0, 38.0],
    "red sea": [20.0, 38.0], "canal de suez": [29.9, 32.5],
    "bab el-mandeb": [12.58, 43.33], "golfo de adén": [12.0, 48.0]
}

def traducir_texto(texto):
    if not texto: return ""
    try: return GoogleTranslator(source='auto', target='es').translate(texto)
    except: return texto

def obtener_datos_petroleo():
    url = "https://query1.finance.yahoo.com/v8/finance/chart/BZ=F"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        respuesta = requests.get(url, headers=headers)
        precio = respuesta.json()['chart']['result'][0]['meta']['regularMarketPrice']
        variacion_pct = (precio - 74.0) / 74.0
        alza = int(15600 * (variacion_pct * 0.65))
        return precio, max(0, alza)
    except: return 0, 0

def generar_mapa_multipolar():
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Iniciando Radar de E.T.B. con Proxy Antibloqueo TOTAL...")
    
    fuentes_rss = [
        ("https://gcaptain.com/feed/", "gCaptain (Naval)"),
        ("https://feeds.bbci.co.uk/mundo/rss.xml", "BBC (Reino Unido)"),
        ("https://news.google.com/rss/search?q=site:elpais.com+oriente+medio+OR+israel+OR+iran&hl=es-419&gl=CO&ceid=CO:es-419", "El País (Vía Proxy)"),
        ("https://news.google.com/rss/search?q=source:reuters+middle+east&hl=en-US&gl=US&ceid=US:en", "Reuters (Occidente)"), 
        # --- AQUÍ ESTÁ EL AJUSTE PARA HISPANTV ---
        ("https://news.google.com/rss/search?q=site:hispantv.com+israel+OR+iran+OR+eeuu+OR+guerra&hl=es-419&gl=CO&ceid=CO:es-419", "HispanTV (Irán - Vía Proxy)"),
        ("https://news.google.com/rss/search?q=site:en.irna.ir+israel+OR+iran+OR+military&hl=en-US&gl=US&ceid=US:en", "IRNA (Irán - Vía Proxy)"),
        ("https://www.aljazeera.com/xml/rss/all.xml", "Al Jazeera (Qatar)"),
        ("https://actualidad.rt.com/rss", "RT (Rusia)"),
        ("https://news.google.com/rss/search?q=site:spanish.news.cn+israel+OR+iran+OR+oriente&hl=es-419&gl=CO&ceid=CO:es-419", "Xinhua (Vía Proxy)"),
        ("https://news.google.com/rss/search?q=site:timesofisrael.com+israel&hl=en-US&gl=US&ceid=US:en", "Times of Israel (Vía Proxy)"),
        ("https://news.google.com/rss/search?q=site:jpost.com+israel&hl=en-US&gl=US&ceid=US:en", "Jerusalem Post (Vía Proxy)")
    ]
    
    palabras_clave = [
        'misil', 'misiles', 'ataque', 'bombardeo', 'dron', 'impacto', 'explosión', 
        'ofensiva', 'sionista', 'resistencia', 'occidente', 'represalia', 'terrorista', 'cohete',
        'missile', 'attack', 'strike', 'drone', 'explosion', 'idf', 'hezbollah', 'iran', 'hamas', 'rocket', 'terror',
        'militar', 'tensión', 'ejército', 'tanker', 'vessel', 'ship', 'shipping', 'hormuz', 'barco', 'petrolero',
        'gerald', 'ford', 'carrier', 'portaaviones', 'destructor', 'destroyer', 'fragata', 'frigate', 'submarino',
        'bloqueo', 'blockade', 'houthi', 'hutí', 'rebeldes', 'base', 'tropas', 'troops', 'amenaza', 'threat',
        'israel', 'israelí', 'israeli', 'tel aviv', 'telavit', 'jerusalén', 'jerusalem', 'haifa', 'netanyahu', 'mossad'
    ]
    
    mapa_osint = folium.Map(location=[30.0, 40.0], zoom_start=5, tiles='CartoDB dark_matter')
    agrupador_noticias = MarkerCluster(name="Reportes").add_to(mapa_osint)
    
    impactos = 0
    for url, agencia in fuentes_rss:
        print(f"[*] Escaneando antena: {agencia}...") 
        try:
            flujo = feedparser.parse(url)
            
            if hasattr(flujo, 'bozo_exception'):
                print(f"   [!] Bloqueo detectado en {agencia}: {flujo.bozo_exception}")
                continue

            for entrada in flujo.entries:
                texto = (entrada.get('title', '') + " " + entrada.get('description', '')).lower()
                
                if any(p in texto for p in palabras_clave):
                    coordenada_encontrada = None
                    
                    for ciudad, coords in COORDENADAS_CLAVE.items():
                        if ciudad in texto:
                            coordenada_encontrada = coords
                            break
                    
                    if not coordenada_encontrada:
                        if any(x in agencia for x in ['Irán', 'HispanTV', 'IRNA']): coordenada_encontrada = [35.6892, 51.3890]
                        elif any(x in agencia for x in ['Israel', 'Jerusalem']): coordenada_encontrada = [32.0853, 34.7818]
                        elif any(x in agencia for x in ['Naval', 'gCaptain']): coordenada_encontrada = [26.56, 56.25]
                        elif 'Rusia' in agencia: coordenada_encontrada = [55.7558, 37.6173]
                        elif any(x in agencia for x in ['China', 'Xinhua']): coordenada_encontrada = [39.9042, 116.4074]
                        else: coordenada_encontrada = [31.0, 40.0] 
                    
                    if coordenada_encontrada:
                        titulo_es = traducir_texto(entrada.title)
                        info_html = f"<b>{agencia}</b><br>{titulo_es}<br><a href='{entrada.link}' target='_blank'>Leer más</a>"
                        
                        if any(x in agencia for x in ['Irán', 'Rusia', 'China', 'IRNA', 'Xinhua', 'HispanTV']): color = 'red'
                        elif any(x in agencia for x in ['Israel', 'Jerusalem', 'Reuters']): color = 'blue'
                        elif 'gCaptain' in agencia: color = 'lightgray'
                        else: color = 'orange'
                        
                        folium.Marker(location=coordenada_encontrada, popup=folium.Popup(info_html, max_width=250),
                                      icon=folium.Icon(color=color, icon='ship' if 'gCaptain' in agencia else 'info-sign')).add_to(agrupador_noticias)
                        impactos += 1
                        
        except Exception as e: 
            print(f"   [!] Error fatal en la antena {agencia}: {e}")
            continue

    p_brent, a_gas = obtener_datos_petroleo()
    color_b = "#ff4444" if a_gas > 500 else "#00ff41"
    panel_html = f"""
    <div style="position: fixed; bottom: 35px; left: 20px; width: 240px; height: 140px; 
                background-color: rgba(0, 0, 0, 0.9); border: 2px solid {color_b}; z-index:9999; 
                color: white; font-family: 'Courier New', Courier; padding: 15px; border-radius: 12px; 
                box-shadow: 0 0 20px {color_b}; line-height: 1.5;">
        <b style="color: #ffcc00; font-size: 13px; letter-spacing: 1px;">CENTRO DE MANDO E.T.B.</b><br>
        <hr style="border: 0.5px solid #444; margin: 10px 0;">
        <span style="font-size: 16px;">BRENT: <b style="color: #ffffff;">${p_brent:.2f}</b></span><br>
        <span style="font-size: 12px; color: #ff4444; font-weight: bold;">PROY. ALZA GASOLINA:</span><br>
        <span style="font-size: 24px; font-weight: bold; color: #ff4444;">+${a_gas} <small style="font-size: 11px;">/gal</small></span>
    </div>
    """
    mapa_osint.get_root().html.add_child(folium.Element(panel_html))
    mapa_osint.save("radar_geopolitico_standalone.html")
    print(f"-> Sistema Operativo. Reportes Totales: {impactos} | Brent: ${p_brent:.2f}")

if __name__ == "__main__":
    generar_mapa_multipolar()