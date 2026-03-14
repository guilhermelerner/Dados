import pandas as pd
import io

conteudo_sensores = """sensor_id,temperatura,pressao,status
S1,23.5,1012,OK
S2,NA,1015,Falha
S3,24.1,-,OK
S4,22.8,1010,OK"""

df_sensores = pd.read_csv(io.StringIO(conteudo_sensores), na_values=['NA', '-'])

print("Informações do DataFrame (Contagem de não nulos):")
df_sensores.info()

print("\nConteúdo do DataFrame:")
print(df_sensores)