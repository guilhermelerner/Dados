import sqlite3 

import pandas as pd

# Conectar ao banco
con = sqlite3.connect("mydata.sqlite")

# Criar tabela
con.execute("""
CREATE TABLE IF NOT EXISTS test (
    id INTEGER,
    nome TEXT
)
""")

# Inserir dados
con.execute("INSERT INTO test (id, nome) VALUES (1, 'Ana')")
con.execute("INSERT INTO test (id, nome) VALUES (2, 'Guilherme')")

# Salvar alterações
con.commit()

# Consultar dados
cursor = con.execute("SELECT * FROM test")
rows = cursor.fetchall()

# Converter para DataFrame
df = pd.DataFrame(rows, columns=[x[0] for x in cursor.description])

print(df)

# Fechar conexão
con.close()