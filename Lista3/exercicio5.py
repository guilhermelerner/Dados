import pandas as pd
import io

conteudo_transacoes = """id_transacao,valor,moeda
1,1.250.00,BRL
2,3.500.50,BRL
3,999.99,USD"""

df_transacoes = pd.read_csv(io.StringIO(conteudo_transacoes), thousands='.', decimal='.')

print("Tipos de dados:")
print(df_transacoes.dtypes)
print(f"\nMédia dos valores: {df_transacoes['valor'].mean():.2f}")
print("\nConteúdo do DataFrame:")
print(df_transacoes)