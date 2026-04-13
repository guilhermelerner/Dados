import pandas as pd
import io

conteudo_base = """Monitor,10,799.90
Teclado,25,120.50
Mouse,40,50.00
Webcam,15,250.00
"""
csv_completo = "produto,quantidade,preco_unitario\n" + (conteudo_base * 25)

leitor_blocos = pd.read_csv(io.StringIO(csv_completo), chunksize=20)

print("Iniciando processamento em blocos...\n")

for i, bloco in enumerate(leitor_blocos, 1):
    print(f"--- Bloco {i} ---")
    print(f"Número de linhas no bloco: {len(bloco)}")
    print("3 primeiras linhas do bloco:")
    print(bloco.head(3))
    print("-" * 20)