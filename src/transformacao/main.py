# IMPORTAR AS BIBLIOTECAS
import pandas as pd
import sqlite3
from datetime import datetime

# DEFINIR O CAMINHO PARA O ARQUIVO JSONL
df = pd.read_json('../data/data.json') 

# ADICIONAR A COLUNA _SOURCE COM O VALOR FIXO
df['_source'] = "http://lista.mercadolivre.com.br/tenis-corrida-masculino"

# ADICIONAR A COLUNA _DATA_COLETA COM A DATA E HORA ATUAIS
df['_data_coleta'] = datetime.now()

# TRATAR OS VALORES NULOS PARA AS COLUNAS NUMÉRICAS E DE TEXTO
df['old_price_reais'] = df['old_price_reais'].fillna(0).astype(float)
df['old_price_centavos'] = df['old_price_centavos'].fillna(0).astype(float)
df['new_price_reais'] = df['new_price_reais'].fillna(0).astype(float)
df['new_price_centavos'] = df['new_price_centavos'].fillna(0).astype(float)
df['reviews_rating_number'] = df['reviews_rating_number'].fillna(0).astype(float)

#REMOVER OS PARENTESES DA COLUNA  'REVIEWS_AMOUNT'
df['reviews_amount'] = df['reviews_amount'].str.replace('[\(\)]','',regex=True)
df['reviews_amount'] = df['reviews_amount'].fillna(0).astype(int)

# TRATAR OS PREÇOS COMO FLOATS E CALCULAR OS VALORES TOTAIS
df['old_price'] = df['old_price_reais'] + df['old_price_centavos'] / 100
df['new_price'] = df['new_price_reais'] + df['new_price_centavos'] / 100

# REMOVER AS COLUNAS ANTIGAS DE PREÇOS
df.drop(columns=['old_price_reais', 'old_price_centavos','new_price_reais','new_price_centavos'])

# CONECTAR AO BANCO DE DADOS SQLITE (OU CRIAR UM NOVO)
conn = sqlite3.connect('../data/quotes.db')

# SALVAR O DATAFRAME NO BANCO DE DADOS SQLITE
df.to_sql('mercadolivre_itens', conn, if_exists='replace',index=False)

# FECHAR A CONEXÃO COM O BANCO DE DADOS
conn.close()

print(df.head())