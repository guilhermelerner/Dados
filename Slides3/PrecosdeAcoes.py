import numpy as np
precos = np.array([120.50, 121.00, 119.80, 122.30, 120.00])
variacao = np.diff(precos) / precos[:-1] * 100
print(f"Variações diárias (%): {variacao}")