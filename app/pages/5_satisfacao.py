import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================================
# CONFIGURAÇÃO DA PÁGINA
# =========================================================

st.set_page_config(
    page_title="Dashboard Satisfação",
    page_icon="⭐",
    layout="wide"
)

# =========================================================
# TÍTULO
# =========================================================

st.title("⭐ Dashboard de Satisfação - Olist")
st.markdown("Análise de avaliações e atrasos nas entregas")

# =========================================================
# CARREGAMENTO DOS DADOS
# =========================================================

reviews = pd.read_csv(
    "data/cleaned/pessoa_5/p5_order_reviews_dataset.csv"
)

orders = pd.read_csv(
    "data/cleaned/pessoa_5/p5_orders_dataset.csv"
)

# =========================================================
# JUNÇÃO DOS DADOS
# =========================================================

df = reviews.merge(
    orders,
    on="order_id",
    how="left"
)

# =========================================================
# TRATAMENTO DAS DATAS
# =========================================================

df["order_delivered_customer_date"] = pd.to_datetime(
    df["order_delivered_customer_date"],
    errors="coerce"
)

df["order_estimated_delivery_date"] = pd.to_datetime(
    df["order_estimated_delivery_date"],
    errors="coerce"
)

# =========================================================
# CRIANDO ATRASO NA ENTREGA
# =========================================================

df["delivery_delay"] = (
    df["order_delivered_customer_date"]
    - df["order_estimated_delivery_date"]
).dt.days

# =========================================================
# LIMPEZA
# =========================================================

df = df.dropna(subset=["delivery_delay"])

# =========================================================
# KPIs
# =========================================================

media_nota = df["review_score"].mean()

total_avaliacoes = len(df)

avaliacoes_negativas = len(
    df[df["review_score"] <= 3]
)

percentual_negativas = (
    avaliacoes_negativas / total_avaliacoes
) * 100

# =========================================================
# CARDS
# =========================================================

col1, col2, col3 = st.columns(3)

col1.metric(
    "⭐ Média das Notas",
    f"{media_nota:.2f}"
)

col2.metric(
    "📝 Total de Avaliações",
    f"{total_avaliacoes:,}"
)

col3.metric(
    "😡 Avaliações Negativas",
    f"{percentual_negativas:.1f}%"
)

st.divider()

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.header("Filtros")

notas = st.sidebar.multiselect(
    "Selecione as notas",
    options=sorted(df["review_score"].unique()),
    default=sorted(df["review_score"].unique())
)

df_filtrado = df[
    df["review_score"].isin(notas)
]

# =========================================================
# GRÁFICO 1 — DISTRIBUIÇÃO DAS NOTAS
# =========================================================

dist_notas = (
    df_filtrado["review_score"]
    .value_counts()
    .sort_index()
    .reset_index()
)

dist_notas.columns = [
    "Nota",
    "Quantidade"
]

fig1 = px.bar(
    dist_notas,
    x="Nota",
    y="Quantidade",
    title="Distribuição das Avaliações",
    text="Quantidade"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# =========================================================
# GRÁFICO 2 — ATRASO X NOTA
# =========================================================

fig2 = px.box(
    df_filtrado,
    x="review_score",
    y="delivery_delay",
    title="Atraso na Entrega x Nota",
    labels={
        "review_score": "Nota",
        "delivery_delay": "Dias de atraso"
    }
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# =========================================================
# GRÁFICO 3 — MÉDIA DE ATRASO POR NOTA
# =========================================================

media_delay = (
    df_filtrado
    .groupby("review_score")["delivery_delay"]
    .mean()
    .reset_index()
)

fig3 = px.line(
    media_delay,
    x="review_score",
    y="delivery_delay",
    markers=True,
    title="Média de Atraso por Nota",
    labels={
        "review_score": "Nota",
        "delivery_delay": "Média de atraso"
    }
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# =========================================================
# GRÁFICO 4 — POSITIVAS X NEGATIVAS
# =========================================================

df_filtrado["tipo_review"] = df_filtrado[
    "review_score"
].apply(
    lambda x: "Negativa"
    if x <= 3
    else "Positiva"
)

tipo_review = (
    df_filtrado["tipo_review"]
    .value_counts()
    .reset_index()
)

tipo_review.columns = [
    "Tipo",
    "Quantidade"
]

fig4 = px.pie(
    tipo_review,
    names="Tipo",
    values="Quantidade",
    title="Avaliações Positivas x Negativas"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

# =========================================================
# INSIGHTS
# =========================================================

st.subheader("📌 Insights")

pior_nota = media_delay.loc[
    media_delay["delivery_delay"].idxmax(),
    "review_score"
]

st.write(
    f"A nota com maior média de atraso foi {pior_nota}."
)

st.write(
    "Pedidos com maiores atrasos tendem a receber avaliações mais baixas."
)

st.write(
    "A maior parte das avaliações permanece positiva."
)