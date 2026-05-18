# Logística e Prazo de Entrega

**Responsável:** Pessoa 4

## 📊 Tabelas Principais

`orders, order_items, customers`

## 🎯 Objetivos da Análise

- Tempo médio de entrega
- Comparar prazo estimado vs real
- Taxa de atraso por região
- Impacto do atraso na satisfação

## 📁 Estrutura

```
src/pessoa_4/
├── etl/
│   ├── extract.py
│   ├── transform.py
│   └── load.py
└── analysis/
    └── (scripts de análise)
```
## 🚀 Como Executar

```bash
# Extract
python src/pessoa_4/etl/extract.py

# Transform
python src/pessoa_4/etl/transform.py
```

## 📊 Visualizações e métricas apresentadas no Dashboard

O dashboard apresenta análises logísticas utilizando os dados públicos da Olist.

### Métricas apresentadas
- Tempo médio de entrega
- Atraso médio dos pedidos
- Taxa de pedidos atrasados
- Média de avaliação dos clientes

### Visualizações apresentadas
- Top 10 estados com maior taxa de atraso
- Comparativo de avaliações entre pedidos atrasados e entregues no prazo
- Indicadores logísticos gerais

---

## ☁️ Publicação da solução no Streamlit Cloud

A aplicação foi preparada para publicação no Streamlit Cloud.

### Etapas realizadas
1. Upload do projeto no GitHub
2. Integração do repositório com Streamlit Cloud
3. Configuração do arquivo principal da aplicação
4. Publicação do dashboard online
