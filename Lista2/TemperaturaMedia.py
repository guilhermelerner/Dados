import numpy as np
temps = np.array([22, 24, 21, 23, 25, 20, 22])
media = np.mean(temps)
dia_quente = np.max(temps)
print(f"Média: {media:.2f}, Máxima: {dia_quente}")