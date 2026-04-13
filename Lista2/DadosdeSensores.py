import numpy as np
leituras = np.random.rand(20)
acima_limite = leituras[leituras > 0.7]
print(f"Leituras > 0.7: {acima_limite}")