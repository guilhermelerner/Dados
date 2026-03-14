import pandas as pd
import io
import numpy as np

conteudo_base = """S1,23.5,1012,OK
S2,NA,1015,Falha
S3,24.1,-,OK
S4,22.8,1010,OK
S5,25.0,1011,OK
"""
csv_sensores = "sensor_id,temperatura,pressao,status\n" + (conteudo_base * 10)

leitor = pd.read_csv(io.StringIO(csv_sensores), chunksize=10, na_values=['NA', '-'])

print("Iniciando a análise por blocos...\n")

for i, bloco in enumerate(leitor, 1):

    temp_media = bloco['temperatura'].mean()
    nulos_temp = bloco['temperatura'].isna().sum()
    
    print(f"--- Bloco {i} ---")
    print(f"Temperatura Média: {temp_media:.2f}°C")
    print(f"Valores ausentes em 'temperatura': {nulos_temp}")
    print("-" * 25)