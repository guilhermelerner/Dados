import requests
import os

# Boas práticas de identificação exigidas pela Open Library
HEADERS = {
    "User-Agent": "TrabalhoAcademico_Unicent/1.0 (seu_email@exemplo.com)"
}

def pesquisar_e_salvar_capas(termo_busca):
    url_busca = "https://openlibrary.org/search.json"
    
    parametros = {
        "q": termo_busca,
        "limit": 3 # Limitando a 3 resultados para não baixar muita coisa de uma vez
    }

    # 1. Cria uma pasta chamada 'capas_baixadas' no seu VS Code (se ela não existir)
    pasta_destino = "capas_baixadas"
    os.makedirs(pasta_destino, exist_ok=True)

    print(f"--- Pesquisando por: '{termo_busca}' ---")
    
    try:
        # Faz a requisição de busca
        resposta = requests.get(url_busca, params=parametros, headers=HEADERS)
        resposta.raise_for_status() 
        
        dados = resposta.json()
        livros_encontrados = dados.get('docs', [])

        print(f"Encontrados {len(livros_encontrados)} livros. Baixando imagens...\n")

        for index, livro in enumerate(livros_encontrados):
            nome_livro = livro.get('title', f'livro_desconhecido_{index}')
            autor = livro.get('author_name', ['Autor desconhecido'])[0]
            id_capa = livro.get('cover_i')
            
            print(f"Resultado {index + 1}: {nome_livro} (por {autor})")

            # 2. Se o livro tem um ID de capa, fazemos o download
            if id_capa:
                url_imagem = f"https://covers.openlibrary.org/b/id/{id_capa}-L.jpg"
                
                # Fazendo o GET direto na URL da imagem
                resposta_imagem = requests.get(url_imagem, headers=HEADERS)
                
                if resposta_imagem.status_code == 200:
                    # Limpando o nome do livro para não dar erro no nome do arquivo (tirando barras e dois pontos)
                    nome_arquivo_limpo = nome_livro.replace("/", "_").replace(":", "").replace("\\", "_")
                    caminho_arquivo = os.path.join(pasta_destino, f"{nome_arquivo_limpo}.jpg")
                    
                    # 3. Salvando a imagem no disco 
                    with open(caminho_arquivo, 'wb') as arquivo:
                        arquivo.write(resposta_imagem.content)
                        
                    print(f"  [✓] Capa salva com sucesso em: {caminho_arquivo}")
                else:
                    print("  [x] Erro ao tentar baixar a imagem desta capa.")
            else:
                print("  [-] Imagem da capa não cadastrada na Open Library.")
            print("-" * 50)

    except requests.exceptions.RequestException as e:
        print(f"Ocorreu um erro na requisição: {e}")

# --- Execução do Exemplo ---
if __name__ == "__main__":
   
    pesquisar_e_salvar_capas("Freud")