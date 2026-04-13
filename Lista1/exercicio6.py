import math

def calcular_distancia(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    
    distancia = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distancia

ponto_a = (1, 2)
ponto_b = (4, 6)

resultado = calcular_distancia(ponto_a, ponto_b)
print(f"A distância entre {ponto_a} e {ponto_b} é: {resultado:.2f}")