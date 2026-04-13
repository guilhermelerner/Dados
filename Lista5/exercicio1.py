import pandas as pd

# Carregando o arquivo CSV com os parâmetros especificados
df_vendas = pd.read_csv(
    'vendas.csv',
    header=None,      
    index_col=0,       
    na_values=['ND']   
)

# Exibindo as primeiras linhas para conferência
print(df_vendas.head())