import pandas as pd
import sqlite3
import requests
import zipfile
import os
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Identificador do dataset na API do portal dados.gov.br
DATASET_ID = "voos-e-operacoes-aereas-dados-estatisticos-do-transporte-aereo"
API_URL = f"https://dados.gov.br/api/3/action/package_show?id={DATASET_ID}"

# Arquivos gerados pelo pipeline
ARQUIVO_ZIP = "Base_10_anos.zip"
ARQUIVO_CSV_EXTRAIDO = "dados_anac_raw.csv"
ARQUIVO_JSON = "dados_anac_processados.json"
BANCO_SQL = "pipeline_anac.db"

# Headers para evitar bloqueios de segurança 
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

def buscar_url_via_api():
    """Consulta a API do catálogo de dados para encontrar o link do ZIP de 10 anos"""
    print("--- ETAPA 0: CONSULTA À API ---")
    url_seguranca = "https://www.gov.br/anac/pt-br/assuntos/dados-e-estatisticas/dados-estatisticos/arquivos/Base_10_anos.zip"
    
    try:
        response = requests.get(API_URL, headers=HEADERS, timeout=20)
        if response.status_code == 200:
            recursos = response.json().get('result', {}).get('resources', [])
            for res in recursos:
                if "10 anos" in res.get('name', '') or "Base_10_anos" in res.get('url', ''):
                    print(f"✔ URL localizada via API: {res['url']}")
                    return res['url']
        
        print("⚠ API instável. Usando URL de redundância.")
        return url_seguranca
    except Exception as e:
        print(f"⚠ Falha ao conectar na API ({e}). Usando URL padrão.")
        return url_seguranca

def extrair_e_baixar(url):
    """Realiza o download (streaming) e descompacta o arquivo"""
    print("\n--- ETAPA 1: EXTRAÇÃO (DOWNLOAD E ZIP) ---")
    
    if not os.path.exists(ARQUIVO_ZIP):
        try:
            print("Baixando base de dados (aprox. 14MB)...")
            with requests.get(url, headers=HEADERS, stream=True, timeout=120) as r:
                r.raise_for_status()
                with open(ARQUIVO_ZIP, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=1024*1024): # 1MB chunks
                        f.write(chunk)
            print("✔ Download finalizado.")
        except Exception as e:
            print(f"❌ Erro fatal no download: {e}")
            exit()
    else:
        print(f"✔ Arquivo {ARQUIVO_ZIP} encontrado localmente.")

    # Processo de Extração
    try:
        with zipfile.ZipFile(ARQUIVO_ZIP, 'r') as zip_ref:
            lista = zip_ref.namelist()
            csv_interno = [f for f in lista if f.lower().endswith('.csv')][0]
            zip_ref.extract(csv_interno)
            
            if os.path.exists(ARQUIVO_CSV_EXTRAIDO): os.remove(ARQUIVO_CSV_EXTRAIDO)
            os.rename(csv_interno, ARQUIVO_CSV_EXTRAIDO)
            print(f"✔ CSV '{csv_interno}' extraído com sucesso.")
    except Exception as e:
        print(f"❌ Erro ao manipular o ZIP: {e}")
        exit()

def transformar_dados():
    """Trata o CSV, normaliza colunas, filtra anos e gera JSON"""
    print("\n--- ETAPA 2: TRANSFORMAÇÃO E LIMPEZA ---")
    try:
        # Leitura inicial com separador comum da ANAC ponto e vírgula.
        df = pd.read_csv(ARQUIVO_CSV_EXTRAIDO, sep=';', encoding='latin1', on_bad_lines='skip', low_memory=False)
        
        # Caso o separador seja vírgula.
        if df.shape[1] < 2:
            df = pd.read_csv(ARQUIVO_CSV_EXTRAIDO, sep=',', encoding='latin1', on_bad_lines='skip')

        # Remove espaços e coloca em MAIÚSCULO para evitar KeyErrors
        df.columns = df.columns.str.upper().str.replace(' ', '_').str.strip()

        # Mapeamento dinâmico para garantir que o script ache os dados mesmo com nomes variados
        mapeamento = {
            'PASSAGEIROS_PAGOS': ['PASSAGEIROS_PAGOS', 'PASSAGEIROS_PAGOS_TOTAL', 'PAX_PAGOS'],
            'CARGA_PAGA_KG': ['CARGA_PAGA_KG', 'CARGA_PAGA_(KG)', 'CARGA_PAGA'],
            'ANO': ['ANO', 'ANO_REFERENCIA']
        }

        def encontrar_coluna(alvo, lista_possibilidades):
            for p in lista_possibilidades:
                if p in df.columns: return p
            return None

        col_ano = encontrar_coluna('ANO', mapeamento['ANO'])
        col_pax = encontrar_coluna('PASSAGEIROS_PAGOS', mapeamento['PASSAGEIROS_PAGOS'])
        col_carga = encontrar_coluna('CARGA_PAGA_KG', mapeamento['CARGA_PAGA_KG'])

        # Filtro de 10 anos (2016 - 2026)
        df[col_ano] = pd.to_numeric(df[col_ano], errors='coerce')
        df = df[df[col_ano] >= 2016].copy()

        # Conversão numérica e limpeza de nulos
        df[col_pax] = pd.to_numeric(df[col_pax], errors='coerce').fillna(0)
        df[col_carga] = pd.to_numeric(df[col_carga], errors='coerce').fillna(0)

        # Padronização final das colunas para o JSON e Banco
        df = df.rename(columns={col_ano: 'ANO', col_pax: 'PASSAGEIROS_PAGOS', col_carga: 'CARGA_PAGA_KG'})
        
        # Seleção do Schema Final
        colunas_final = ['ANO', 'MES', 'EMPRESA_SIGLA', 'PASSAGEIROS_PAGOS', 'CARGA_PAGA_KG', 'NATUREZA']
        df_final = df[[c for c in colunas_final if c in df.columns]]

        # Exportação para JSON 
        df_final.to_json(ARQUIVO_JSON, orient='records', indent=4)
        print(f"✔ Transformação concluída. {len(df_final)} registros salvos em JSON.")
        
        return df_final

    except Exception as e:
        print(f"❌ Erro na transformação: {e}")
        exit()

def calcular_e_salvar(df):
    """Cálculos estatísticos, Carga SQL e Visualização"""
    print("\n--- ETAPA 3: ESTATÍSTICAS ---")
    stats = df.groupby('ANO')['PASSAGEIROS_PAGOS'].agg(['mean', 'max', 'min']).reset_index()
    print(stats.to_string(index=False))

    print("\n--- ETAPA 4: BANCO DE DADOS RELACIONAL ---")
    conn = sqlite3.connect(BANCO_SQL)
    df.to_sql('transporte_aereo', conn, if_exists='replace', index=False)
    conn.close()
    print(f"✔ Dados salvos no banco: {BANCO_SQL}")

    print("\n--- ETAPA 5: VISUALIZAÇÕES ---")
    sns.set_theme(style="darkgrid")
    
    # Gráfico 1: Evolução de Passageiros
    plt.figure(figsize=(10, 5))
    df_agrupado = df.groupby('ANO')['PASSAGEIROS_PAGOS'].sum().reset_index()
    sns.lineplot(data=df_agrupado, x='ANO', y='PASSAGEIROS_PAGOS', marker='o', color='teal')
    plt.title('Evolução de Passageiros Pagos (2016-2026)')
    plt.savefig('grafico_evolucao.png')

    # Gráfico 2: Carga por Natureza 
    plt.figure(figsize=(10, 5))
    df_carga = df.groupby(['ANO', 'NATUREZA'])['CARGA_PAGA_KG'].sum().reset_index()
    sns.barplot(data=df_carga, x='ANO', y='CARGA_PAGA_KG', hue='NATUREZA')
    plt.title('Volume de Carga Paga por Tipo de Voo')
    plt.savefig('grafico_carga.png')
    
    print("✔ Gráficos 'grafico_evolucao.png' e 'grafico_carga.png' gerados.")

def main():
    start = datetime.now()
    print(f"PIPELINE EXECUTÁVEL INICIADO EM {start.strftime('%H:%M:%S')}")
    print("="*60)
    
    url = buscar_url_via_api()
    extrair_e_baixar(url)
    dados = transformar_dados()
    calcular_e_salvar(dados)
    
    print("="*60)
    print(f"TRABALHO FINALIZADO COM SUCESSO! Duração: {datetime.now() - start}")

if __name__ == "__main__":
    main()