import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Bombeiros PE - IA", layout="wide")

# 2. CSS PARA O VISUAL (GAMBIARRA NECESSÁRIA PARA AS CORES)
st.markdown("""
<style>
    .stApp { background-color: #F5F5F5; }
    div[data-testid="metric-container"] {
        background-color: #FFFFFF;
        border: 1px solid #E0E0E0;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    h3 { font-size: 16px; margin-bottom: 5px; color: #555; }
    h2 { font-size: 28px; font-weight: bold; color: #333; }
</style>
""", unsafe_allow_html=True)

# 3. BARRA LATERAL COM FILTROS (O SEGREDO DA INTERATIVIDADE)
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Bras%C3%A3o_CBMPE.png/120px-Bras%C3%A3o_CBMPE.png", width=80)
st.sidebar.header("🎛️ Filtros do Dashboard")
st.sidebar.info("Use os filtros abaixo para cruzar dados em tempo real.")

# -- GERANDO DADOS MAIS ROBUSTOS PARA AGUENTAR FILTROS --
# Criamos 500 linhas de dados falsos para parecer real
np.random.seed(42) # Pra sempre gerar os mesmos dados
df = pd.DataFrame({
    'Bairro': np.random.choice(['Boa Viagem', 'Santo Amaro', 'Várzea', 'Ibura', 'Derby', 'Casa Forte'], 500),
    'Tipo': np.random.choice(['Incêndio', 'Salvamento', 'Vistoria', 'Acidente Veicular'], 500),
    'Status': np.random.choice(['Concluído', 'Em Andamento', 'Pendente'], 500),
    'Risco': np.random.randint(1, 100, 500),
    'Latitude': np.random.uniform(-8.05, -8.15, 500), # Latitudes de Recife
    'Longitude': np.random.uniform(-34.88, -34.95, 500) # Longitudes de Recife
})

# -- O FILTRO DE BAIRRO --
bairros_selecionados = st.sidebar.multiselect(
    "📍 Selecione o Bairro:",
    options=df['Bairro'].unique(),
    default=df['Bairro'].unique() # Começa com todos marcados
)

# -- O FILTRO DE STATUS --
status_selecionado = st.sidebar.multiselect(
    "🚦 Status da Ocorrência:",
    options=df['Status'].unique(),
    default=df['Status'].unique()
)

# -- APLICAÇÃO DOS FILTROS (MÁGICA) --
# O dataframe df_filtrado é o que vai ser usado nos gráficos
df_filtrado = df[
    (df['Bairro'].isin(bairros_selecionados)) & 
    (df['Status'].isin(status_selecionado))
]

# 4. O DASHBOARD (CORPO DA PÁGINA)
st.title("🔥 Sistema de Inteligência Operacional - CBMPE")
st.markdown("---")

# -- CARDS (KPIs) QUE MUDAM COM O FILTRO --
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Filtrado", len(df_filtrado), help="Total de ocorrências baseadas nos filtros selecionados")
col2.metric("Risco Médio", f"{int(df_filtrado['Risco'].mean())}%", delta_color="inverse", help="Média de risco calculada pela IA")
col3.metric("Em Andamento", len(df_filtrado[df_filtrado['Status']=='Em Andamento']))
col4.metric("Concluídas", len(df_filtrado[df_filtrado['Status']=='Concluído']), delta="ok")

st.markdown("---")

# -- LINHA 1 DE GRÁFICOS: MAPA E PIZZA --
c1, c2 = st.columns([2, 1])

with c1:
    st.subheader("🗺️ Mapa de Calor das Ocorrências")
    st.caption("Visualize onde estão os focos de incêndio e acidentes.")
    # Mapa simples usando dados filtrados
    st.map(df_filtrado, latitude='Latitude', longitude='Longitude')

with c2:
    st.subheader("📊 Distribuição por Tipo")
    st.caption("Qual o tipo de chamado mais comum?")
    # Gráfico de Rosquinha (Donut Chart)
    fig_pizza = px.pie(df_filtrado, names='Tipo', hole=0.5, 
                       color_discrete_sequence=px.colors.sequential.RdBu)
    fig_pizza.update_traces(textinfo='percent+label', hoverinfo='label+percent+value') # As "dicas" ao passar o mouse
    st.plotly_chart(fig_pizza, use_container_width=True)

# -- LINHA 2: MACHINE LEARNING (O QUE O PDF PEDE NA PÁGINA 8) --
st.divider()
st.header("🤖 Inteligência Artificial e Previsões")
st.info("Esta seção mostra os 'Fatores Determinantes' (Feature Importance) e a projeção futura de casos.")

c3, c4 = st.columns(2)

with c3:
    st.subheader("🔍 Fatores Determinantes (IA)")
    st.caption("O que mais influencia o risco de uma ocorrência?")
    
    # SIMULAÇÃO DO GRÁFICO DA PÁGINA 8 DO PDF (Feature Importance)
    # Criando dados fictícios de "Importância das Variáveis"
    df_importance = pd.DataFrame({
        'Fator': ['Localização (Bairro)', 'Horário do Dia', 'Condição Climática', 'Trânsito', 'Infraestrutura Urbana'],
        'Importancia': [0.85, 0.65, 0.45, 0.30, 0.20]
    }).sort_values(by='Importancia', ascending=True)

    # Gráfico de Barras Horizontais
    fig_imp = px.bar(df_importance, x='Importancia', y='Fator', orientation='h',
                     color='Importancia', color_continuous_scale='Blues')
    fig_imp.update_layout(xaxis_title="Nível de Influência (0-1)", yaxis_title="")
    st.plotly_chart(fig_imp, use_container_width=True)

with c4:
    st.subheader("📈 Previsão de Casos (Próximos Meses)")
    st.caption("Linha sólida: Histórico | Linha tracejada: Previsão da IA")
    
    # SIMULAÇÃO DE PREVISÃO TEMPORAL
    meses = ['Ago', 'Set', 'Out', 'Nov', 'Dez', 'Jan (Prev)', 'Fev (Prev)']
    valores = [20, 25, 22, 30, 45, 50, 55]
    tipo_dado = ['Real', 'Real', 'Real', 'Real', 'Real', 'Previsão IA', 'Previsão IA']
    
    df_prev = pd.DataFrame({'Mês': meses, 'Ocorrências': valores, 'Tipo': tipo_dado})
    
    # Gráfico de Linha com diferenciação de cor/estilo
    fig_line = px.line(df_prev, x='Mês', y='Ocorrências', color='Tipo', markers=True,
                       color_discrete_map={'Real': '#1f77b4', 'Previsão IA': '#ff7f0e'})
    # Deixar a linha de previsão pontilhada
    fig_line.update_traces(patch={"line": {"dash": "dot"}}, selector={"legendgroup": "Previsão IA"})
    
    st.plotly_chart(fig_line, use_container_width=True)
