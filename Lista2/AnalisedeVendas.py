import numpy as np
vendas = np.random.randint(50, 201, size=(3, 4))
total_por_produto = np.sum(vendas, axis=1)
print(f"Total por produto: {total_por_produto}")