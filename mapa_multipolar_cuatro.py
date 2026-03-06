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
socket.setdefaulttimeout(12)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
]

# --- DICCIONARIO TÁCTICO GLOBAL ---
COORDENADAS_CLAVE = {
    "tel aviv": [32.0853, 34.7818], "jerusalén": [31.7683, 35.2137],
    "jerusalem": [31.7683, 35.2137], "haifa": [32.7940, 34.9896],
    "gaza": [31.5017, 34.4668], "ashkelon": [31.6693, 34.5715],
    "beersheba": [31.2518, 34.7913], "eilat": [29.5577, 34.9519],
    "rafa": [31.2968, 34.2435], "hebron": [31.5326, 35.0998],
    "teherán": [35.6892, 51.3890], "tehran": [35.6892, 51.3890],
    "isfahán": [32.6539, 51.6660], "shiraz": [29.5918, 52.5837],
    "bandar abbas": [27.1832, 56.2666], "hormuz": [26.56, 56.25],
    "qom": [34.6401, 50.8764], "beirut": [33.8938, 35.5018],
    "damasco": [33.5138, 36.2765], "damascus": [33.5138, 36.2765],
    "alepo": [36.2021, 37.1343], "saná": [15.3694, 44.2045],
    "sanaa": [15.3694, 44.2045], "hodeida": [14.7979, 42.9530],
    "bagdad": [33.3152, 44.3661], "baghdad": [33.3152, 44.3661],
    "erbil": [36.1901, 44.0086], "basora": [30.5081, 47.7835],
    "riad": [24.7136, 46.6753], "doha": [25.2854, 51.5310],
    "dubái": [25.2048, 55.2708], "abu dhabi": [24.4539, 54.3773],
    "kuwait": [29.3759, 47.9774], "estrecho de ormuz": [26.56, 56.25],
    "strait of hormuz": [26.56, 56.25], "mar rojo": [20.0, 38.0],
    "red sea": [20.0, 38.0], "canal de suez": [29.9, 32.5],
    "bab el-mandeb": [12.58, 43.33], "pekín": [39.9042, 116.4074],
    "beijing": [39.9042, 116.4074], "moscú": [55.7558, 37.6173],
    "moscow": [55.7558, 37.6173], "ankara": [39.9334, 32.8597],
    "cairo": [30.0444, 31.2357]
}

def traducir_texto(texto):
    if not texto: return ""
    try:
        if any('\u4e00' <= char <= '\u9fff' for char in texto):
            return GoogleTranslator(source='zh-CN', target='es').translate(texto)
        if any('\u0600' <= char <= '\u06ff' for char in texto):
            return GoogleTranslator(source='ar', target='es').translate(texto)
        return GoogleTranslator(source='auto', target='es').translate(texto)
    except:
        return texto

def obtener_datos_petroleo():
    url = "https://query1.finance.yahoo.com/v8/finance/chart/BZ=F"
    headers = {'User-Agent': random.choice(USER_AGENTS)}
    try:
        resp = requests.get(url, headers=headers, timeout=8)
        precio = resp.json()['chart']['result'][0]['meta']['regularMarketPrice']
        variacion = (precio - 74.0) / 74.0
        alza = int(15600 * (variacion * 0.65))
        return precio, max(0, alza)
    except:
        return 0, 0

def obtener_feeds_optimizados():
    return [
        ("https://www.aljazeera.com/xml/rss/all.xml", "Al Jazeera (Qatar)", "independiente"),
        ("https://actualidad.rt.com/rss", "RT Español (Rusia)", "alternativo"),
        ("https://sputniknews.lat/export/rss2/archive/index.xml", "Sputnik (Rusia)", "alternativo"),
        ("https://www.chinadaily.com.cn/rss/world_rss.xml", "China Daily (China)", "chino"),
        ("http://www.xinhuanet.com/english/rss/worldrss.xml", "Xinhua (China)", "chino"),
        ("https://www.cgtn.com/subscribe/rss/section/world.xml", "CGTN World (China)", "chino"),
        ("https://gcaptain.com/feed/", "gCaptain (Naval/EEUU)", "occidental"),
        ("https://feeds.bbci.co.uk/news/rss.xml", "BBC News (UK)", "occidental"),
        ("https://feeds.bbci.co.uk/mundo/rss.xml", "BBC Mundo (UK)", "occidental"),
        ("http://rss.cnn.com/rss/edition.rss", "CNN (EEUU)", "occidental"),
        ("https://www.jpost.com/Rss/RssFeedsHeadlines.aspx", "Jerusalem Post (Israel)", "occidental"),
        ("https://www.reddit.com/r/worldnews/.rss", "Reddit r/worldnews (Agregador)", "independiente"),
        ("https://www.middleeasteye.net/rss", "Middle East Eye (Independiente)", "independiente"),
        ("https://www.al-monitor.com/rss", "Al-Monitor (Oriente Medio)", "independiente")
    ]

def generar_enlaces(titulo, agencia, url_original, bloque):
    botones = {}
    titulo_enc = urllib.parse.quote_plus(titulo)
    
    botones['directo'] = {'url': url_original, 'texto': '🔗 DIRECTO', 'color': '#00ff41', 'prio': 1}
    
    if bloque in ['resistencia', 'alternativo', 'chino']:
        botones['baidu'] = {'url': f"https://news.baidu.com/ns?word={urllib.parse.quote(titulo)}&tn=news", 'texto': '🇨🇳 BAIDU', 'color': '#2932e1', 'prio': 2}
        botones['sogou'] = {'url': f"https://www.sogou.com/web?query={titulo_enc}", 'texto': '🔍 SOGOU', 'color': '#ff6f00', 'prio': 3}
    
    botones['ddg'] = {'url': f"https://duckduckgo.com/?q={titulo_enc}&ia=news", 'texto': '🦆 DUCKDUCKGO', 'color': '#de5833', 'prio': 4}
    
    if bloque in ['resistencia', 'alternativo']:
        botones['archive'] = {'url': f"https://archive.ph/newest/{url_original}", 'texto': '🛡️ ARCHIVE', 'color': '#ff4444', 'prio': 5}
    
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
        if ciudad in texto_lower:
            return coords, ciudad
    return None, None

def generar_mapa():
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Radar Geopolítico - Evasión Táctica v2.1")
    print("[*] VOLUMEN MASIVO ACTIVADO: Procesando hasta 80 reportes por antena.")
    print("[*] Advertencia: La traducción masiva puede tomar entre 1 y 2 minutos. Procesando...")
    
    feeds = obtener_feeds_optimizados()
    
    palabras_clave = [
        'misil', 'misiles', 'ataque', 'bombardeo', 'dron', 'impacto', 'explosión', 
        'ofensiva', 'sionista', 'resistencia', 'represalia', 'cohete', 'hezbollah',
        'hamas', 'yihad', 'fuerza quds', 'ejército', 'defensa', 'escudo',
        'missile', 'attack', 'strike', 'drone', 'explosion', 'idf', 'airstrike',
        'retaliation', 'militant', 'terrorist', 'rocket', 'intercept', 'iron dome',
        'tension', 'conflict', 'war', 'military', 'naval', 'blockade',
        'tanker', 'vessel', 'ship', 'shipping', 'hormuz', 'barco', 'petrolero',
        'carrier', 'portaaviones', 'destroyer', 'frigate', 'submarine', 'fleet',
        'embargo', 'sanctions', 'oil', 'gas', 'energy', 'brics', 'multipolar',
        'ceasefire', 'truce', 'netanyahu', 'mossad', 'ayatollah', 'houthis',
        'palestina', 'palestine', 'gaza', 'cisjordania', 'west bank', 'jerusalem',
        'iran', 'israel', 'lebanon', 'libano', 'syria', 'siria', 'yemen', 'iraq', 'irak'
    ]
    
    mapa = folium.Map(location=[28.0, 45.0], zoom_start=5, tiles='CartoDB dark_matter')
    
    c_resist = MarkerCluster(name="🔴 Eje Resistencia").add_to(mapa)
    c_oriental = MarkerCluster(name="🔵 Rusia/China").add_to(mapa)
    c_occ = MarkerCluster(name="🟠 Occidente").add_to(mapa)
    c_ind = MarkerCluster(name="🟢 Independientes").add_to(mapa)
    
    impactos = 0
    errores = []
    
    for url, agencia, bloque in feeds:
        print(f"[*] Extrayendo base de datos completa: {agencia}...")
        time.sleep(0.3)
        
        try:
            feedparser.USER_AGENT = random.choice(USER_AGENTS)
            flujo = feedparser.parse(url)
            
            if hasattr(flujo, 'bozo_exception') and flujo.bozo_exception:
                if 'timeout' in str(flujo.bozo_exception).lower():
                    print(f"   [!] Timeout en escudo perimetral")
                    errores.append(f"{agencia}: Timeout")
                    continue
            
            if not flujo.entries:
                print(f"   [!] Antena sin señal o bloqueada")
                errores.append(f"{agencia}: Sin entradas")
                continue
            
            print(f"   [+] {len(flujo.entries)} transmisiones totales detectadas. Filtrando e iniciando traducción pesada...")
            
            # --- AQUÍ ESTÁ EL CAMBIO: AUMENTO DE CAPACIDAD DE 6 a 80 ---
            for entry in flujo.entries[:80]:
                titulo = entry.get('title', '')
                desc = entry.get('description', '')
                texto = (titulo + ' ' + desc).lower()
                
                if not any(p in texto for p in palabras_clave):
                    continue
                
                titulo_es = traducir_texto(titulo)
                coords, ciudad = detectar_ciudad(texto)
                
                if not coords:
                    if bloque == 'resistencia': coords, ciudad = [35.6892, 51.3890], "Teherán"
                    elif bloque == 'alternativo': coords, ciudad = [55.7558, 37.6173], "Moscú"
                    elif bloque == 'chino': coords, ciudad = [39.9042, 116.4074], "Beijing"
                    elif 'israel' in agencia.lower(): coords, ciudad = [32.0853, 34.7818], "Tel Aviv"
                    elif 'naval' in agencia.lower(): coords, ciudad = [26.56, 56.25], "Ormuz"
                    else: coords, ciudad = [31.0, 40.0], "Zona Conflicto"
                
                color, icono = color_y_icono(bloque, agencia)
                url_orig = entry.get('link', url)
                btns = generar_enlaces(titulo_es, agencia, url_orig, bloque)
                
                html_btns = "".join([
                    f"<a href='{b['url']}' target='_blank' style='display:block;background:{b['color']};color:{'#000' if b['color']=='#00ff41' else '#fff'};padding:6px;text-decoration:none;font-size:10px;font-weight:bold;margin-top:5px;border-radius:4px;text-align:center;transition:0.2s;'>{b['texto']}</a>"
                    for b in btns.values()
                ])
                
                popup_html = f"""
                <div style="width:240px;background:rgba(20,20,20,0.95);padding:10px;border-radius:6px;border:1px solid {color};font-family:Arial;">
                    <div style="background:{color};color:white;padding:4px;font-size:11px;font-weight:bold;text-align:center;border-radius:3px;">{agencia}</div>
                    <div style="font-size:12px;color:#eee;margin:8px 0;line-height:1.4;">{titulo_es[:110]}{'...' if len(titulo_es)>110 else ''}</div>
                    <div style="font-size:9px;color:#aaa;text-align:center;margin-bottom:6px;letter-spacing:1px;">📍 {ciudad.upper()}</div>
                    {html_btns}
                </div>
                """
                
                m = folium.Marker(
                    location=coords,
                    popup=folium.Popup(popup_html, max_width=260),
                    icon=folium.Icon(color=color, icon=icono, prefix='glyphicon'),
                    tooltip=f"{agencia[:20]}: {titulo_es[:35]}..."
                )
                
                if bloque == 'resistencia': m.add_to(c_resist)
                elif bloque in ['alternativo', 'chino']: m.add_to(c_oriental)
                elif bloque == 'occidental': m.add_to(c_occ)
                else: m.add_to(c_ind)
                
                impactos += 1
                
        except Exception as e:
            print(f"   [!] Error crítico: {str(e)[:40]}")
            errores.append(f"{agencia}: {str(e)[:30]}")
            continue
    
    folium.LayerControl().add_to(mapa)
    
    p_brent, a_gas = obtener_datos_petroleo()
    color_b = "#ff4444" if a_gas > 500 else "#00ff41"
    
    leyenda = f"""
    <div style="position:fixed;top:20px;right:20px;width:240px;background:rgba(10,10,10,0.95);border:2px solid #444;padding:15px;border-radius:10px;font-family:'Courier New',monospace;font-size:11px;color:#fff;z-index:9999;box-shadow:0 0 15px #000;">
        <h4 style="color:#00ff41;margin:0 0 10px 0;text-align:center;font-size:13px;letter-spacing:1px;">🛰️ RADAR TÁCTICO v2.1</h4>
        <div style="border-top:1px solid #333;padding-top:10px;line-height:1.6;">
            <span style="color:#ff4444;">🔴</span> Eje Resistencia<br>
            <span style="color:#8b0000;">🔴</span> Rusia<br>
            <span style="color:#00008b;">🔵</span> China<br>
            <span style="color:#ffa500;">🟠</span> Occidente<br>
            <span style="color:#32cd32;">🟢</span> Independientes
        </div>
        <div style="margin-top:10px;border-top:1px solid #333;padding-top:8px;color:#888;font-size:10px;">
            Reportes Activos: {impactos}<br>
            Antenas Fallidas: {len(errores)}
        </div>
    </div>
    """
    mapa.get_root().html.add_child(folium.Element(leyenda))
    
    panel = f"""
    <div style="position:fixed;bottom:30px;left:20px;width:220px;background:rgba(0,0,0,0.95);border:2px solid {color_b};padding:15px;border-radius:10px;z-index:9999;color:#fff;font-family:'Courier New',monospace;box-shadow:0 0 15px {color_b};">
        <b style="color:#ffcc00;font-size:12px;letter-spacing:1px;">⛽ CENTRO ENERGÍA E.T.B.</b>
        <hr style="border:0.5px solid #444;margin:10px 0;">
        <span style="font-size:14px;">BRENT: <b style="color:#fff;">${p_brent:.2f}</b></span><br>
        <span style="font-size:11px;color:#ff4444;font-weight:bold;">PROY. GASOLINA:</span><br>
        <span style="font-size:22px;color:#ff4444;font-weight:bold;">+${a_gas}</span> <small style="font-size:10px;">/gal</small>
    </div>
    """
    mapa.get_root().html.add_child(folium.Element(panel))
    
    mapa.save("mapa_multipolar.html")
    
    print(f"\n{'='*60}")
    print(f"✅ BARRIDO TÁCTICO COMPLETADO CON VOLUMEN MASIVO")
    print(f"📊 Impactos procesados: {impactos} | Brent: ${p_brent:.2f} | Alza: +${a_gas}/gal")
    print(f"📁 mapa_multipolar.html sincronizado.")
    if errores:
        print(f"⚠️ Reporte de Bajas ({len(errores)}): {', '.join([e.split(':')[0] for e in errores[:3]])}")
    print(f"{'='*60}")
    
    return impactos

if __name__ == "__main__":
    generar_mapa()