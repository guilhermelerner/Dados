import numpy as np

np.random.seed(42)

vendas_diarias = np.random.randint(100, 501, 12)

media_vendas = np.mean(vendas_diarias)
max_vendas = np.max(vendas_diarias)
min_vendas = np.min(vendas_diarias)
total_vendas = np.sum(vendas_diarias)

print(f"Vendas Diarias: {vendas_diarias}")
print(f"Media de Vendas: {media_vendas}")
print(f"Maximo de Vendas: {max_vendas}")
print(f"Minimo de Vendas: {min_vendas}")
print(f"Total de Vendas: {total_vendas}")

matriz_vendas = vendas_diarias.reshape(3, 4)

print("Matriz de Vendas (Semanas x Dias):")
print(matriz_vendas)
