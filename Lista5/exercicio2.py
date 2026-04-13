import pandas as pd

dados_relatorio = {
    'Mês': ['Jan', 'Fev', 'Mar', 'Abr'],
    'Receita': [25000, 28000, 22000, 31000],
    'Lucro': [5000, 6500, 4000, 8000]
}
relatorio_anual = pd.DataFrame(dados_relatorio)

dados_brutos = {
    'ID': [101, 102, 103],
    'Produto': ['Placa Mãe', 'Processador', 'Memória RAM'],
    'Qtd': [5, 3, 10]
}
pd.DataFrame(dados_brutos).to_excel('arquivo_existente.xlsx', sheet_name='Dados Brutos', index=False)


print("Executando a Tarefa 1...")
relatorio_anual.to_excel('relatorio.xlsx', sheet_name='Resultados', index=False)
print("-> Arquivo 'relatorio.xlsx' salvo com sucesso com a aba 'Resultados'!\n")


print("Executando a Tarefa 2...")
df_brutos = pd.read_excel('arquivo_existente.xlsx', sheet_name='Dados Brutos')

print("-> Dados carregados do 'arquivo_existente.xlsx':")
print(df_brutos)