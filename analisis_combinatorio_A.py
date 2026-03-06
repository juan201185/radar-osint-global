import math
from collections import Counter

def generar_primos(limite_cantidad):
    """Genera una lista de los primeros N números primos."""
    primos = [2, 3]
    num = 5
    while len(primos) < limite_cantidad:
        es_primo = True
        for p in primos:
            if p * p > num:
                break
            if num % p == 0:
                es_primo = False
                break
        if es_primo:
            primos.append(num)
        num += 2
    return primos

# 1. Generar los primeros 100,000 primos
print("Generando 100,000 primos para el análisis de la topología SNI...")
N_PRIMOS = 100000
lista_primos = generar_primos(N_PRIMOS)

# 2. Calcular A'(X) para cada posición X (empezando desde X=2 para tener X-1 y X-2)
valores_A_prima = []

for X in range(2, N_PRIMOS):
    P_X = lista_primos[X]
    P_X_menos_1 = lista_primos[X-1]
    P_X_menos_2 = lista_primos[X-2]
    
    # TU ECUACIÓN DESPEJADA: A'(X) = P(X) - 2P(X-1) + P(X-2) - 2
    A_prima_X = P_X - 2 * P_X_menos_1 + P_X_menos_2 - 2
    valores_A_prima.append(A_prima_X)

# 3. Análisis Combinatorio y Frecuencias
frecuencias = Counter(valores_A_prima)
total_estados = len(valores_A_prima)

print("\n--- RESULTADOS DEL COLAPSO DISCRETO DE A'(X) ---")
print(f"Total de valores acotados encontrados: {len(frecuencias)}")
print("\nValor A'(X) | Apariciones | Frecuencia Probabilística (%)")
print("---------------------------------------------------------")

# Ordenar los resultados del que más aparece al que menos
for valor, cantidad in frecuencias.most_common():
    porcentaje = (cantidad / total_estados) * 100
    print(f"{valor:>10} | {cantidad:>11} | {porcentaje:>25.4f}%")