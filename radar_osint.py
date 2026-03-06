import feedparser
import datetime

def interceptar_comunicaciones_osint():
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Iniciando barrido de frecuencias OSINT...")
    
    # Fuentes de datos
    fuentes_rss = [
        "https://feeds.bbci.co.uk/mundo/rss.xml"
    ]
    
    palabras_clave = [
        'misil', 'misiles', 'irán', 'israel', 'ataque', 
        'bombardeo', 'dron', 'impacto', 'cúpula', 'hezbolá', 'trump'
    ]
    
    print("\n=======================================================")
    print(" 📡 REPORTE TÁCTICO DE IMPACTOS Y ALERTAS (ÚLTIMA HORA)")
    print("=======================================================\n")
    
    alertas_encontradas = 0
    
    for url in fuentes_rss:
        flujo_noticias = feedparser.parse(url)
        
        for entrada in flujo_noticias.entries:
            titulo = entrada.title.lower()
            
            # Usamos .get() también en la descripción por si alguna noticia viene sin ella
            resumen_crudo = entrada.get('description', '')
            resumen = resumen_crudo.lower()
            
            if any(palabra in titulo or palabra in resumen for palabra in palabras_clave):
                print(f"[!] URGENTE: {entrada.title.upper()}")
                print(f"    Resumen: {resumen_crudo}")
                
                # LA CORRECCIÓN: Extracción segura de la hora
                hora_cable = entrada.get('published', entrada.get('updated', 'Hora no reportada por la agencia'))
                print(f"    Hora de intercepción: {hora_cable}")
                
                print(f"    Confirmar fuente: {entrada.link}\n")
                
                alertas_encontradas += 1
                
            if alertas_encontradas >= 5:
                break
                
    if alertas_encontradas == 0:
        print("[*] Radar limpio. Sin reportes masivos en este momento.")

if __name__ == "__main__":
    interceptar_comunicaciones_osint()