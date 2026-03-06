import pandas as pd
import pdfplumber
import os

# CONFIGURACIÓN DE ARCHIVOS
pdfs = ["018-22.pdf", "036-23.pdf", "003-24.pdf", "008-25.pdf"]
csv_masacres = "base_datos_patia_2021_2026.csv"
csv_lideres = "lideres_caracterizados_cauca.csv"

def extraer_texto_pdfs(lista_pdfs):
    print("📖 Extrayendo conocimiento de los informes de la Defensoría...")
    biblioteca_texto = {}
    for pdf_p in lista_pdfs:
        if os.path.exists(pdf_p):
            with pdfplumber.open(pdf_p) as doc:
                texto_completo = ""
                for pagina in doc.pages:
                    texto_completo += (pagina.extract_text() or "")
                biblioteca_texto[pdf_p] = texto_completo
    return biblioteca_texto

def ejecutar_cruce():
    # 1. Cargar textos de PDFs
    textos = extraer_texto_pdfs(pdfs)
    
    # 2. Cargar CSVs
    df_l = pd.read_csv(csv_lideres)
    df_m = pd.read_csv(csv_masacres)
    
    print("🔍 Buscando correlaciones (Cruce de Inteligencia)...")

    # Función para buscar coincidencias
    def buscar_en_alertas(fila):
        lugar = str(fila['municipio'])
        nombre = str(fila.get('nombre_victima', ''))
        coincidencias = []
        
        for nombre_pdf, contenido in textos.items():
            # Si el lugar o el nombre aparecen en el PDF
            if lugar.lower() in contenido.lower() or (nombre != '' and nombre.lower() in contenido.lower()):
                coincidencias.append(nombre_pdf)
        
        return ", ".join(coincidencias) if coincidencias else "SIN_ALERTA_DETECTADA"

    # Aplicar el cruce a líderes y masacres
    df_l['alerta_previa'] = df_l.apply(buscar_en_alertas, axis=1)
    df_m['alerta_previa'] = df_m.apply(buscar_en_alertas, axis=1)

    # 3. Guardar resultados finales
    df_l.to_csv("RESULTADO_LIDERES_ALERTA.csv", index=False)
    df_m.to_csv("RESULTADO_MASACRES_ALERTA.csv", index=False)
    
    print("✅ Proceso completado.")
    print(f"📊 Se analizaron {len(df_l)} líderes y {len(df_m)} masacres.")
    print("📂 Archivos generados: RESULTADO_LIDERES_ALERTA.csv y RESULTADO_MASACRES_ALERTA.csv")

if __name__ == "__main__":
    ejecutar_cruce()