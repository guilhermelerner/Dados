import pandas as pd
import io

dados_csv = """data,temperatura_c,umidade_relativa
2023-03-01,28.5,75
2023-03-02,30.1,80
2023-03-03,27.9,70"""

df_clima = pd.read_csv(io.StringIO(dados_csv), parse_dates=['data'], index_col='data')

print("Informações do DataFrame:")
df_clima.info()

print("\nConteúdo do DataFrame:")
print(df_clima)