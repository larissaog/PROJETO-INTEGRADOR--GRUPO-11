# ============================================================================
# DASHBOARD STREAMLIT - ANÁLISE FINANCEIRA
# Pessoa 6: Análise Financeira e Pagamentos
# ============================================================================

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================================

st.set_page_config(  # Configurações que vão aparecer no navegador, cosmético
    page_title="Análise Financeira",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# TÍTULO E INTRODUÇÃO
# ============================================================================

st.title("💰 Análise Financeira e Pagamentos")
st.markdown("""
Dashboard com análises de **receita**, **ticket médio**, **sazonalidade** e **parcelamento**.
Aluno Responsável: Lucas Vinícius dos Santos
""")
st.markdown("---")

# ============================================================================
# CAMINHOS
# ============================================================================

# Encontrar a raiz do projeto
CLEANED_DATA_PATH = "data/cleaned/pessoa_6"

# ============================================================================
# CARREGAR E PROCESSAR DADOS
# ============================================================================

# O cache_data garante que a função seja executada apenas uma vez
@st.cache_data
def carregar_dados():

    # Carregar CSVs
    df_payments = pd.read_csv(f"{CLEANED_DATA_PATH}/payments_clean.csv")
    df_orders = pd.read_csv(f"{CLEANED_DATA_PATH}/orders_clean.csv")
    
    # Reconverter datas
    df_orders['order_purchase_timestamp'] = pd.to_datetime(df_orders['order_purchase_timestamp'])
    df_orders['order_approved_at'] = pd.to_datetime(df_orders['order_approved_at'])
    df_orders['order_delivered_carrier_date'] = pd.to_datetime(df_orders['order_delivered_carrier_date'])
    df_orders['order_delivered_customer_date'] = pd.to_datetime(df_orders['order_delivered_customer_date'])
    df_orders['order_estimated_delivery_date'] = pd.to_datetime(df_orders['order_estimated_delivery_date'])
    
    # Merge payments + orders, funciona como um left join
    df_receita = df_payments.merge(
        df_orders[['order_id', 'order_purchase_timestamp', 'order_status']], 
        on='order_id', 
        how='left'
    )
    
    # Filtrar apenas pedidos entregues
    df_receita_entregue = df_receita[df_receita['order_status'] == 'delivered'].copy()
    
    return df_receita_entregue

df_receita_entregue = carregar_dados()

# ============================================================================
# MÉTRICAS PRINCIPAIS (KPIs)
# ============================================================================

st.header("📊 Métricas Principais")

# Calcular KPIs
receita_total = df_receita_entregue['payment_value'].sum()
num_pedidos = df_receita_entregue['order_id'].nunique()
ticket_medio = receita_total / num_pedidos

# Exibir em 3 colunas
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="💰 Receita Total",
        value=f"R$ {receita_total:,.2f}",
        help="Soma de todos os pagamentos de pedidos entregues"
    )

with col2:
    st.metric(
        label="📦 Total de Pedidos",
        value=f"{num_pedidos:,}",
        help="Número de pedidos únicos entregues"
    )

with col3:
    st.metric(
        label="🎯 Ticket Médio",
        value=f"R$ {ticket_medio:.2f}",
        help="Valor médio por pedido"
    )

st.markdown("---")

# ============================================================================
# ANÁLISE 1: RECEITA MENSAL
# ============================================================================

st.header("📈 Análise 1: Evolução da Receita Mensal")

# Preparar dados
df_receita_entregue['ano_mes'] = df_receita_entregue['order_purchase_timestamp'].dt.to_period('M').astype(str)

df_receita_mensal = df_receita_entregue.groupby('ano_mes').agg({
    'payment_value': 'sum',
    'order_id': 'nunique'
}).reset_index()

df_receita_mensal.columns = ['ano_mes', 'receita_total', 'total_pedidos']
df_receita_mensal['ticket_medio'] = df_receita_mensal['receita_total'] / df_receita_mensal['total_pedidos']

# Criar gráfico
fig1 = go.Figure()

fig1.add_trace(go.Scatter(
    x=df_receita_mensal['ano_mes'],
    y=df_receita_mensal['receita_total'],
    mode='lines+markers',
    name='Receita Mensal',
    line=dict(color='#1f77b4', width=3),
    marker=dict(size=8),
    customdata=df_receita_mensal[['total_pedidos']],
    hovertemplate=(
        '<b>%{x}</b><br>' +
        'Receita: R$ %{y:,.2f}<br>' +
        'Pedidos: %{customdata[0]:,}' +
        '<extra></extra>'
    )
))

fig1.update_layout(
    xaxis_title='Mês/Ano',
    yaxis_title='Receita (R$)',
    template='plotly_white',
    height=500,
    hovermode='x unified',
    hoverlabel=dict(
        bgcolor="white",
        font_size=14,
        font_color="black",
        bordercolor="#cccccc"
    )
)

# Usar o tamanho do navegador, fica mais responsivo
st.plotly_chart(fig1, use_container_width=True)

# Insights
col1, col2 = st.columns(2)

with col1:
    melhor_mes = df_receita_mensal.loc[df_receita_mensal['receita_total'].idxmax()]
    st.success(f"""
    **🏆 Melhor Mês**  
    **Período:** {melhor_mes['ano_mes']}  
    **Receita:** R$ {melhor_mes['receita_total']:,.2f}  
    **Pedidos:** {melhor_mes['total_pedidos']:,}
    """)

with col2:
    pior_mes = df_receita_mensal.loc[df_receita_mensal['receita_total'].idxmin()]
    st.info(f"""
    **📉 Pior Mês**  
    **Período:** {pior_mes['ano_mes']}  
    **Receita:** R$ {pior_mes['receita_total']:,.2f}  
    **Pedidos:** {pior_mes['total_pedidos']:,}
    """)

st.markdown("---")

# ============================================================================
# ANÁLISE 2: TICKET MÉDIO
# ============================================================================

st.header("🎯 Análise 2: Evolução do Ticket Médio")

# Criar gráfico
fig2 = go.Figure()

fig2.add_trace(go.Scatter(
    x=df_receita_mensal['ano_mes'],
    y=df_receita_mensal['ticket_medio'],
    mode='lines+markers',
    name='Ticket Médio',
    line=dict(color='#9b59b6', width=3),
    marker=dict(size=8),
    fill='tozeroy',
    fillcolor='rgba(155, 89, 182, 0.2)',
    customdata=df_receita_mensal[['total_pedidos', 'receita_total']],
    hovertemplate=(
        '<b>%{x}</b><br>' +
        'Ticket Médio: R$ %{y:.2f}<br>' +
        'Pedidos: %{customdata[0]:,}<br>' +
        'Receita Total: R$ %{customdata[1]:,.2f}' +
        '<extra></extra>'
    )
))

# Linha de média geral
media_geral = df_receita_mensal['ticket_medio'].mean()
fig2.add_hline(
    y=media_geral,
    line_dash="dash",
    line_color="red",
    annotation_text=f"Média: R$ {media_geral:.2f}",
    annotation_position="right"
)

fig2.update_layout(
    xaxis_title='Mês/Ano',
    yaxis_title='Ticket Médio (R$)',
    template='plotly_white',
    height=500,
    showlegend=False,
    hoverlabel=dict(
        bgcolor="white",
        font_size=14,
        font_color="black",
        bordercolor="#cccccc"
    )
)

st.plotly_chart(fig2, use_container_width=True)

# Estatísticas
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("📊 Ticket Médio Geral", f"R$ {media_geral:.2f}")

with col2:
    max_ticket = df_receita_mensal['ticket_medio'].max()
    mes_max = df_receita_mensal.loc[df_receita_mensal['ticket_medio'].idxmax(), 'ano_mes']
    st.metric("📈 Maior Ticket Médio", f"R$ {max_ticket:.2f}", delta=mes_max)

with col3:
    min_ticket = df_receita_mensal['ticket_medio'].min()
    mes_min = df_receita_mensal.loc[df_receita_mensal['ticket_medio'].idxmin(), 'ano_mes']
    st.metric("📉 Menor Ticket Médio", f"R$ {min_ticket:.2f}", delta=mes_min)

st.markdown("---")

# ============================================================================
# ANÁLISE 3: SAZONALIDADE
# ============================================================================

st.header("📅 Análise 3: Sazonalidade - Receita por Mês do Ano")

# Preparar dados
df_receita_entregue['mes_numero'] = df_receita_entregue['order_purchase_timestamp'].dt.month

df_sazonalidade = df_receita_entregue.groupby('mes_numero').agg({
    'payment_value': 'sum',
    'order_id': 'nunique'
}).reset_index()

df_sazonalidade.columns = ['mes_numero', 'receita_total', 'total_pedidos']
df_sazonalidade['ticket_medio'] = df_sazonalidade['receita_total'] / df_sazonalidade['total_pedidos']

# Nomes dos meses
meses_nomes = {
    1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
    5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
    9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
}
df_sazonalidade['mes_nome'] = df_sazonalidade['mes_numero'].map(meses_nomes)

# Criar gráfico
fig3 = go.Figure()

fig3.add_trace(go.Bar(
    x=df_sazonalidade['mes_nome'],
    y=df_sazonalidade['receita_total'],
    marker_color='#3498db',
    text=df_sazonalidade['receita_total'],
    texttemplate='R$ %{text:,.0f}',
    textposition='outside',
    customdata=df_sazonalidade[['total_pedidos', 'ticket_medio']],
    hovertemplate=(
        '<b>%{x}</b><br>' +
        'Receita Total: R$ %{y:,.2f}<br>' +
        'Pedidos: %{customdata[0]:,}<br>' +
        'Ticket Médio: R$ %{customdata[1]:.2f}' +
        '<extra></extra>'
    )
))

fig3.update_layout(
    xaxis_title='Mês',
    yaxis_title='Receita Total (R$)',
    template='plotly_white',
    height=500,
    showlegend=False,
    hoverlabel=dict(
        bgcolor="white",
        font_size=14,
        font_color="black",
        bordercolor="#cccccc"
    )
)

st.plotly_chart(fig3, use_container_width=True)

# Insights
col1, col2 = st.columns(2)

with col1:
    melhor_mes_ano = df_sazonalidade.loc[df_sazonalidade['receita_total'].idxmax()]
    st.success(f"""
    **🏆 Melhor Mês do Ano**  
    **Mês:** {melhor_mes_ano['mes_nome']}  
    **Receita:** R$ {melhor_mes_ano['receita_total']:,.2f}  
    **Pedidos:** {melhor_mes_ano['total_pedidos']:,}
    """)

with col2:
    pior_mes_ano = df_sazonalidade.loc[df_sazonalidade['receita_total'].idxmin()]
    st.info(f"""
    **📉 Pior Mês do Ano**  
    **Mês:** {pior_mes_ano['mes_nome']}  
    **Receita:** R$ {pior_mes_ano['receita_total']:,.2f}  
    **Pedidos:** {pior_mes_ano['total_pedidos']:,}
    """)

st.markdown("---")

# ============================================================================
# ANÁLISE 4: PARCELAMENTO
# ============================================================================

st.header("💳 Análise 4: Parcelamento")

# Preparar dados
df_parcelamento = df_receita_entregue.groupby('payment_installments').agg({
    'payment_value': ['sum', 'mean'],
    'order_id': 'nunique'
}).reset_index()

df_parcelamento.columns = ['num_parcelas', 'receita_total', 'valor_medio', 'num_pedidos']
df_parcelamento['percentual_pedidos'] = (df_parcelamento['num_pedidos'] / df_parcelamento['num_pedidos'].sum()) * 100
df_parcelamento = df_parcelamento.sort_values('num_parcelas')

# Criar gráfico scatter
fig4 = go.Figure()

fig4.add_trace(go.Scatter(
    x=df_parcelamento['num_parcelas'],
    y=df_parcelamento['valor_medio'],
    mode='markers',
    marker=dict(
        size=df_parcelamento['num_pedidos'],
        sizemode='area',
        sizeref=2.*max(df_parcelamento['num_pedidos'])/(40.**2),
        color=df_parcelamento['num_pedidos'],
        colorscale='Blues',
        showscale=True,
        colorbar=dict(title="Nº de<br>Pedidos"),
        line=dict(width=1, color='white')
    ),
    customdata=df_parcelamento[['num_pedidos', 'receita_total', 'percentual_pedidos']],
    hovertemplate=(
        '<b>%{x}x Parcelas</b><br>' +
        'Valor Médio: R$ %{y:,.2f}<br>' +
        'Pedidos: %{customdata[0]:,} (%{customdata[2]:.1f}%)<br>' +
        'Receita Total: R$ %{customdata[1]:,.2f}' +
        '<extra></extra>'
    ),
    name=''
))

fig4.update_layout(
    title={
        'text': '<b>💳 Relação: Número de Parcelas x Valor Médio da Compra</b>',
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 20, 'color': '#2c3e50'}
    },
    xaxis_title='Número de Parcelas',
    yaxis_title='Valor Médio da Compra (R$)',
    template='plotly_white',
    height=600,
    showlegend=False,
    hoverlabel=dict(
        bgcolor="white",
        font_size=14,
        font_color="black",
        bordercolor="#cccccc"
    )
)

fig4.update_xaxes(dtick=1)
st.plotly_chart(fig4, use_container_width=True)

# ============================================================================
# RODAPÉ
# ============================================================================

st.markdown("---")
st.caption("Dashboard Financeiro - Projeto Integrador SENAC - Grupo 37 - Pessoa 6")
st.caption("Todos os gráficos tem tooltip com o hover do mouse.")