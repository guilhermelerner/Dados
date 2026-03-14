import pandas as pd
import io

conteudo_notas = """aluno,matematica,portugues,historia
Ana,8.5,7.0,9.0
Bruno,6.0,7.5,6.5
Carla,9.0,8.0,8.5
Daniel,7.5,6.5,7.0"""

df_notas = pd.read_csv(io.StringIO(conteudo_notas))

estatisticas = df_notas.describe()

print("--- Estatísticas Descritivas ---")
print(estatisticas)