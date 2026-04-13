import sqlalchemy as sqla
import pandas as pd

engine = sqla.create_engine("sqlite:///novo_banco.sqlite")

with engine.connect() as conn:
    conn.execute(sqla.text("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY,
            nome TEXT,
            idade INTEGER
        )
        """))
with  engine.connect() as conn:
    conn.execute(sqla.text("""
        INSERT INTO usuarios (nome, idade)
        VALUES ('Ana', 23), ('Guilherme', 21)
    """))
    conn.commit()
df = pd.read_sql("SELECT * FROM usuarios", engine)
print (df)