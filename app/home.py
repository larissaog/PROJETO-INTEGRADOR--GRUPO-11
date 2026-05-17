import streamlit as st

# ── CONFIGURAÇÃO DA PÁGINA ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Dashboard Olist | Grupo 11",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── ESTILO CUSTOMIZADO ──────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Cards de navegação */
    .nav-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        border: 1px solid #e0e0e0;
        border-left: 5px solid #4CAF50;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 16px;
        transition: box-shadow 0.2s;
    }
    .nav-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .nav-card h3 {
        margin: 0 0 6px 0;
        font-size: 1.1rem;
        color: #1a1a2e;
    }
    .nav-card p {
        margin: 0;
        font-size: 0.88rem;
        color: #555;
    }
    /* Cores por área */
    .card-clientes    { border-left-color: #2196F3; }
    .card-produtos    { border-left-color: #FF9800; }
    .card-vendedores  { border-left-color: #9C27B0; }
    .card-logistica   { border-left-color: #F44336; }
    .card-satisfacao  { border-left-color: #FFD600; }
    .card-financeiro  { border-left-color: #4CAF50; }

    /* Banner de destaque */
    .hero {
        background: linear-gradient(120deg, #1a1a2e 0%, #16213e 60%, #0f3460 100%);
        border-radius: 12px;
        padding: 40px 36px;
        color: white;
        margin-bottom: 32px;
    }
    .hero h1 { margin: 0 0 8px 0; font-size: 2rem; }
    .hero p  { margin: 0; color: #b0bec5; font-size: 1rem; }

    /* Rodapé */
    .footer {
        text-align: center;
        font-size: 0.8rem;
        color: #999;
        margin-top: 48px;
        padding-top: 16px;
        border-top: 1px solid #eee;
    }
</style>
""", unsafe_allow_html=True)


# ── HERO ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🛒 Dashboard Olist — Grupo 11</h1>
    <p>Projeto Integrador · Introdução a Ciência de Dados · SENAC SP<br>
    Análise do Brazilian E-Commerce Public Dataset</p>
</div>
""", unsafe_allow_html=True)


# ── DESCRIÇÃO ───────────────────────────────────────────────────────────────
st.markdown(
    "Selecione uma das páginas no menu lateral ou clique em uma das áreas abaixo "
    "para explorar as análises do grupo."
)
st.markdown("---")


# ── CARDS DE NAVEGAÇÃO ──────────────────────────────────────────────────────
paginas = [
    {
        "emoji": "👥",
        "titulo": "Clientes",
        "responsavel": "Felipe Mayer",
        "descricao": "Distribuição geográfica, perfil e comportamento de compra dos clientes.",
        "classe": "card-clientes",
        "link": "pages/1_👥_Clientes",
    },
    {
        "emoji": "📦",
        "titulo": "Produtos",
        "responsavel": "Amanda",
        "descricao": "Categorias mais vendidas, preços médios e volume por produto.",
        "classe": "card-produtos",
        "link": "pages/2_📦_Produtos",
    },
    {
        "emoji": "🏪",
        "titulo": "Vendedores",
        "responsavel": "Tomaz Marinho",
        "descricao": "Desempenho dos vendedores, localização e tempo de resposta.",
        "classe": "card-vendedores",
        "link": "pages/3_🏪_Vendedores",
    },
    {
        "emoji": "🚚",
        "titulo": "Logística",
        "responsavel": "Natália",
        "descricao": "Prazos de entrega, atrasos e análise de frete por região.",
        "classe": "card-logistica",
        "link": "pages/4_🚚_Logística",
    },
    {
        "emoji": "⭐",
        "titulo": "Satisfação",
        "responsavel": "Larissa",
        "descricao": "Avaliações dos clientes, notas por categoria e análise de reviews.",
        "classe": "card-satisfacao",
        "link": "pages/5_⭐_Satisfação",
    },
    {
        "emoji": "💰",
        "titulo": "Financeiro",
        "responsavel": "Lucas",
        "descricao": "Faturamento, formas de pagamento, parcelamento e receita por período.",
        "classe": "card-financeiro",
        "link": "pages/6_💰_Financeiro",
    },
]

col1, col2 = st.columns(2)

for i, pg in enumerate(paginas):
    coluna = col1 if i % 2 == 0 else col2
    with coluna:
        st.markdown(f"""
        <div class="nav-card {pg['classe']}">
            <h3>{pg['emoji']} {pg['titulo']}</h3>
            <p><strong>Responsável:</strong> {pg['responsavel']}</p>
            <p>{pg['descricao']}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")


# ── SOBRE O DATASET ─────────────────────────────────────────────────────────
with st.expander("📂 Sobre o Dataset — Brazilian E-Commerce (Olist)"):
    st.markdown("""
    O dataset contém informações reais de **~100 mil pedidos** realizados entre 2016 e 2018
    na plataforma Olist, maior loja de departamentos dos marketplaces brasileiros.

    **Tabelas utilizadas:**

    | Arquivo | Conteúdo |
    |---|---|
    | `olist_customers_dataset.csv` | Dados dos clientes |
    | `olist_orders_dataset.csv` | Pedidos e status |
    | `olist_order_items_dataset.csv` | Itens de cada pedido |
    | `olist_order_payments_dataset.csv` | Formas e valores de pagamento |
    | `olist_order_reviews_dataset.csv` | Avaliações dos clientes |
    | `olist_products_dataset.csv` | Informações dos produtos |
    | `olist_sellers_dataset.csv` | Dados dos vendedores |
    | `olist_geolocation_dataset.csv` | Coordenadas geográficas |
    | `product_category_name_translation.csv` | Tradução das categorias |

    **Fonte:** [Kaggle — Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
    """)


# ── RODAPÉ ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    Projeto Integrador · SENAC SP · Grupo 11 &nbsp;|&nbsp;
    Felipe · Amanda · Tomaz Marinho · Natália · Larissa · Lucas
</div>
""", unsafe_allow_html=True)