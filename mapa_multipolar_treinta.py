import feedparser
import folium
from folium.plugins import MarkerCluster
import datetime
import requests
from deep_translator import GoogleTranslator
import urllib.parse
import random
import socket
import time
import math
import csv
import io

# --- CONFIGURACIÓN DE RED Y EVASIÓN ---
socket.setdefaulttimeout(20)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0"
]

# --- DICCIONARIO TÁCTICO GLOBAL (MEDIO ORIENTE + ÁFRICA + LATAM SUMADOS) ---
COORDENADAS_CLAVE = {
    # ORIGINALES MEDIO ORIENTE
    "tel aviv": [32.0853, 34.7818], "telavit": [32.0853, 34.7818],
    "jerusalén": [31.7683, 35.2137], "jerusalem": [31.7683, 35.2137],
    "haifa": [32.7940, 34.9896], "gaza": [31.5017, 34.4668],
    "ashkelon": [31.6693, 34.5715], "beersheba": [31.2518, 34.7913],
    "eilat": [29.5577, 34.9519], "rafa": [31.2968, 34.2435],
    "hebron": [31.5326, 35.0998], "al quds": [31.7683, 35.2137],
    "teherán": [35.6892, 51.3890], "tehran": [35.6892, 51.3890],
    "isfahán": [32.6539, 51.6660], "shiraz": [29.5918, 52.5837],
    "bandar abbas": [27.1832, 56.2666], "hormuz": [26.56, 56.25],
    "qom": [34.6401, 50.8764], "mashhad": [36.2605, 59.6168],
    "beirut": [33.8938, 35.5018], "tiro": [33.2705, 35.1966],
    "sidon": [33.5614, 35.3758], "damasco": [33.5138, 36.2765],
    "damascus": [33.5138, 36.2765], "alepo": [36.2021, 37.1343],
    "homs": [34.7308, 36.7094], "saná": [15.3694, 44.2045],
    "sanaa": [15.3694, 44.2045], "hodeida": [14.7979, 42.9530],
    "aden": [12.7855, 45.0145], "bagdad": [33.3152, 44.3661],
    "baghdad": [33.3152, 44.3661], "erbil": [36.1901, 44.0086],
    "basora": [30.5081, 47.7835], "kirkuk": [35.4669, 44.3929],
    "riad": [24.7136, 46.6753], "doha": [25.2854, 51.5310],
    "dubái": [25.2048, 55.2708], "abu dhabi": [24.4539, 54.3773],
    "kuwait": [29.3759, 47.9774], "manama": [26.2285, 50.5860],
    "muscat": [23.5859, 58.4059], "estrecho de ormuz": [26.56, 56.25],
    "strait of hormuz": [26.56, 56.25], "mar rojo": [20.0, 38.0],
    "red sea": [20.0, 38.0], "canal de suez": [29.9, 32.5],
    "bab el-mandeb": [12.58, 43.33], "golfo de adén": [12.0, 48.0],
    "golfo pérsico": [26.0, 52.0], "persian gulf": [26.0, 52.0],
    "pekín": [39.9042, 116.4074], "beijing": [39.9042, 116.4074],
    "moscú": [55.7558, 37.6173], "moscow": [55.7558, 37.6173],
    "ankara": [39.9334, 32.8597], "turquía": [39.9334, 32.8597],
    "cairo": [30.0444, 31.2357], "el cairo": [30.0444, 31.2357],
    # AGREGADOS ÁFRICA
    "niamey": [13.5116, 2.1254], "níger": [13.5116, 2.1254], "niger": [13.5116, 2.1254],
    "bamako": [12.6392, -8.0029], "malí": [12.6392, -8.0029], "mali": [12.6392, -8.0029],
    "ouagadougou": [12.3714, -1.5197], "burkina faso": [12.3714, -1.5197],
    "dakar": [14.7167, -17.4677], "senegal": [14.7167, -17.4677],
    "abuja": [9.0579, 7.4951], "nigeria": [9.0579, 7.4951],
    "jartum": [15.5007, 32.5599], "khartoum": [15.5007, 32.5599], "sudán": [15.5007, 32.5599], "sudan": [15.5007, 32.5599],
    "yibuti": [11.8251, 42.5903], "djibouti": [11.8251, 42.5903],
    "mogadiscio": [2.0469, 45.3182], "mogadishu": [2.0469, 45.3182], "somalia": [2.0469, 45.3182],
    "sahel": [14.0, 0.0],
    # AGREGADOS LATAM (EJE SOBERANÍA)
    "malvinas": [-51.7963, -59.5236], "falkland": [-51.7963, -59.5236],
    "esequibo": [6.13, -59.0], "georgetown": [6.8013, -58.1551],
    "buenos aires": [-34.6037, -58.3816], "caracas": [10.4806, -66.9036],
    "popayán": [2.4411, -76.6061]
}

# --- CÁLCULO DE FRP TÉRMICO ---
def calcular_radio_impacto(frp_valor):
    """Calcula el radio visual del marcador basado en la energía del fuego (MW)"""
    return math.sqrt(frp_valor) * 1.5

def traducir_texto(texto):
    if not texto:
        return ""
    try:
        # Retardo aleatorio para evadir el radar antibots de Google
        time.sleep(random.uniform(0.5, 1.5)) 
        if any('\u4e00' <= char <= '\u9fff' for char in texto):
            return GoogleTranslator(source='zh-CN', target='es').translate(texto)
        if any('\u0600' <= char <= '\u06ff' for char in texto):
            return GoogleTranslator(source='ar', target='es').translate(texto)
        return GoogleTranslator(source='auto', target='es').translate(texto)
    except Exception:
        # Fallback silencioso: si Google tumba la conexión, pasa el texto original sin tirar error en consola
        return texto
def obtener_datos_petroleo():
    print("\n[*] Obteniendo cotización de energía (Bypass total: Cambio de proveedor)...")
    print("   [📡] Conectando a los servidores de CNBC Markets (Nivel Institucional)...")
    
    # El símbolo @LCO.1 corresponde al ICE Brent Crude Oil en la red de CNBC
    url_cnbc = "https://quote.cnbc.com/quote-html-webservice/restQuote/symbolType/symbol?symbols=@LCO.1&requestMethod=itv&noform=1&exthrs=1&output=json"
    
    headers = {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'application/json'
    }
    
    try:
        respuesta = requests.get(url_cnbc, headers=headers, timeout=10)
        datos = respuesta.json()
        
        precio_str = datos['FormattedQuoteResult']['FormattedQuote'][0]['last']
        precio = float(precio_str)
        
        variacion_pct = (precio - 74.0) / 74.0
        alza = int(15600 * (variacion_pct * 0.65))
        
        print(f"   [✓] Extracción limpia y sin bloqueos. Brent: ${precio:.2f}")
        return round(precio, 2), max(0, alza)
        
    except Exception as e:
        print(f"   [❌] Falla en la red satelital secundaria: {str(e)[:30]}")
        return 93.06, 2561

def descargar_termica_nasa(capa_termica):
    """Descarga datos reales del satélite Suomi NPP VIIRS de las últimas 24h"""
    print("   [🛰️] Conectando a los servidores de NASA FIRMS (VIIRS 24h)...")
    url_nasa = "https://firms.modaps.eosdis.nasa.gov/data/active_fire/suomi-npp-viirs-c2/csv/SUOMI_VIIRS_C2_Global_24h.csv"
    
    try:
        headers = {'User-Agent': random.choice(USER_AGENTS)}
        req = requests.get(url_nasa, headers=headers, timeout=20)
        lector = csv.DictReader(io.StringIO(req.text))
        
        impactos_reales = 0
        for fila in lector:
            frp = float(fila['frp'])
            # Solo potencias de fuego extremas (Ignoramos pequeñas fogatas)
            if frp > 50.0:
                lat = float(fila['latitude'])
                lon = float(fila['longitude'])
                radio = calcular_radio_impacto(frp)
                
                folium.CircleMarker(
                    location=[lat, lon], radius=radio, color='#ff4444', fill=True,
                    fill_color='#ff4444', fill_opacity=0.6, 
                    popup=f"<div style='width:160px;font-family:Arial;'><b style='color:red;'>🔥 IMPACTO FÍSICO</b><br><b>FRP:</b> {frp} MW<br><b>Satélite:</b> Suomi NPP<br><b>Hora (UTC):</b> {fila['acq_time']}</div>"
                ).add_to(capa_termica)
                impactos_reales += 1
                
        print(f"   [✓] {impactos_reales} firmas térmicas masivas descargadas y geolocalizadas.")
    except Exception as e:
        print(f"   [❌] Interferencia con satélite NASA: {str(e)[:30]}")

def obtener_feeds_masivos():
    """
    Motor de Ingesta Masiva E.T.B. con Fuentes Originales + Agencias Gringas + ÁFRICA + LATAM
    """
    return [
        # TUS 22 ORIGINALES INTACTOS
        ("https://gcaptain.com/feed/", "gCaptain (Naval)", "occidental"),
        ("https://feeds.bbci.co.uk/mundo/rss.xml", "BBC Mundo (UK)", "occidental"),
        ("https://feeds.bbci.co.uk/news/rss.xml", "BBC News (UK)", "occidental"),
        ("https://news.google.com/rss/search?q=site:cnn.com+israel+OR+iran+OR+middle+east&hl=en-US&gl=US&ceid=US:en", "CNN (USA)", "occidental"),
        ("https://news.google.com/rss/search?q=site:foxnews.com+israel+OR+iran+OR+middle+east&hl=en-US&gl=US&ceid=US:en", "Fox News (USA)", "occidental"),
        ("https://news.google.com/rss/search?q=site:nytimes.com+israel+OR+iran+OR+middle+east&hl=en-US&gl=US&ceid=US:en", "NY Times (USA)", "occidental"),
        ("https://news.google.com/rss/search?q=site:apnews.com+israel+OR+iran+OR+middle+east&hl=en-US&gl=US&ceid=US:en", "AP News (USA)", "occidental"),
        ("https://news.google.com/rss/search?q=site:elpais.com+oriente+medio+OR+israel+OR+iran&hl=es-419&gl=CO&ceid=CO:es-419", "El País (Proxy)", "occidental"),
        ("https://news.google.com/rss/search?q=source:reuters+middle+east&hl=en-US&gl=US&ceid=US:en", "Reuters (Proxy)", "occidental"),
        ("https://news.google.com/rss/search?q=site:hispantv.com+israel+OR+iran+OR+eeuu+OR+guerra&hl=es-419&gl=CO&ceid=CO:es-419", "HispanTV (Proxy)", "resistencia"),
        ("https://news.google.com/rss/search?q=site:en.irna.ir+israel+OR+iran+OR+military&hl=en-US&gl=US&ceid=US:en", "IRNA (Proxy)", "resistencia"),
        ("https://news.google.com/rss/search?q=site:tasnimnews.com+israel+OR+iran+OR+military&hl=en-US&gl=US&ceid=US:en", "Tasnim News (Proxy)", "resistencia"),
        ("https://www.aljazeera.com/xml/rss/all.xml", "Al Jazeera (Qatar)", "independiente"),
        ("https://actualidad.rt.com/rss", "RT (Rusia)", "alternativo"),
        ("https://sputniknews.lat/export/rss2/archive/index.xml", "Sputnik (Rusia)", "alternativo"),
        ("https://news.google.com/rss/search?q=site:spanish.news.cn+israel+OR+iran+OR+oriente&hl=es-419&gl=CO&ceid=CO:es-419", "Xinhua (Proxy)", "chino"),
        ("https://www.scmp.com/rss/91/feed", "South China Morning Post (China)", "chino"),
        ("https://news.google.com/rss/search?q=site:timesofisrael.com+israel&hl=en-US&gl=US&ceid=US:en", "Times of Israel (Proxy)", "occidental"),
        ("https://www.israelhayom.com/feed/", "Israel Hayom (Israel)", "occidental"),
        ("https://news.google.com/rss/search?q=site:ynet.co.il+OR+site:ynetnews.com+israel+OR+iran+OR+gaza+OR+hezbollah&hl=en-US&gl=US&ceid=US:en", "Ynet (Israel)", "occidental"),
        ("https://www.middleeasteye.net/rss", "Middle East Eye", "independiente"),
        ("https://www.al-monitor.com/rss", "Al-Monitor", "independiente"),
        # AGREGADOS ÁFRICA
        ("https://es.africanews.com/feed", "Africanews (África)", "independiente"),
        ("https://news.google.com/rss/search?q=site:jeuneafrique.com+mali+OR+niger+OR+sudan+OR+sahel&hl=fr&gl=FR&ceid=FR:fr", "Jeune Afrique (Proxy Francia)", "occidental"),
        ("https://actualidad.rt.com/rss/africa", "RT África (Rusia)", "alternativo"),
        ("https://news.google.com/rss/search?q=site:aljazeera.com/africa+military+OR+conflict&hl=en-US&gl=US&ceid=US:en", "Al Jazeera África", "independiente"),
        ("https://news.google.com/rss/search?q=site:allafrica.com+military+OR+conflict+OR+sahel&hl=en-US&gl=US&ceid=US:en", "AllAfrica (Proxy)", "independiente"),
        ("https://news.google.com/rss/search?q=site:rfi.fr/es/áfrica+militar+OR+wagner+OR+sahel&hl=es-419&gl=CO&ceid=CO:es-419", "RFI África (Francia)", "occidental"),
        # AGREGADOS LATAM (EJE SOBERANÍA)
        ("https://www.telesurtv.net/rss/rss.xml", "TeleSUR (LatAm)", "resistencia"),
        ("https://actualidad.rt.com/rss/america_latina", "RT LatAm", "alternativo"),
        ("https://news.google.com/rss/search?q=esequibo+OR+malvinas+OR+comando+sur&hl=es-419&gl=CO&ceid=CO:es-419", "Monitor Sur", "independiente")
    ]

def generar_enlaces(titulo, agencia, url_original, bloque):
    botones = {}
    titulo_enc = urllib.parse.quote_plus(titulo)
    
    botones['directo'] = {
        'url': url_original, 'texto': '🔗 ENLACE DIRECTO', 'color': '#00ff41', 'prio': 1
    }
    
    if bloque in ['resistencia', 'alternativo', 'chino']:
        botones['baidu'] = {
            'url': f"https://news.baidu.com/ns?word={urllib.parse.quote(titulo)}&tn=news",
            'texto': '🇨🇳 BUSCAR EN BAIDU', 'color': '#2932e1', 'prio': 2
        }
        botones['sogou'] = {
            'url': f"https://www.sogou.com/web?query={titulo_enc}",
            'texto': '🔍 SOGOU/WECHAT', 'color': '#ff6f00', 'prio': 3
        }
    
    botones['ddg'] = {
        'url': f"https://duckduckgo.com/?q={titulo_enc}&ia=news",
        'texto': '🦆 DUCKDUCKGO', 'color': '#de5833', 'prio': 4
    }
    
    if bloque in ['resistencia', 'alternativo']:
        botones['archive'] = {
            'url': f"https://archive.ph/newest/{url_original}",
            'texto': '🛡️ ARCHIVE.PH', 'color': '#ff4444', 'prio': 5
        }
    
    return dict(sorted(botones.items(), key=lambda x: x[1]['prio']))

def color_y_icono(bloque, agencia):
    if bloque == 'resistencia': return 'red', 'fire'
    elif bloque == 'alternativo': return 'darkred', 'globe'
    elif bloque == 'chino': return 'darkblue', 'star'
    elif bloque == 'occidental': return 'blue' if 'israel' in agencia.lower() else 'orange', 'flag' if 'israel' in agencia.lower() else 'warning-sign'
    else: return 'green', 'info-sign'

def detectar_ciudad(texto):
    texto_lower = texto.lower()
    for ciudad, coords in COORDENADAS_CLAVE.items():
        if ciudad in texto_lower: return coords, ciudad
    return None, None
def generar_mapa_volumen_maximo():
    print(f"\n{'='*70}")
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] RADAR E.T.B. v4.0 - MODO INTEGRAL (REAL-TIME NASA + SIGINT)")
    print(f"{'='*70}")
    
    feeds = obtener_feeds_masivos()
    
    # LISTA COMBINADA DE PALABRAS CLAVE (INCLUYE LATAM Y ÁFRICA)
    palabras_clave = [
        'misil', 'misiles', 'ataque', 'bombardeo', 'dron', 'impacto', 'explosión', 
        'ofensiva', 'sionista', 'resistencia', 'represalia', 'cohete', 'hezbollah',
        'hamas', 'yihad', 'fuerza quds', 'ejército', 'defensa', 'escudo',
        'missile', 'attack', 'strike', 'drone', 'explosion', 'idf', 'airstrike',
        'retaliation', 'militant', 'terrorist', 'rocket', 'intercept', 'iron dome',
        'tension', 'conflict', 'war', 'military', 'naval', 'blockade',
        'tanker', 'vessel', 'ship', 'shipping', 'hormuz', 'barco', 'petrolero',
        'carrier', 'portaaviones', 'destroyer', 'frigate', 'submarine', 'fleet',
        'embargo', 'sanctions', 'oil', 'gas', 'energy',
        'brics', 'multipolar', 'ceasefire', 'truce', 'netanyahu', 'mossad',
        'ayatollah', 'revolutionary guard', 'houthis', 'houthi', 'hutí',
        'palestina', 'palestine', 'gaza', 'cisjordania', 'west bank', 'jerusalem',
        'iran', 'israel', 'lebanon', 'libano', 'syria', 'siria', 'yemen', 'iraq', 'irak',
        # África
        'sahel', 'níger', 'niger', 'malí', 'mali', 'burkina faso',
        'sudán', 'sudan', 'djibouti', 'somalia', 'africom', 'wagner',
        'africa corps', 'cedeao', 'ecowas', 'uranio', 'tuareg', 'jihadist',
        'yihadista', 'mercenary', 'mercenario', 'rsf', 'saf',
        # LatAm (Eje Soberanía)
        'malvinas', 'falkland', 'esequibo', 'comando sur', 'southcom', 'litio', 'soberanía', 'petro', 'milei'
    ]
    
    # Términos específicos para disparar la alerta SIGINT (Capa 3 en vivo)
    terminos_guerra_e = ['spoofing', 'gps', 'jamming', 'interferencia', 'ciberataque', 'hack', 'cibernético']
    
    # Cámara ampliada para ver desde Malvinas hasta Beijing
    mapa = folium.Map(location=[15.0, -10.0], zoom_start=3, tiles='CartoDB dark_matter')
    
    # --- SISTEMA DE CAPAS AVANZADAS ---
    capa_noticias = folium.FeatureGroup(name="📰 CAPA 2: Reportes y Noticias Globales")
    capa_termica = folium.FeatureGroup(name="🔥 CAPA 1: Radiancia Térmica (NASA FIRMS 24h)")
    capa_sigint = folium.FeatureGroup(name="🔮 CAPA 3: Guerra Electrónica (SIGINT en vivo)")
    
    mapa.add_child(capa_noticias)
    mapa.add_child(capa_termica)
    mapa.add_child(capa_sigint)

    # --- LLAMADA AL MOTOR SATELITAL REAL ---
    descargar_termica_nasa(capa_termica)

    # CLÚSTER ASIGNADO A LA CAPA DE NOTICIAS
    cluster_maestro = MarkerCluster(
        name="🛰️ REPORTE GLOBAL UNIFICADO",
        spiderfyOnMaxZoom=True,
        showCoverageOnHover=False,
        zoomToBoundsOnClick=True
    ).add_to(capa_noticias)
    
    total_procesados = 0
    total_filtrados = 0
    feeds_activos = 0
    
    # --- BOT DE CENSURA: Contadores ---
    noticias_occidente = 0
    noticias_resistencia = 0
    
    for idx, (url, agencia, bloque) in enumerate(feeds, 1):
        print(f"[{idx}/{len(feeds)}] 🛰️  {agencia}")
        
        feedparser.USER_AGENT = random.choice(USER_AGENTS)
        if idx > 1: time.sleep(random.uniform(0.5, 1.5))
        
        try:
            flujo = feedparser.parse(url)
            if not flujo.entries: 
                print("      ❌ Feed vacío o bloqueado")
                continue
            
            entradas_feed = len(flujo.entries)
            feeds_activos += 1
            filtrados_feed = 0
            
            # --- IMPRESIÓN DE TELEMETRÍA: ENTRADAS ---
            print(f"      📥 {entradas_feed} entradas detectadas - INICIANDO PROCESAMIENTO TOTAL...")
            
            for entry in flujo.entries:
                try:
                    titulo = entry.get('title', '') or ''
                    descripcion = entry.get('description', '') or ''
                    texto_completo = (titulo + " " + descripcion).lower()
                    total_procesados += 1
                    
                    if not any(p in texto_completo for p in palabras_clave): continue
                    
                    titulo_es = traducir_texto(titulo)
                    if not titulo_es or titulo_es == titulo: titulo_es = titulo[:100]
                    
                    coords, ciudad = detectar_ciudad(texto_completo)
                    
                    if not coords:
                        if bloque == 'resistencia': coords, ciudad = [35.6892, 51.3890], "Teherán"
                        elif bloque == 'alternativo': coords, ciudad = [55.7558, 37.6173], "Moscú"
                        elif bloque == 'chino': coords, ciudad = [39.9042, 116.4074], "Beijing"
                        elif 'israel' in agencia.lower(): coords, ciudad = [32.0853, 34.7818], "Tel Aviv"
                        elif 'naval' in agencia.lower() or 'gCaptain' in agencia: coords, ciudad = [26.56, 56.25], "Estrecho de Ormuz"
                        elif 'africa' in agencia.lower() or 'afrique' in agencia.lower(): coords, ciudad = [14.0, 0.0], "Sahel / África"
                        elif 'latam' in agencia.lower() or 'telesur' in agencia.lower(): coords, ciudad = [4.0, -65.0], "Latinoamérica"
                        else: coords, ciudad = [31.0, 40.0], "Zona de Conflicto"
                    
                    color, icono = color_y_icono(bloque, agencia)
                    url_original = entry.get('link', url)
                    btns = generar_enlaces(titulo_es, agencia, url_original, bloque)
                    
                    # ACTUALIZACIÓN BOT DE CENSURA
                    if bloque == 'occidental': noticias_occidente += 1
                    if bloque in ['resistencia', 'alternativo']: noticias_resistencia += 1

                    # --- DETECTOR SIGINT EN TIEMPO REAL ---
                    if any(termino in texto_completo for termino in terminos_guerra_e):
                        folium.Circle(
                            location=coords, radius=150000, color='#800080', fill=True,
                            fill_color='#800080', fill_opacity=0.35, 
                            popup=f"<div style='width:200px;font-family:Arial;'><b style='color:#800080;'>🔮 ALERTA SIGINT (GUERRA E.)</b><br><small>{titulo_es[:120]}</small></div>"
                        ).add_to(capa_sigint)

                    # --- CONSTRUCCIÓN VISUAL DEL POPUP (FORMATO LIMPIO Y VERTICAL) ---
                    html_btns = "".join([
                        f"<a href='{b['url']}' target='_blank' "
                        f"style='display:block;background:{b['color']};color:{'#000' if b['color']=='#00ff41' else '#fff'};"
                        f"padding:5px;text-decoration:none;font-size:9px;font-weight:bold;margin-top:4px;"
                        f"border-radius:3px;text-align:center;'>{b['texto']}</a>"
                        for b in btns.values()
                    ])
                    
                    popup_html = f"""
                    <div style="width:260px;background:rgba(20,20,20,0.95);padding:10px;border-radius:6px;border:1px solid {color};font-family:Arial;">
                        <div style="background:{color};color:white;padding:4px;font-size:10px;font-weight:bold;text-align:center;border-radius:3px;">
                            {agencia}
                        </div>
                        <div style="font-size:11px;color:#eee;margin:6px 0;line-height:1.3;">
                            {titulo_es[:120]}{'...' if len(titulo_es) > 120 else ''}
                        </div>
                        <div style="font-size:8px;color:#666;text-align:center;margin-bottom:5px;letter-spacing:0.5px;">
                            📍 {ciudad.upper()}
                        </div>
                        {html_btns}
                    </div>
                    """
                    
                    folium.Marker(
                        location=coords, 
                        popup=folium.Popup(popup_html, max_width=270), 
                        icon=folium.Icon(color=color, icon=icono, prefix='glyphicon'), 
                        tooltip=f"{agencia[:18]}: {titulo_es[:32]}..."
                    ).add_to(cluster_maestro)
                    
                    filtrados_feed += 1
                    total_filtrados += 1
                except Exception as e: continue
            
            # --- IMPRESIÓN DE TELEMETRÍA: RESULTADOS ---
            print(f"      ✅ {filtrados_feed} noticias relevantes extraídas")
            
        except Exception as e: 
            print("      ❌ Error crítico en la conexión al feed")
            continue
    
    print(f"\n{'='*70}")
    print("RESUMEN DE INGESTA MASIVA E INTELIGENCIA")
    print(f"{'='*70}")
    print(f"Feeds activos: {feeds_activos}/{len(feeds)}")
    print(f"Noticias relevantes geolocalizadas: {total_filtrados:,}")
    
    # LÓGICA DE ACTIVACIÓN DEL BOT DE CENSURA
    if noticias_resistencia > (noticias_occidente * 1.5):
        print(f"\n[🚨 ALERTA DE CENSURA] Alta actividad del Eje Multipolar ignorada por Occidente.")
        print(f"   (Fuentes Multipolar/Resistencia: {noticias_resistencia} | Fuentes Occidente: {noticias_occidente})")
    
    p_brent, a_gas = obtener_datos_petroleo()
    
    if a_gas > 0: 
        color_dinamico, signo, texto_etiqueta, valor_mostrar = "#ff4444", "+", "PROY. ALZA GASOLINA:", a_gas
    elif a_gas < 0: 
        color_dinamico, signo, texto_etiqueta, valor_mostrar = "#00ff41", "-", "PROY. BAJA GASOLINA:", abs(a_gas)
    else: 
        color_dinamico, signo, texto_etiqueta, valor_mostrar = "#ffcc00", "", "PROY. VARIACIÓN GASOLINA:", 0
        
    leyenda = f"""
    <div style="position:fixed;top:20px;right:20px;width:260px;background:rgba(10,10,10,0.95);border:2px solid #444;padding:15px;border-radius:10px;font-family:'Courier New',monospace;font-size:10px;color:#fff;z-index:9999;">
        <h4 style="color:#00ff41;margin:0 0 10px 0;text-align:center;font-size:13px;">🛰️ RADAR E.T.B. v4.0</h4>
        <div style="border-top:1px solid #333;padding-top:10px;line-height:1.6;">
            <span style="color:#ff4444;">🔴</span> Eje Resistencia (MO+África+LatAm)<br>
            <span style="color:#8b0000;">🔴</span> Rusia/Aliados<br>
            <span style="color:#00008b;">🔵</span> China<br>
            <span style="color:#ffa500;">🟠</span> Occidente<br>
            <span style="color:#32cd32;">🟢</span> Independientes<br>
            <span style="color:#800080;">🟣</span> Capa 3 (Guerra E. / Spoofing)
        </div>
        <div style="margin-top:10px;border-top:1px solid #333;padding-top:8px;color:#888;font-size:9px;">
            Fuentes activas: {feeds_activos}<br>
            Noticias: {total_filtrados:,}<br>
            Actualizado: {datetime.datetime.now().strftime('%H:%M')}
        </div>
    </div>
    """
    mapa.get_root().html.add_child(folium.Element(leyenda))
    
    panel = f"""
    <div style="position:fixed;bottom:30px;left:20px;width:240px;background:rgba(0,0,0,0.95);border:2px solid {color_dinamico};padding:15px;border-radius:10px;z-index:9999;color:#fff;font-family:'Courier New',monospace;">
        <b style="color:#ffcc00;font-size:11px;letter-spacing:1px;">⛽ CENTRO DE ENERGÍA</b>
        <hr style="border:0.5px solid #444;margin:10px 0;">
        <span style="font-size:14px;">BRENT: <b style="color:#fff;">${p_brent:.2f}</b></span><br>
        <span style="font-size:10px;color:{color_dinamico};font-weight:bold;">{texto_etiqueta}</span><br>
        <span style="font-size:20px;color:{color_dinamico};font-weight:bold;">{signo}${valor_mostrar}</span> <small style="font-size:9px;">/gal</small>
    </div>
    """
    mapa.get_root().html.add_child(folium.Element(panel))
    
    # Agregamos el control de capas para encender/apagar la Capa 3 y la Térmica
    folium.LayerControl(collapsed=False).add_to(mapa)
    mapa.save("mapa_multipolar.html")
    
    print(f"\n{'='*70}")
    print(f"[✅ MAPA GENERADO EXITOSAMENTE: mapa_multipolar.html]")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    generar_mapa_volumen_maximo()