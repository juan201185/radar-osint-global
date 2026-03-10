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

# --- CONFIGURACIÓN DE RED Y EVASIÓN ---
socket.setdefaulttimeout(20)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0"
]

# --- DICCIONARIO TÁCTICO GLOBAL ---
COORDENADAS_CLAVE = {
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
    "cairo": [30.0444, 31.2357], "el cairo": [30.0444, 31.2357]
}

def traducir_texto(texto):
    if not texto:
        return ""
    try:
        time.sleep(0.5) 
        if any('\u4e00' <= char <= '\u9fff' for char in texto):
            return GoogleTranslator(source='zh-CN', target='es').translate(texto)
        if any('\u0600' <= char <= '\u06ff' for char in texto):
            return GoogleTranslator(source='ar', target='es').translate(texto)
        return GoogleTranslator(source='auto', target='es').translate(texto)
    except Exception as e:
        print(f"      [!] Error traducción: {str(e)[:30]}")
        return texto

def obtener_datos_petroleo():
    """
    Extracción robusta vía CNBC (Bypass Wall Street WAF)
    """
    url_cnbc = "https://quote.cnbc.com/quote-html-webservice/restQuote/symbolType/symbol?symbols=@LCO.1&requestMethod=itv&noform=1&exthrs=1&output=json"
    headers = {'User-Agent': random.choice(USER_AGENTS), 'Accept': 'application/json'}
    
    try:
        respuesta = requests.get(url_cnbc, headers=headers, timeout=10)
        precio = float(respuesta.json()['FormattedQuoteResult']['FormattedQuote'][0]['last'])
        variacion = (precio - 74.0) / 74.0
        alza = int(15600 * (variacion * 0.65))
        return round(precio, 2), max(0, alza)
    except:
        return 0.0, 0

def obtener_feeds_masivos():
    """
    Motor de Ingesta Masiva E.T.B. con Fuentes Purificadas
    """
    return [
        ("https://gcaptain.com/feed/", "gCaptain (Naval)", "occidental"),
        ("https://feeds.bbci.co.uk/mundo/rss.xml", "BBC Mundo (UK)", "occidental"),
        ("https://feeds.bbci.co.uk/news/rss.xml", "BBC News (UK)", "occidental"),
        ("https://news.google.com/rss/search?q=site:elpais.com+oriente+medio+OR+israel+OR+iran&hl=es-419&gl=CO&ceid=CO:es-419", "El País (Proxy)", "occidental"),
        ("https://news.google.com/rss/search?q=source:reuters+middle+east&hl=en-US&gl=US&ceid=US:en", "Reuters (Proxy)", "occidental"),
        ("https://news.google.com/rss/search?q=site:hispantv.com+israel+OR+iran+OR+eeuu+OR+guerra&hl=es-419&gl=CO&ceid=CO:es-419", "HispanTV (Proxy)", "resistencia"),
        ("https://news.google.com/rss/search?q=site:en.irna.ir+israel+OR+iran+OR+military&hl=en-US&gl=US&ceid=US:en", "IRNA (Proxy)", "resistencia"),
        ("https://www.aljazeera.com/xml/rss/all.xml", "Al Jazeera (Qatar)", "independiente"),
        ("https://actualidad.rt.com/rss", "RT (Rusia)", "alternativo"),
        ("https://sputniknews.lat/export/rss2/archive/index.xml", "Sputnik (Rusia)", "alternativo"),
        ("https://news.google.com/rss/search?q=site:spanish.news.cn+israel+OR+iran+OR+oriente&hl=es-419&gl=CO&ceid=CO:es-419", "Xinhua (Proxy)", "chino"),
        
        # --- SUSTITUCIÓN TÁCTICA: SCMP EN LUGAR DE GLOBAL TIMES ---
        ("https://www.scmp.com/rss/91/feed", "South China Morning Post (China)", "chino"),
        
        ("https://news.google.com/rss/search?q=site:timesofisrael.com+israel&hl=en-US&gl=US&ceid=US:en", "Times of Israel (Proxy)", "occidental"),
        
        # --- SUSTITUCIÓN TÁCTICA: ISRAEL HAYOM EN LUGAR DE JPOST ---
        ("https://www.israelhayom.com/feed/", "Israel Hayom (Israel)", "occidental"),
        
        ("https://www.middleeasteye.net/rss", "Middle East Eye", "independiente"),
        ("https://www.al-monitor.com/rss", "Al-Monitor", "independiente"),
    ]

def generar_enlaces(titulo, agencia, url_original, bloque):
    botones = {}
    titulo_enc = urllib.parse.quote_plus(titulo)
    
    botones['directo'] = {
        'url': url_original,
        'texto': '🔗 ENLACE DIRECTO',
        'color': '#00ff41',
        'prio': 1
    }
    
    if bloque in ['resistencia', 'alternativo', 'chino']:
        botones['baidu'] = {
            'url': f"https://news.baidu.com/ns?word={urllib.parse.quote(titulo)}&tn=news",
            'texto': '🇨🇳 BUSCAR EN BAIDU',
            'color': '#2932e1',
            'prio': 2
        }
        botones['sogou'] = {
            'url': f"https://www.sogou.com/web?query={titulo_enc}",
            'texto': '🔍 SOGOU/WECHAT',
            'color': '#ff6f00',
            'prio': 3
        }
    
    botones['ddg'] = {
        'url': f"https://duckduckgo.com/?q={titulo_enc}&ia=news",
        'texto': '🦆 DUCKDUCKGO',
        'color': '#de5833',
        'prio': 4
    }
    
    if bloque in ['resistencia', 'alternativo']:
        botones['archive'] = {
            'url': f"https://archive.ph/newest/{url_original}",
            'texto': '🛡️ ARCHIVE.PH',
            'color': '#ff4444',
            'prio': 5
        }
    
    return dict(sorted(botones.items(), key=lambda x: x[1]['prio']))

def color_y_icono(bloque, agencia):
    if bloque == 'resistencia':
        return 'red', 'fire'
    elif bloque == 'alternativo':
        return 'darkred', 'globe'
    elif bloque == 'chino':
        return 'darkblue', 'star'
    elif bloque == 'occidental':
        return 'blue' if 'israel' in agencia.lower() else 'orange', 'flag' if 'israel' in agencia.lower() else 'warning-sign'
    else:
        return 'green', 'info-sign'

def detectar_ciudad(texto):
    texto_lower = texto.lower()
    for ciudad, coords in COORDENADAS_CLAVE.items():
        if ciudad in texto_lower:
            return coords, ciudad
    return None, None

def generar_mapa_volumen_maximo():
    print(f"\n{'='*70}")
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] RADAR E.T.B. - MODO INGESTA MASIVA")
    print(f"{'='*70}")
    print("[*] Configuración: Volumen extremo + Evasión activa + Dispersión Táctica")
    print("[*] Objetivo: Procesar 100% de noticias disponibles sin apilamiento")
    print(f"{'='*70}\n")
    
    feeds = obtener_feeds_masivos()
    
    palabras_clave = [
        'misil', 'misiles', 'ataque', 'bombardeo', 'dron', 'impacto', 'explosión', 
        'ofensiva', 'sionista', 'resistencia', 'represalia', 'cohete', 'hezbollah',
        'hamas', 'yihad', 'fuerza quds', 'ejército', 'defensa', 'escudo',
        'missile', 'attack', 'strike', 'drone', 'explosion', 'idf', 'airstrike',
        'retaliation', 'militant', 'terrorist', 'rocket', 'intercept', 'iron dome',
        'tension', 'conflict', 'war', 'military', 'naval', 'blockade',
        'tanker', 'vessel', 'ship', 'shipping', 'hormuz', 'barco', 'petrolero',
        'carrier', 'portaaviones', 'destroyer', 'frigate', 'submarine', 'fleet',
        'blockade', 'embargo', 'sanctions', 'oil', 'gas', 'energy',
        'brics', 'multipolar', 'ceasefire', 'truce', 'netanyahu', 'mossad',
        'ayatollah', 'revolutionary guard', 'houthis', 'houthi', 'hutí',
        'palestina', 'palestine', 'gaza', 'cisjordania', 'west bank', 'jerusalem',
        'iran', 'israel', 'lebanon', 'libano', 'syria', 'siria', 'yemen', 'iraq', 'irak'
    ]
    
    mapa = folium.Map(
        location=[30.0, 40.0],
        zoom_start=5,
        tiles='CartoDB dark_matter'
    )
    
    c_resistencia = MarkerCluster(name="🔴 Eje Resistencia (Irán/Aliados)").add_to(mapa)
    c_oriental = MarkerCluster(name="🔵 Eje Oriental (Rusia/China)").add_to(mapa)
    c_occidente = MarkerCluster(name="🟠 Bloque Occidental").add_to(mapa)
    c_independiente = MarkerCluster(name="🟢 Medios Independientes").add_to(mapa)
    
    total_procesados = 0
    total_filtrados = 0
    errores = []
    feeds_activos = 0
    
    for idx, (url, agencia, bloque) in enumerate(feeds, 1):
        print(f"[{idx}/{len(feeds)}] 🛰️  {agencia}")
        
        feedparser.USER_AGENT = random.choice(USER_AGENTS)
        
        if idx > 1:
            pausa = random.uniform(0.5, 1.5)
            time.sleep(pausa)
        
        try:
            flujo = feedparser.parse(url)
            
            if hasattr(flujo, 'bozo_exception') and flujo.bozo_exception:
                error_str = str(flujo.bozo_exception).lower()
                if 'timeout' in error_str or 'temporary failure' in error_str:
                    print(f"      ⚠️  Timeout de red - reintentando...")
                    feedparser.USER_AGENT = random.choice(USER_AGENTS)
                    time.sleep(2)
                    flujo = feedparser.parse(url)
            
            if not flujo.entries:
                print(f"      ❌ Feed vacío o bloqueado")
                errores.append(f"{agencia}: Sin entradas")
                continue
            
            entradas_feed = len(flujo.entries)
            feeds_activos += 1
            print(f"      📥 {entradas_feed} entradas detectadas - INICIANDO PROCESAMIENTO TOTAL...")
            
            filtrados_feed = 0
            
            for entry in flujo.entries:
                try:
                    titulo = entry.get('title', '') or ''
                    descripcion = entry.get('description', '') or ''
                    texto_completo = (titulo + " " + descripcion).lower()
                    
                    total_procesados += 1
                    
                    if not any(p in texto_completo for p in palabras_clave):
                        continue
                    
                    titulo_es = traducir_texto(titulo)
                    if not titulo_es or titulo_es == titulo:
                        titulo_es = titulo[:100] if len(titulo) > 100 else titulo
                    
                    coords, ciudad = detectar_ciudad(texto_completo)
                    ciudad_exacta = bool(coords)
                    
                    if not coords:
                        if bloque == 'resistencia':
                            coords, ciudad = [35.6892, 51.3890], "Teherán"
                        elif bloque == 'alternativo':
                            coords, ciudad = [55.7558, 37.6173], "Moscú"
                        elif bloque == 'chino':
                            coords, ciudad = [39.9042, 116.4074], "Beijing"
                        elif 'israel' in agencia.lower():
                            coords, ciudad = [32.0853, 34.7818], "Tel Aviv"
                        elif 'naval' in agencia.lower() or 'gCaptain' in agencia:
                            coords, ciudad = [26.56, 56.25], "Estrecho de Ormuz"
                        else:
                            coords, ciudad = [31.0, 40.0], "Zona de Conflicto"
                    
                    # --- ALGORITMO DE DISPERSIÓN TÁCTICA ---
                    # Desapilamiento de coordenadas para no ocultar noticias
                    radio = 0.05 if ciudad_exacta else 2.5
                    lat_dispersion = coords[0] + random.uniform(-radio, radio)
                    lon_dispersion = coords[1] + random.uniform(-radio, radio)
                    coords_finales = [lat_dispersion, lon_dispersion]
                    
                    color, icono = color_y_icono(bloque, agencia)
                    url_orig = entry.get('link', url)
                    btns = generar_enlaces(titulo_es, agencia, url_orig, bloque)
                    
                    html_btns = "".join([
                        f"<a href='{b['url']}' target='_blank' style='display:block;background:{b['color']};color:{'#000' if b['color']=='#00ff41' else '#fff'};padding:5px;text-decoration:none;font-size:9px;font-weight:bold;margin-top:4px;border-radius:3px;text-align:center;'>{b['texto']}</a>"
                        for b in btns.values()
                    ])
                    
                    popup_html = f"""
                    <div style="width:260px;background:rgba(20,20,20,0.95);padding:10px;border-radius:6px;border:1px solid {color};font-family:Arial;">
                        <div style="background:{color};color:white;padding:4px;font-size:10px;font-weight:bold;text-align:center;border-radius:3px;">{agencia}</div>
                        <div style="font-size:11px;color:#eee;margin:6px 0;line-height:1.3;">{titulo_es[:120]}{'...' if len(titulo_es) > 120 else ''}</div>
                        <div style="font-size:8px;color:#666;text-align:center;margin-bottom:5px;letter-spacing:0.5px;">📍 {ciudad.upper()}</div>
                        {html_btns}
                    </div>
                    """
                    
                    marcador = folium.Marker(
                        location=coords_finales,  # Usamos las coordenadas esparcidas
                        popup=folium.Popup(popup_html, max_width=270),
                        icon=folium.Icon(color=color, icon=icono, prefix='glyphicon'),
                        tooltip=f"{agencia[:18]}: {titulo_es[:32]}..."
                    )
                    
                    if bloque == 'resistencia':
                        marcador.add_to(c_resistencia)
                    elif bloque in ['alternativo', 'chino']:
                        marcador.add_to(c_oriental)
                    elif bloque == 'occidental':
                        marcador.add_to(c_occidente)
                    else:
                        marcador.add_to(c_independiente)
                    
                    filtrados_feed += 1
                    total_filtrados += 1
                    
                except Exception as e:
                    continue
            
            print(f"      ✅ {filtrados_feed} noticias relevantes extraídas")
            
        except Exception as e:
            print(f"      ❌ Error crítico: {str(e)[:50]}")
            errores.append(f"{agencia}: {str(e)[:40]}")
            continue
    
    print(f"\n{'='*70}")
    print("RESUMEN DE INGESTA MASIVA")
    print(f"{'='*70}")
    print(f"Feeds activos: {feeds_activos}/{len(feeds)}")
    print(f"Total entradas procesadas: {total_procesados:,}")
    print(f"Noticias relevantes geolocalizadas: {total_filtrados:,}")
    print(f"Tasa de filtrado: {(total_filtrados/total_procesados*100):.1f}%" if total_procesados > 0 else "N/A")
    if errores:
        print(f"Feeds con problemas: {len(errores)}")
    
    # OBTENER DATOS DE PETRÓLEO
    print(f"\n[*] Obteniendo datos energéticos...")
    p_brent, a_gas = obtener_datos_petroleo()
    
    if p_brent == 0:
        print(f"   [!] Error de conexión. Mostrando $0.00")
        
    # --- LÓGICA DINÁMICA REAL PARA EL PANEL ---
    if a_gas > 0:
        color_dinamico = "#ff4444"  # Rojo (Alza)
        signo = "+"
        texto_etiqueta = "PROY. ALZA GASOLINA:"
        valor_mostrar = a_gas
    elif a_gas < 0:
        color_dinamico = "#00ff41"  # Verde (Baja)
        signo = "-"
        texto_etiqueta = "PROY. BAJA GASOLINA:"
        valor_mostrar = abs(a_gas)
    else:
        color_dinamico = "#ffcc00"  # Amarillo (Estable)
        signo = ""
        texto_etiqueta = "PROY. VARIACIÓN GASOLINA:"
        valor_mostrar = 0
        
    print(f"   [✓] Brent: ${p_brent:.2f} | {texto_etiqueta} {signo}${valor_mostrar}/gal")
    
    leyenda = f"""
    <div style="position:fixed;top:20px;right:20px;width:260px;background:rgba(10,10,10,0.95);border:2px solid #444;padding:15px;border-radius:10px;font-family:'Courier New',monospace;font-size:10px;color:#fff;z-index:9999;">
        <h4 style="color:#00ff41;margin:0 0 10px 0;text-align:center;font-size:13px;">🛰️ RADAR E.T.B.</h4>
        <div style="border-top:1px solid #333;padding-top:10px;line-height:1.6;">
            <span style="color:#ff4444;">🔴</span> Eje Resistencia<br>
            <span style="color:#8b0000;">🔴</span> Rusia/Aliados<br>
            <span style="color:#00008b;">🔵</span> China<br>
            <span style="color:#ffa500;">🟠</span> Occidente<br>
            <span style="color:#32cd32;">🟢</span> Independientes
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
    
    folium.LayerControl(collapsed=False).add_to(mapa)
    mapa.save("mapa_multipolar.html")
    
    print(f"\n{'='*70}")
    print(f"[✅ MAPA GENERADO: mapa_multipolar.html]")
    print(f"   Brent: ${p_brent:.2f} | {texto_etiqueta} {signo}${valor_mostrar}/gal")
    print(f"{'='*70}\n")
    
    return total_filtrados

if __name__ == "__main__":
    generar_mapa_volumen_maximo()