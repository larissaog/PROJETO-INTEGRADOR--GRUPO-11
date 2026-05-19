import streamlit as st
import pandas as pd
import plotly.express as px

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Dashboard Olist",
    page_icon="📊",
    layout="wide"
)

# TÍTULO
st.title("📊 Dashboard de Clientes - Olist")
st.markdown("Análise de clientes, pedidos e pagamentos")

# CARREGAMENTO DOS DADOS
customers = pd.read_csv("notebooks/pessoa_1_clientes/olist_customers_dataset.csv")
orders = pd.read_csv("notebooks/pessoa_1_clientes/olist_orders_dataset.csv")
payments = pd.read_csv("notebooks/pessoa_1_clientes/olist_order_payments_dataset.csv")
items = pd.read_csv("notebooks/pessoa_1_clientes/olist_order_items_dataset.csv")

# JUNÇÃO DOS DADOS
df = orders.merge(customers, on="customer_id", how="left")
df = df.merge(payments, on="order_id", how="left")
df = df.merge(items, on="order_id", how="left")

# KPIs
total_clientes = df["customer_unique_id"].nunique()
total_pedidos = df["order_id"].nunique()
valor_total = df["payment_value"].sum()
ticket_medio = valor_total / total_pedidos

# CARDS
col1, col2, col3, col4 = st.columns(4)

col1.metric("Clientes", f"{total_clientes:,}")
col2.metric("Pedidos", f"{total_pedidos:,}")
col3.metric("Faturamento", f"R$ {valor_total:,.2f}")
col4.metric("Ticket Médio", f"R$ {ticket_medio:,.2f}")

st.divider()

# SIDEBAR
st.sidebar.header("Filtros")

estados = st.sidebar.multiselect(
    "Selecione os estados",
    options=df["customer_state"].unique(),
    default=df["customer_state"].unique()
)

df_filtrado = df[df["customer_state"].isin(estados)]

# GRÁFICO 1 — CLIENTES POR ESTADO
clientes_estado = (
    df_filtrado.groupby("customer_state")["customer_unique_id"]
    .nunique()
    .reset_index()
)

fig1 = px.bar(
    clientes_estado,
    x="customer_state",
    y="customer_unique_id",
    title="Clientes por Estado"
)

st.plotly_chart(fig1, use_container_width=True)

# GRÁFICO 2 — FORMAS DE PAGAMENTO
pagamentos = (
    df_filtrado.groupby("payment_type")["payment_value"]
    .sum()
    .reset_index()
)

fig2 = px.pie(
    pagamentos,
    names="payment_type",
    values="payment_value",
    title="Distribuição de Pagamentos"
)

st.plotly_chart(fig2, use_container_width=True)

# GRÁFICO 3 — TOP ESTADOS EM FATURAMENTO
faturamento_estado = (
    df_filtrado.groupby("customer_state")["payment_value"]
    .sum()
    .reset_index()
    .sort_values(by="payment_value", ascending=False)
)

fig3 = px.bar(
    faturamento_estado,
    x="customer_state",
    y="payment_value",
    title="Faturamento por Estado"
)

st.plotly_chart(fig3, use_container_width=True)

# INSIGHTS
st.subheader("📌 Insights")

estado_top = faturamento_estado.iloc[0]["customer_state"]

st.write(
    f"O estado com maior faturamento é {estado_top}."
)

st.write(
    "O dashboard permite analisar clientes, pedidos e comportamento de compra."
)
