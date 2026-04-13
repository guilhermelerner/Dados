import pandas as pd

# Lendo o arquivo com o separador correto
df = pd.read_csv('vendas.csv', sep=';')

# Exibindo o resultado
print(df)