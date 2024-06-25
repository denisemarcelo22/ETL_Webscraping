# IMPORTAR AS BIBLIOTECAS
import pandas as pd
import sqlite3
import datetime

# DEFINIR O CAMINHO PARA O ARQUIVO JSONL
df = pd.read_json('../data/data.jsonl', lines=True)

# ADICIONAR A COLUNA _SOURCE COM O VALOR FIXO
df['_source'] = "http://lista.mercadolivre.com.br/tenis-corrida-masculino"

# ADICIONAR A COLUNA _DATA_COLETA COM A DATA E HORA ATUAIS
df['_data_coleta'] = datetime.now()

print(df)
