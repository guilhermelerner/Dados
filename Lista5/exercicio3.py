import requests
import pandas as pd

url = 'https://api.dados.exemplo/usuarios'

# Fazendo a requisição GET para a URL da API
resposta = requests.get(url)

# Verificando se a requisição foi bem-sucedida (Status Code 200)
if resposta.status_code == 200:
    # Convertendo a resposta da API para um objeto JSON (lista de dicionários)
    dados_json = resposta.json()
    
    # Transformando o JSON em um DataFrame Pandas
    df_usuarios = pd.DataFrame(dados_json)
    
    print(df_usuarios.head())
else:
    print(f"Erro na requisição. Código de status: {resposta.status_code}")