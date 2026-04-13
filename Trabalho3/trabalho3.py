import pandas as pd
import mysql.connector
from mysql.connector import Error
import zipfile
import os
import matplotlib.pyplot as plt
import seaborn as sns
import logging
from datetime import datetime
from dotenv import load_dotenv
# --- CONFIGURAÇÕES ---
ARQUIVO_ZIP = "Base_10_anos.zip"
ARQUIVO_CSV_EXTRAIDO = "dados_anac_raw.csv"
ARQUIVO_LOG = "automacao_anac.log"

# Configuração do MySQL 
DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

# Configuração de Logs 
logging.basicConfig(
    filename=ARQUIVO_LOG,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# --- ETAPA 1: EXTRAÇÃO LOCAL ---
def extrair_zip_local():
    logging.info("Iniciando extração do arquivo local...")
    if not os.path.exists(ARQUIVO_ZIP):
        msg = f"Arquivo {ARQUIVO_ZIP} não encontrado na pasta!"
        logging.error(msg)
        print(msg)
        return False

    try:
        with zipfile.ZipFile(ARQUIVO_ZIP, 'r') as zip_ref:
            lista = zip_ref.namelist()
            csv_nome = [f for f in lista if f.lower().endswith('.csv')][0]
            zip_ref.extract(csv_nome)
            
            if os.path.exists(ARQUIVO_CSV_EXTRAIDO): os.remove(ARQUIVO_CSV_EXTRAIDO)
            os.rename(csv_nome, ARQUIVO_CSV_EXTRAIDO)
            
            logging.info(f"Sucesso: {csv_nome} extraído.")
            return True
    except Exception as e:
        logging.error(f"Erro na extração: {e}")
        return False

# --- ETAPA 2: PROCESSAMENTO  ---
def transformar_dados():
    print("Processando dados com Pandas...")
    try:
        df = pd.read_csv(ARQUIVO_CSV_EXTRAIDO, sep=';', encoding='latin1', on_bad_lines='skip', low_memory=False)
        df.columns = df.columns.str.upper().str.replace(' ', '_').str.strip()
        
        mapeamento = {}
        colunas_ja_mapeadas = set()

        # Ordem de prioridade para não repetir nomes
        regras = [
            ('ANO', 'ano'),
            ('MES', 'mes'),
            ('EMPRESA', 'empresa'),
            ('PASSAGEIROS', 'passageiros'),
            ('CARGA', 'carga')
        ]

        for busca, destino in regras:
            for col_original in df.columns:
                if busca in col_original and destino not in colunas_ja_mapeadas:
                    mapeamento[col_original] = destino
                    colunas_ja_mapeadas.add(destino)
                    break 

        df = df.rename(columns=mapeamento)
        
        # Filtra apenas o que mapeamos e remove o resto
        cols_finais = [c for c in ['ano', 'mes', 'empresa', 'passageiros', 'carga'] if c in df.columns]
        df = df[cols_finais].fillna(0)
        
        if 'ano' in df.columns:
            df['ano'] = pd.to_numeric(df['ano'], errors='coerce')
            df = df[df['ano'] >= 2016].copy()

        return df.sample(n=min(5000, len(df)))
    except Exception as e:
        logging.error(f"Erro no processamento: {e}")
        return None

# --- ETAPA 3: CARGA MYSQL ---
def carregar_mysql(df):
    print("Carga no MySQL...")
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS transporte_anac")

        colunas_sql = ", ".join([f"{c} VARCHAR(100)" if c == 'empresa' else f"{c} FLOAT" for c in df.columns])
        cursor.execute(f"CREATE TABLE transporte_anac (id INT AUTO_INCREMENT PRIMARY KEY, {colunas_sql})")

        cols = ", ".join(df.columns)
        placeholders = ", ".join(["%s"] * len(df.columns))
        sql = f"INSERT INTO transporte_anac ({cols}) VALUES ({placeholders})"
        
        cursor.executemany(sql, [tuple(x) for x in df.values])
        conn.commit()
        
        logging.info(f"Sucesso: {cursor.rowcount} registros inseridos.")
    except Error as e:
        if conn: conn.rollback()
        logging.error(f"Falha no MySQL: {e}")
        print(f"Erro no banco: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# --- ETAPA 4: VISUALIZAÇÃO -----
def gerar_visualizacoes(df):
    print("Gerando gráficos para o Moodle...")
    # Padroniza as colunas para maiúsculo
    df.columns = [c.upper() for c in df.columns]
    
    try:
        
        if 'EMPRESA' in df.columns and 'PASSAGEIROS' in df.columns:
            plt.figure(figsize=(10, 8))
            
            # Agrupa por empresa e soma passageiros, pegando as top 5
            top_pax = df.groupby('EMPRESA')['PASSAGEIROS'].sum().nlargest(5)
            
            # Cria o gráfico de pizza
            top_pax.plot(kind='pie', autopct='%1.1f%%', startangle=140, shadow=True, cmap='Paired')
            
            plt.title("Participação das Top 5 Empresas (Volume de Passageiros)")
            plt.ylabel("") # Remove o nome da coluna no eixo Y
            plt.tight_layout()
            
            plt.savefig("grafico_pizza_anac.png")
            print("✔ Gráfico 1: Pizza (Market Share) gerado.")

        # 2. GRÁFICO DE DISPERSÃO 
        if 'PASSAGEIROS' in df.columns and 'CARGA' in df.columns:
            plt.figure(figsize=(10, 6))
            sns.scatterplot(data=df, x='PASSAGEIROS', y='CARGA', hue='ANO', palette='viridis', alpha=0.7)
            plt.title("Dispersão: Relação entre Passageiros e Carga Paga")
            plt.grid(True, linestyle='--', alpha=0.5)
            plt.savefig("grafico_dispersao_anac.png")
            print("✔ Gráfico 2: Scatter Plot gerado.")
            
        plt.close('all')
        
    except Exception as e:
        print(f"⚠ Erro ao gerar os gráficos: {e}")
        # --- BLOCO DE EXECUÇÃO -----
if __name__ == "__main__":
    print(f"--- Pipeline Iniciado: {datetime.now().strftime('%H:%M:%S')} ---")
    
    # 1. Tenta extrair o ZIP
    if extrair_zip_local():
        # 2. Transforma os dados
        dados = transformar_dados()
        
        if dados is not None:
            # 3. Carrega no MySQL
            carregar_mysql(dados)
            
            # 4. Gera os gráficos
            gerar_visualizacoes(dados)
            
            print(f"--- Pipeline Finalizado com Sucesso às {datetime.now().strftime('%H:%M:%S')} ---")
            print("Verifique os arquivos .png e o log na sua pasta.")
        else:
            print("❌ Falha no processamento dos dados.")
    else:
        print("❌ Falha na extração. Verifique se o arquivo Base_10_anos.zip está na pasta.")