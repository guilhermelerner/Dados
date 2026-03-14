import numpy as np

matriz_aleatoria = np.random.randint(1, 101, size=(5, 5))

print(matriz_aleatoria)

soma_colunas = np.sum(matriz_aleatoria, axis=0)

print(soma_colunas)

max_por_linha = np.max(matriz_aleatoria, axis=1)

print(max_por_linha)
