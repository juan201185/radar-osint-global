import pandas as pd
import folium
from folium.plugins import HeatMap
import requests
from io import StringIO
import datetime

# --- CONFIGURACIÓN TÁCTICA ---
# Su clave de la NASA recién obtenida
MAP_KEY = "c7d1ad2cb48cfb61a3b6653a1cf98ea9" 

# Área de vigilancia: Golfo Pérsico y Estrecho de Ormuz
# Formato: Oeste, Sur, Este, Norte
ZONA_VIGILANCIA = "48,23,60,30" 

def obtener_datos_nasa(rango_dias=1):
    """
    Descarga datos de satélite VIIRS (resolución 375m).
    Este sensor es el mejor para detectar incendios pequeños o explosiones.
    """
    url = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{MAP_KEY}/VIIRS_SNPP_NRT/{ZONA_VIGILANCIA}/{rango_dias}"
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Conectando con satélites NASA...")
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            df = pd.read_csv(StringIO(response.text))
            print(f"-> Éxito: {len(df)} puntos térmicos detectados en las últimas {rango_dias*24}h.")
            return df
        else:
            print(f"-> Error de conexión: {response.status_code}")
            return None
    except Exception as e:
        print(f"-> Error inesperado: {e}")
        return None

def generar_mapa_mando():
    # 1. Obtener datos de hoy
    df_hoy = obtener_datos_nasa(1)
    if df_hoy is None or df_hoy.empty:
        print("No se encontraron datos recientes. Intente más tarde.")
        return

    # 2. Crear el mapa con estilo nocturno (CartoDB dark_matter)
    # Centrado en el Estrecho de Ormuz
    mapa = folium.Map(location=[26.5, 54.5], zoom_start=6, tiles='CartoDB dark_matter')

    # 3. Clasificación de puntos
    # Filtramos los puntos de alta confianza o temperatura extrema
    # bright_ti4 > 340 Kelvin suele indicar fuego intenso o explosión
    anomalias = df_hoy[df_hoy['bright_ti4'] > 340]
    puntos_normales = df_hoy[df_hoy['bright_ti4'] <= 340]

    # 4. Agregar "Ruido" térmico (Círculos pequeños naranjas)
    # Representan actividad industrial normal o pozos petroleros
    for _, fila in puntos_normales.iterrows():
        folium.CircleMarker(
            location=[fila['latitude'], fila['longitude']],
            radius=1.5,
            color='#FFA500',
            fill=True,
            opacity=0.4,
            tooltip="Actividad térmica normal (Posible pozo/refinería)"
        ).add_to(mapa)

    # 5. Agregar ALERTAS DE IMPACTO (Iconos de fuego rojo)
    for _, fila in anomalias.iterrows():
        temp_c = round(fila['bright_ti4'] - 273.15, 1)
        info = f"""
        <div style="font-family: Arial; width: 200px;">
            <h4 style="color:red; margin:0;">ALERTA DE ANOMALÍA</h4>
            <hr>
            <b>Lat/Lon:</b> {fila['latitude']}, {fila['longitude']}<br>
            <b>Temp. Sensor:</b> {temp_c}°C<br>
            <b>Hora Satélite:</b> {fila['acq_time']} UTC<br>
            <b>Confianza:</b> {fila['confidence']}<br>
            <p style="font-size:10px; color:gray;">Detectado por Satélite VIIRS SNPP</p>
        </div>
        """
        folium.Marker(
            location=[fila['latitude'], fila['longitude']],
            popup=folium.Popup(info, max_width=250),
            icon=folium.Icon(color='red', icon='fire', prefix='fa')
        ).add_to(mapa)

    # 6. Guardar el mapa
    nombre_archivo = "radar_ataques_real.html"
    mapa.save(nombre_archivo)
    print(f"\n[SISTEMA LISTO]")
    print(f"Mapa generado como: {nombre_archivo}")
    print("Abra el archivo en su navegador para iniciar el análisis.")

if __name__ == "__main__":
    generar_mapa_mando()