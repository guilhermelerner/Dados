import pandas as pd
import io

conteudo_experimento = """amostra,ph,temperatura,concentracao
A01,6.8,25.2,0.15
A02,7.1,26.5,0.18
A03,6.5,24.9,0.14
A04,6.9,25.8,0.16"""

df_exp = pd.read_csv(io.StringIO(conteudo_experimento))

print("--- Primeiras linhas (head) ---")
print(df_exp.head(2))

print("\n--- Últimas linhas (tail) ---")
print(df_exp.tail(2))

print("\n--- Resumo estatístico (describe) ---")
print(df_exp.describe())