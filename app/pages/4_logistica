
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title='Dashboard Logístico', layout='wide')

st.title('📦 Dashboard Logístico — Olist')

# =========================
# Leitura dos dados
# =========================

orders = pd.read_csv('dados/olist_orders_dataset.csv')
customers = pd.read_csv('dados/olist_customers_dataset.csv')
reviews = pd.read_csv('dados/olist_order_reviews_dataset.csv')

# =========================
# Tratamento dos dados
# =========================

orders['order_purchase_timestamp'] = pd.to_datetime(
    orders['order_purchase_timestamp']
)

orders['order_delivered_customer_date'] = pd.to_datetime(
    orders['order_delivered_customer_date']
)

orders['order_estimated_delivery_date'] = pd.to_datetime(
    orders['order_estimated_delivery_date']
)

orders = orders.dropna(subset=['order_delivered_customer_date'])

# =========================
# Métricas
# =========================

orders['delivery_time'] = (
    orders['order_delivered_customer_date'] -
    orders['order_purchase_timestamp']
).dt.days

orders['delay'] = (
    orders['order_delivered_customer_date'] -
    orders['order_estimated_delivery_date']
).dt.days

orders['is_delayed'] = orders['delay'] > 0

# =========================
# Merge dos dados
# =========================

df = orders.merge(customers, on='customer_id', how='left')
df = df.merge(reviews, on='order_id', how='left')

# =========================
# KPIs
# =========================

media_entrega = df['delivery_time'].mean()
taxa_atraso = df['is_delayed'].mean() * 100
atraso_medio = df['delay'].mean()
nota_media = df['review_score'].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric('Tempo médio de entrega', f'{media_entrega:.2f} dias')
col2.metric('Taxa de atraso', f'{taxa_atraso:.2f}%')
col3.metric('Atraso médio', f'{atraso_medio:.2f} dias')
col4.metric('Nota média', f'{nota_media:.2f}')

# =========================
# Taxa de atraso por estado
# =========================

st.subheader('Top 10 estados com maior taxa de atraso')

delay_by_state = (
    df.groupby('customer_state')['is_delayed']
    .mean()
    .sort_values(ascending=False)
)

fig1, ax1 = plt.subplots(figsize=(8,5))

delay_by_state.head(10).plot(kind='barh', ax=ax1)

ax1.set_xlabel('Taxa de atraso')
ax1.set_ylabel('Estado')

st.pyplot(fig1)

# =========================
# Distribuição do tempo de entrega
# =========================

st.subheader('Distribuição do tempo de entrega')

fig2, ax2 = plt.subplots(figsize=(8,5))

ax2.hist(df['delivery_time'], bins=30)

ax2.set_xlabel('Dias')
ax2.set_ylabel('Quantidade')

st.pyplot(fig2)

# =========================
# Satisfação x atraso
# =========================

st.subheader('Impacto do atraso na satisfação')

satisfacao = df.groupby('is_delayed')['review_score'].mean()

fig3, ax3 = plt.subplots(figsize=(6,4))

satisfacao.plot(kind='bar', ax=ax3)

ax3.set_xlabel('Pedido atrasado')
ax3.set_ylabel('Nota média')

st.pyplot(fig3)
