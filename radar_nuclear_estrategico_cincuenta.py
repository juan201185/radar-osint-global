# 2. PINTAR DATOS BRUTOS: SENSORES DE RADIACIÓN (CORREGIDO PARA TIEMPO REAL)
        rad_count = 0
        try:
            print("Descargando telemetría de radiación OSINT (Filtro Reciente)...")
            coordenadas_tacticas = [
                (31.7, 35.2), # Israel
                (32.0, 50.0), # Centro Irán
                (24.0, 54.0), # Golfo / Omán
                (39.0, 35.0)  # Turquía
            ]
            
            estaciones = {}
            for lat_base, lon_base in coordenadas_tacticas:
                # --- AQUÍ ESTÁ LA MAGIA: order=captured_at+desc ---
                url_rad = f"https://api.safecast.org/measurements.json?latitude={lat_base}&longitude={lon_base}&distance=1000000&order=captured_at+desc"
                rad_resp = self.session.get(url_rad, timeout=10)
                
                if rad_resp.status_code == 200:
                    data = rad_resp.json()
                    for r in data[:20]: # Toma los 20 más recientes por zona
                        id_est = f"{round(r['latitude'],3)}_{round(r['longitude'],3)}"
                        if id_est not in estaciones:
                            estaciones[id_est] = r
                            # Destacamos si la radiación es peligrosa (> 1.0 uSv/h)
                            es_peligro = float(r['value']) > 1.0
                            color_rad = "red" if es_peligro else "lime"
                            
                            html_rad = f"<div style='width:180px; font-family:monospace;'><b style='color:{color_rad};'>Sensor OSINT</b><hr><b>Valor:</b> {r['value']} {r['unit']}<br><b>Fecha:</b> {r['captured_at'][:10]}<br><b>Hora:</b> {r['captured_at'][11:19]}</div>"
                            
                            folium.CircleMarker(
                                [r['latitude'], r['longitude']], radius=5, color=color_rad, fill=True, fillOpacity=0.8,
                                popup=folium.Popup(html_rad, max_width=200)
                            ).add_to(capa_sensores)
                
            rad_count = len(estaciones)
            if rad_count > 0:
                print(f"-> EXITO: {rad_count} sensores activos y recientes plasmados en el mapa.")
            else:
                print("-> AVISO: Red SafeCast inactiva en la región actualmente (Devolvió 0 datos).")
                
        except Exception as e: print(f"-> Error crítico cargando radiación: {e}")