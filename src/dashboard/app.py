import streamlit as st
import pandas as pd
import sqlite3

# CONECTAR AO BANCO DE DADOS SQLLITE
conn = sqlite3.connect('../data/quotes.db')

# CARREGAR OS DADOS DA TABELA 'MERCADOLIVRE_ITEMS' EM UM DATAFRAME PANDAS
df = pd.read_sql_query("SELECT * FROM mercadolivre_itens", conn)

# FECHAR A CONEXÃO COM O BANCO DE DADOS
conn.close()

# TÍTULO DA APLICAÇÃO
st.title('Pesquisa de mercado - Tênis esportivo no Mercado livre')

# MELHORAR O LAYOUT COM COLUNAS PARA KPI'S
st.subheader('KPIs principais do sistema')
col1, col2, col3 = st.columns(3)

# KPI 1: NÚMERO TOTAL DE ITENS
total_itens = df.shape[0]
col1.metric(label = "Número total de itens", value=total_itens)

# KPI 2: NÚMERO DE MARCAS ÚNICAS
unique_brands = df['brand'].nunique()
col2.metric(label="Número de marcas únicas", value=unique_brands)

# KPI 3: PREÇO MÉDIOI NOVO (EM REAIS)
average_new_price = df['new_price'].mean()
col3.metric(label="Preço médio novo (R$)", value=f"{average_new_price:.2f}")

# QUAIS MARCAS SÃO MAIS ENCONTRADAS ATÉ A 10º PÁGINA
st.subheader("Marcas mais enncontradas até a 10º pág.")
col1, col2 = st.columns([4,2])
top_10_pages_brands = df.head(500)['brand'].value_counts().sort_values(ascending=False)
col1.bar_chart(top_10_pages_brands)
col2.write(top_10_pages_brands)

# QUAL O PREÇO  MÉDIO POR MARCA
st.subheader("Preço médio por marca")
col1, col2 = st.columns([4,2])
df_non_zero_prices = df[df['new_price'] > 0 ]
average_price_by_brand = df_non_zero_prices.groupby('brand')['new_price'].mean().sort_values(ascending=False)
col1.bar_chart(average_price_by_brand)
col2.write(average_price_by_brand)

# QUAL A SATISFAÇÃO POR MARCA
st.subheader("Satisfação por marca")
col1, col2 = st.columns([4,2])
df_non_zero_reviews = df[df['reviews_rating_number'] > 0 ]
satifaction_by_brand = df_non_zero_reviews.groupby('brand')['reviews_rating_number'].mean().sort_values(ascending=False)
col1.bar_chart(satifaction_by_brand)
col2.write(satifaction_by_brand)