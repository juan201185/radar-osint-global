#!/bin/bash
echo "=== INICIANDO BARRIDO TÁCTICO TOTAL - CENTRO DE MANDO E.T.B. ==="

# Fila 1: CONFLICTO ACTIVO
echo "[1/11] Radar Multipolar (Noticias)..."
python3 mapa_multipolar.py

echo "[2/11] Radar Regional Medio Oriente (Explosiones NASA)..."
python3 vigilancia_regional_medio_oriente.py

echo "[3/11] Radar Movimiento de Tropas (Despliegues terrestres)..."
python3 radar_movimiento_tropas.py

# Fila 2: LOGÍSTICA Y SUMINISTRO
echo "[4/11] Radar Logístico Atlántico (Puente aéreo)..."
python3 puente_aereo.py

echo "[5/11] Radar Marítimo Rojo (Bloqueo Houthi)..."
python3 radar_maritimo_rojo.py

echo "[6/11] Radar Financiero de Guerra (Petróleo/Sanciones)..."
python3 radar_financiero_guerra.py

# Fila 3: AMENAZAS ESTRATÉGICAS
echo "[7/11] Radar Nuclear Estratégico..."
python3 radar_nuclear_estrategico.py

echo "[8/11] Radar Ciber Guerra..."
python3 radar_ciber_guerra.py

echo "[9/11] Radar Guerra Informacional..."
python3 radar_guerra_info.py

# Fila 4: HUMANITARIO
echo "[10/11] Radar Humanitario Crisis..."
python3 radar_humanitario_crisis.py

# Sincronización
echo "[11/11] Sincronizando Matriz con GitHub..."
git add .
git commit -m "Actualización Centro Mando E.T.B. - $(date '+%Y-%m-%d %H:%M')"
git push

echo "=== ¡CENTRO DE MANDO E.T.B. 100% ACTUALIZADO! ==="