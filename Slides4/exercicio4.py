import pandas as pd
import io

conteudo_estoque = """item;valor_unitario;peso_kg
Maçã;2,99;0,150
Laranja;1,50;0,200
Banana;4,00;0,120"""

df_estoque = pd.read_csv(io.StringIO(conteudo_estoque), sep=';', decimal=',')

print("Tipos de dados do DataFrame:")
print(df_estoque.dtypes)

print("\nConteúdo do DataFrame:")
print(df_estoque)