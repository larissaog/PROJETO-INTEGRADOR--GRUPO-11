import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="PERFORMANCE COMERCIAL - GRUPO 11", layout="wide")

# --- 2. ESTILIZAÇÃO GLOBAL (35PX + NEGRITO) ---
st.markdown("""
    <style>
    /* CABEÇALHO PRINCIPAL */
    .main-title {
        color: #1e3d59; text-align: center; font-weight: 900;
        font-size: 55px !important; text-transform: uppercase;
    }

    /* TEXTOS GERAIS EM 35PX */
    html, body, [class*="st-"], p, div {
        font-size: 35px !important;
    }

    /* NÚMEROS DAS MÉTRICAS (KPIs) EM NEGRITO */
    [data-testid="stMetricValue"] {
        font-size: 50px !important;
        font-weight: bold !important;
        color: #1e3d59;
    }

    /* TÍTULOS DE SEÇÃO EM NEGRITO */
    .section-header {
        color: #ffffff; background-color: #1e3d59; padding: 15px;
        border-radius: 8px; font-weight: bold !important; 
        text-transform: uppercase; margin-top: 40px;
    }

    /* TABELAS COM NÚMEROS EM NEGRITO */
    .stTable td, .stTable th {
        font-size: 35px !important;
        font-weight: bold !important;
    }

    .plot-card {
        background-color: #ffffff; border: 2px solid #e0e0e0;
        padding: 25px; border-radius: 15px;
        box-shadow: 0 6px 15px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CARGA DE DADOS ---
@st.cache_data
def carregar_dados():
    caminho = "notebooks/pessoa_3_vendedores/03_Vend_Perform_Comercial/"
    order_items = pd.read_csv(caminho + 'olist_order_items_dataset.csv')
    sellers = pd.read_csv(caminho + 'olist_sellers_dataset.csv')
    orders = pd.read_csv(caminho + 'olist_orders_dataset.csv')
    
    df_vendas = pd.merge(order_items, sellers, on='seller_id')
    df_completo = pd.merge(df_vendas, orders, on='order_id')
    df_completo['order_purchase_timestamp'] = pd.to_datetime(df_completo['order_purchase_timestamp'])
    return df_completo

df = carregar_dados()

if df is not None:
    st.markdown('<h1 class="main-title">Análise de Performance de Vendedores</h1>', unsafe_allow_html=True)

    # --- SEÇÃO 1: KPIs (Números em Negrito) ---
    st.markdown('<div class="section-header">📊 KPIs DE VENDAS</div>', unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    # Formatação sem decimais para destacar os números
    m1.metric("RECEITA", f"R$ {df['price'].sum():,.0f}") 
    m2.metric("TICKET", f"R$ {df['price'].mean():,.0f}")
    m3.metric("VENDEDORES", f"{df['seller_id'].nunique():,}")
    m4.metric("PEDIDOS", f"{df['order_id'].nunique():,}")

    # --- SEÇÃO 2: SAZONALIDADE ---
    st.markdown('<div class="plot-card">', unsafe_allow_html=True)
    st.markdown('**SAZONALIDADE MENSAL**', unsafe_allow_html=True)
    df['ano'] = df['order_purchase_timestamp'].dt.year
    df['mes'] = df['order_purchase_timestamp'].dt.month
    saz = df.groupby(['ano', 'mes'])['price'].sum().reset_index()
    fig_saz = px.line(saz, x='mes', y='price', color='ano', markers=True)
    fig_saz.update_layout(font=dict(size=25, family="Arial Black")) # Negrito no gráfico
    st.plotly_chart(fig_saz, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- SEÇÃO 3: PERFORMANCE ---
    st.markdown('<div class="section-header">🏆 PERFORMANCE INDIVIDUAL</div>', unsafe_allow_html=True)
    top_10 = df.groupby('seller_id')['price'].sum().sort_values(ascending=False).head(10).reset_index()
    
    st.markdown('<div class="plot-card">', unsafe_allow_html=True)
    fig_bar = px.bar(top_10, x='price', y='seller_id', orientation='h', color='price')
    fig_bar.update_layout(font=dict(size=20, family="Arial Black"), height=600)
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Tabela com números em negrito
    st.markdown('<br>**MAIORES FATURAMENTOS (TOP 10)**', unsafe_allow_html=True)
    # Formatando para moeda antes de exibir na tabela
    top_10_formatted = top_10.copy()
    top_10_formatted['price'] = top_10_formatted['price'].map('R$ {:,.2f}'.format)
    st.table(top_10_formatted)

    # --- SEÇÃO 4: GEOGRAFIA 80/20 ---
    st.markdown('<div class="section-header">🌎 DISTRIBUIÇÃO GEOGRÁFICA (80/20)</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    rec_estado = df.groupby('seller_state')['price'].sum().sort_values(ascending=False).reset_index()
    rec_estado['acum'] = (rec_estado['price'] / rec_estado['price'].sum()).cumsum() * 100
    
    with c1:
        st.markdown('**CORE (80% RECEITA)**', unsafe_allow_html=True)
        fig80 = px.pie(rec_estado[rec_estado['acum'] <= 82], values='price', names='seller_state', color_discrete_sequence=px.colors.qualitative.Pastel)
        fig80.update_layout(font=dict(size=25, family="Arial Black"))
        st.plotly_chart(fig80, use_container_width=True)

    with c2:
        st.markdown('**SECUNDÁRIOS (20% RECEITA)**', unsafe_allow_html=True)
        fig20 = px.pie(rec_estado[rec_estado['acum'] > 82], values='price', names='seller_state', color_discrete_sequence=px.colors.qualitative.Safe)
        fig20.update_layout(font=dict(size=25, family="Arial Black"))
        st.plotly_chart(fig20, use_container_width=True)

st.markdown("<br><p style='text-align: center; font-size: 35px; font-weight: bold;'>Performance Comerical</p>", unsafe_allow_html=True)
