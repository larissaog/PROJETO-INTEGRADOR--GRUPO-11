import streamlit as st
import matplotlib.pyplot as plt

st.title("📦 Métricas Logísticas e Prazos de Entrega")

# Leitura dos dados
orders = pd.read_csv('dados/olist_orders_dataset.csv')
customers = pd.read_csv('dados/olist_customers_dataset.csv')
reviews = pd.read_csv('dados/olist_order_reviews_dataset.csv')

# Conversão de datas
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
orders['order_delivered_customer_date'] = pd.to_datetime(orders['order_delivered_customer_date'])
orders['order_estimated_delivery_date'] = pd.to_datetime(orders['order_estimated_delivery_date'])

# Criação das métricas
orders['delivery_time'] = (
    orders['order_delivered_customer_date'] - orders['order_purchase_timestamp']
).dt.days

orders['delay'] = (
    orders['order_delivered_customer_date'] - orders['order_estimated_delivery_date']
).dt.days

orders['is_delayed'] = orders['delay'] > 0

# Removendo dados nulos
orders = orders.dropna(subset=['order_delivered_customer_date'])

# Merge com clientes
df = orders.merge(customers, on='customer_id', how='left')

# Merge com avaliações
df = df.merge(reviews, on='order_id', how='left')

# Métricas principais
avg_delivery = df['delivery_time'].mean()
avg_delay = df['delay'].mean()
delay_rate = df['is_delayed'].mean() * 100
avg_review = df['review_score'].mean()

# Exibição das métricas
col1, col2 = st.columns(2)

with col1:
    st.metric("Tempo médio de entrega", f"{avg_delivery:.2f} dias")
    st.metric("Taxa de atraso", f"{delay_rate:.2f}%")

with col2:
    st.metric("Atraso médio", f"{avg_delay:.2f} dias")
    st.metric("Média de avaliação", f"{avg_review:.2f}")

# Taxa de atraso por estado
state_delay = (
    df.groupby('customer_state')['is_delayed']
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

# Gráfico
fig, ax = plt.subplots(figsize=(8,5))
state_delay.plot(kind='barh', ax=ax)
ax.set_title('Top 10 estados com maior taxa de atraso')
ax.set_xlabel('Taxa de atraso')
ax.set_ylabel('Estado')

st.pyplot(fig)

# Comparativo de avaliações
st.subheader("Impacto do atraso na satisfação do cliente")
review_comparison = df.groupby('is_delayed')['review_score'].mean()
st.write(review_comparison)
