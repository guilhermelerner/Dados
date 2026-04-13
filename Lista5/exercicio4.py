import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('sqlite:///meu_banco.db')

df_produtos = pd.read_sql_table('produtos', con=engine)

print(df_produtos.head())