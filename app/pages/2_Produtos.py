import pandas as pd
import streamlit as st
import plotly.express as px
from pathlib import Path

# --- 1. CONFIGURAÇÃO DA PÁGINA (ESTILO) ---
st.set_page_config(page_title="Dashboard Amanda", layout="wide")

# CSS para criar espaço entre os elementos
st.markdown("""
    <style>
    .main { padding-top: 2rem; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; font-size: 16px; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Painel de Análise de Produtos")
st.markdown(f"**Responsável:** Amanda | **Status:** Dados Processados ✅")
st.divider() # Linha horizontal para separar o título

# --- 2. CARREGAR DADOS ---
BASE = Path(__file__).resolve().parent.parent.parent
CAMINHO_ARQUIVO = BASE / "data" / "cleaned" / "pessoa_2" / "produtos.csv"

@st.cache_data
def carregar_dados():
    return pd.read_csv(CAMINHO_ARQUIVO, sep=None, engine='python')

try:
    df = carregar_dados()

    # --- 3. ORGANIZAÇÃO EM ABAS (Para não ficar tudo junto) ---
    aba1, aba2, aba3 = st.tabs(["💰 Performance Financeira", "🚚 Logística e Frete", "⭐ Avaliações e Mix"])

    with aba1:
        st.subheader("Análise de Faturamento")
        c1, c2 = st.columns([2, 1]) # Coluna 1 é o dobro da Coluna 2
        
        with c1:
            top_fat = df.groupby('Categoria')['Faturamento'].sum().sort_values(ascending=False).head(10).reset_index()
            fig1 = px.bar(top_fat, x='Categoria', y='Faturamento', 
                          title="Top 10 Categorias por Faturamento",
                          text_auto='.2s', color='Faturamento', color_continuous_scale='Blues')
            fig1.update_layout(margin=dict(t=50, b=50, l=25, r=25)) # Dá respiro no gráfico
            st.plotly_chart(fig1, use_container_width=True)
        
        with c2:
            st.info("💡 **Insight:** As categorias no topo representam 80% do faturamento total desta amostra.")

    with aba2:
        st.subheader("Custos de Logística")
        c3, c4 = st.columns(2)
        
        with c3:
            top_frete = df.groupby('Categoria')['Frete'].mean().sort_values(ascending=False).head(10).reset_index()
            fig3 = px.bar(top_frete, x='Categoria', y='Frete', 
                          title="Frete Médio por Categoria",
                          color='Frete', color_continuous_scale='Reds')
            st.plotly_chart(fig3, use_container_width=True)
            
        with c4:
            top_grama = df.groupby('Categoria')['Frete por grama'].mean().sort_values(ascending=False).head(10).reset_index()
            fig6 = px.line(top_grama, x='Categoria', y='Frete por grama', title="Eficiência: Frete por Grama", markers=True)
            st.plotly_chart(fig6, use_container_width=True)

    with aba3:
        st.subheader("Qualidade e Distribuição")
        c5, c6 = st.columns(2)
        
        with c5:
            top_aval = df.groupby('Categoria')['Avaliacao'].mean().sort_values(ascending=False).head(10).reset_index()
            fig4 = px.bar(top_aval, x='Avaliacao', y='Categoria', orientation='h', 
                          title="Satisfação Média", color='Avaliacao', color_continuous_scale='Purp')
            st.plotly_chart(fig4, use_container_width=True)
            
        with c6:
            top_vol = df['Categoria'].value_counts().head(10).reset_index()
            top_vol.columns = ['Categoria', 'Quantidade']
            fig5 = px.pie(top_vol, values='Quantidade', names='Categoria', title="Mix de Produtos", hole=0.5)
            st.plotly_chart(fig5, use_container_width=True)

except Exception as e:
    st.error(f"Erro: {e}")
