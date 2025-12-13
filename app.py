import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. CONFIGURAÇÃO GERAL
st.set_page_config(page_title="Bombeiros PE - Dashboard", layout="wide")

# 2. ESTILO CSS (AS CORES EXATAS DA SUA IMAGEM)
st.markdown("""
<style>
    /* Fundo geral claro */
    .stApp { background-color: #FAFAFA; }
    
    /* Estilo dos Cards (Copiando sua imagem) */
    .card {
        border-radius: 8px;
        padding: 20px;
        color: white;
        text-align: left;
        height: 120px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        font-family: sans-serif;
        margin-bottom: 15px;
    }
    
    /* CORES IDÊNTICAS AO PRINT */
    .bg-laranja { background-color: #EF6C00; }  /* Laranja forte */
    .bg-azul { background-color: #3949AB; }     /* Azul Indigo */
    .bg-vermelho { background-color: #E65100; } /* Laranja avermelhado */
    .bg-verde { background-color: #388E3C; }    /* Verde Floresta */

    h3 { font-size: 14px; margin: 0; opacity: 0.9; font-weight: 500; color: white !important; }
    h2 { font-size: 24px; margin: 10px 0 0 0; font-weight: bold; color: white !important; }
</style>
""", unsafe_allow_html=True)

# 3. BARRA LATERAL (Filtros Interativos)
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Bras%C3%A3o_CBMPE.png/120px-Bras%C3%A3o_CBMPE.png", width=80)
st.sidebar.title("Filtros")

# Gerando dados simulados para parecer real
df = pd.DataFrame({
    'Bairro': np.random.choice(['Boa Viagem', 'Santo Amaro', 'Várzea', 'Ibura', 'Derby', 'Casa Forte'], 600),
    'Tipo': np.random.choice(['APH', 'Incêndio', 'Salvamento', 'Vistoria', 'Acidente'], 600),
    'Status': np.random.choice(['Concluído', 'Em Andamento', 'Aberto'], 600),
    'Idade': np.random.randint(18, 75, 600),
    'Risco': np.random.randint(1, 100, 600)
})

# Filtro de Bairro
bairro_filtro = st.sidebar.multiselect("Bairro", df['Bairro'].unique(), default=df['Bairro'].unique())
df_filtrado = df[df['Bairro'].isin(bairro_filtro)]

# 4. CARDS COLORIDOS (IGUALZINHO A IMAGEM)
st.markdown("## Visão Geral de Ocorrências")

col1, col2, col3, col4 = st.columns(4)

total = len(df_filtrado)
media = int(total / 30) # Simulação de média diária
abertas = len(df_filtrado[df_filtrado['Status']=='Aberto'])
resolvidas = len(df_filtrado[df_filtrado['Status']=='Concluído'])

with col1:
    st.markdown(f'<div class="card bg-laranja"><h3>Ocorrências Totais</h3><h2>{total}</h2></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="card bg-azul"><h3>Média Diária de Ocorrências</h3><h2>{media}</h2></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="card bg-vermelho"><h3>Ocorrências Abertas</h3><h2>{abertas}</h2></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="card bg-verde"><h3>Ocorrências Resolvidas</h3><h2>{resolvidas}</h2></div>', unsafe_allow_html=True)

# 5. GRÁFICOS DA LINHA DE CIMA
c1, c2, c3 = st.columns([1, 1, 1])

with c1:
    st.markdown("##### Distribuição de Idades")
    # Histograma Azul igual da imagem
    fig_hist = px.histogram(df_filtrado, x="Idade", nbins=6, 
                            color_discrete_sequence=['#5C6BC0'])
    fig_hist.update_layout(bargap=0.1, margin=dict(l=0, r=0, t=0, b=0), height=250)
    st.plotly_chart(fig_hist, use_container_width=True)

with c2:
    st.markdown("##### Tendência (Previsão IA)")
    # Linha Ciano/Azul claro (Simulando passado e futuro)
    meses = ['Ago', 'Set', 'Out', 'Nov', 'Dez', 'Jan (Prev)']
    valores = [18, 30, 25, 38, 48, 55]
    fig_line = px.line(x=meses, y=valores, markers=True,
                       color_discrete_sequence=['#26C6DA']) # Ciano
    fig_line.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=250)
    st.plotly_chart(fig_line, use_container_width=True)

with c3:
    st.markdown("##### Tipos de Caso")
    # Pizza com as cores exatas da imagem (Amarelo, Vermelho, Cinza, Azul, Laranja)
    cores_pizza = ['#FFEE58', '#D32F2F', '#546E7A', '#29B6F6', '#FFA726']
    fig_pie = px.pie(df_filtrado, names='Tipo', hole=0.5, color_discrete_sequence=cores_pizza)
    fig_pie.update_layout(showlegend=False, margin=dict(l=0, r=0, t=0, b=0), height=250)
    st.plotly_chart(fig_pie, use_container_width=True)

# 6. O DETERMINANTE DE IA (PEDIDO NO PDF PAG 8)
st.divider()
st.subheader("🤖 Fatores Determinantes nos Tipos de Caso (IA)")

# Simulação do gráfico de barras horizontais da parte de baixo da sua imagem
fatores = pd.DataFrame({
    'Fator': ['Localização (Bairro)', 'Horário da Ocorrência', 'Densidade Demográfica', 'Infraestrutura', 'Clima'],
    'Influencia': [0.95, 0.80, 0.65, 0.45, 0.20]
}).sort_values(by='Influencia', ascending=True)

# Gráfico de barras horizontais cinza azulado
fig_barh = px.bar(fatores, x='Influencia', y='Fator', orientation='h',
                  color_discrete_sequence=['#5C6BC0'])
fig_barh.update_layout(xaxis_title="Peso na Decisão da IA", yaxis_title="", height=300)
st.plotly_chart(fig_barh, use_container_width=True)
