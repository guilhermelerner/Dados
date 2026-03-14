import numpy as np

def estatisticas(*args):
    if not args:
        return "Nenhum número fornecido."
    
    dados = np.array(args)
    return {
        "média": np.mean(dados),
        "máximo": np.max(dados),
        "mínimo": np.min(dados)
    }

resultado = estatisticas(10, 20, 30, 40, 50)
print(resultado)