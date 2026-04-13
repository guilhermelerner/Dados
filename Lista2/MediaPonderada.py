import numpy as np
notas = [80, 90, 70]
pesos = [0.3, 0.5, 0.2]
media_p = np.average(notas, weights=pesos)