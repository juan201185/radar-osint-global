import feedparser
import folium
import datetime

# --- 1. DICCIONARIO DE GEOCODIFICACIÓN TÁCTICA ---
# Mapeamos las ciudades clave del conflicto a sus coordenadas [Latitud, Longitud]
COORDENADAS_CLAVE = {
    "teherán": [35.6892, 51.3890],
    "isfahán": [32.6539, 51.6660],
    "tel aviv": [32.0853, 34.7818],
    "jerusalén": [31.7683, 35.2137],
    "haifa": [32.7940, 34.9896],
    "gaza": [31.5017, 34.4668],
    "beirut": [33.8938, 35.5018],
    "damasco": [33.5138, 36.2765],
    "bagdad": [33.3152, 44.3661],
    "saná": [15.3694, 44.2045], # Capital de Yemen (Hutíes)
    "dubái": [25.2048, 55.2708]
}

def generar_mapa_noticias():
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Escaneando agencias de noticias y geocodificando impactos...")
    
    # Fuentes RSS (Puede agregar más como Reuters o EFE si consigue los links)
    fuentes_rss = [
        "https://feeds.bbci.co.uk/mundo/rss.xml",
        "https://elpais.com/rss/internacional.xml" # Añadimos El País para más cobertura
    ]
    
    palabras_ataque = ['misil', 'misiles', 'ataque', 'bombardeo', 'dron', 'impacto', 'explosión', 'ofensiva']
    
    # Creamos el mapa centrado en el Medio Oriente
    mapa_osint = folium.Map(location=[32.0, 44.0], zoom_start=5, tiles='CartoDB dark_matter')
    
    impactos_mapeados = 0

    for url in fuentes_rss:
        try:
            flujo_noticias = feedparser.parse(url)
        except Exception as e:
            print(f"Error al conectar con {url}: {e}")
            continue
            
        for entrada in flujo_noticias.entries:
            titulo = entrada.title.lower()
            resumen_crudo = entrada.get('description', '')
            resumen = resumen_crudo.lower()
            
            # 1er Filtro: ¿Habla de un ataque?
            if any(palabra in titulo or palabra in resumen for palabra in palabras_ataque):
                
                # 2do Filtro: ¿Menciona alguna ciudad de nuestro diccionario?
                for ciudad, coords in COORDENADAS_CLAVE.items():
                    if ciudad in titulo or ciudad in resumen:
                        
                        hora_cable = entrada.get('published', entrada.get('updated', 'Hora desconocida'))
                        
                        # Armamos la tarjeta de información para el mapa
                        info_html = f"""
                        <div style="font-family: Arial; width: 250px;">
                            <b style="color:#ffcc00; font-size: 14px;">REPORTE DE AGENCIA: {ciudad.upper()}</b><br>
                            <hr style="border: 1px solid gray;">
                            <b>Titular:</b> {entrada.title}<br><br>
                            <span style="font-size: 11px; color: #cccccc;">{resumen_crudo}</span><br><br>
                            <b>Hora:</b> <span style="color: #66b3ff;">{hora_cable}</span><br>
                            <a href="{entrada.link}" target="_blank" style="color: #ff6666;">[Leer cable original]</a>
                        </div>
                        """
                        
                        # Ponemos un marcador especial (un megáfono o periódico)
                        folium.Marker(
                            location=coords,
                            popup=folium.Popup(info_html, max_width=300),
                            icon=folium.Icon(color='orange', icon='info-sign'),
                            tooltip=f"Reporte en {ciudad.title()}"
                        ).add_to(mapa_osint)
                        
                        impactos_mapeados += 1
                        print(f"[+] Mapeado impacto reportado en: {ciudad.title()}")
                        
                        # Evitamos poner múltiples marcadores por la misma noticia en distintas ciudades
                        break 

    # Guardamos el mapa
    archivo_salida = "mapa_osint_noticias.html"
    mapa_osint.save(archivo_salida)
    
    print(f"\n[SISTEMA LISTO] Se han geocodificado {impactos_mapeados} reportes.")
    print(f"Abra el archivo '{archivo_salida}' en su navegador.")

if __name__ == "__main__":
    generar_mapa_noticias()