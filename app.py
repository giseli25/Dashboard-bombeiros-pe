import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Configuração da página para ocupar toda a largura
st.set_page_config(page_title="Bombeiros PE", layout="wide")

# --- CSS PARA FORÇAR AS CORES (A GAMBIARRA) ---
st.markdown("""
<style>
    /* Cor de fundo geral */
    .stApp {
        background-color: #F5F5F5;
    }
    /* Estilo dos Cards do Topo */
    div[data-testid="column"] {
        background-color: transparent;
    }
    .card-laranja {
        background-color: #FF6F00;
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .card-azul {
        background-color: #3F51B5;
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .card-vermelho {
        background-color: #FF5722;
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .card-verde {
        background-color: #388E3C;
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    h3 { margin: 0; font-size: 16px; }
    h2 { margin: 0; font-size: 30px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR (Barra Lateral) ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Bras%C3%A3o_CBMPE.png/120px-Bras%C3%A3o_CBMPE.png", width=100)
    st.title("Bombeiros PE")
    st.markdown("---")
    st.write("🔥 Ocorrências")
    st.write("📊 Dashboard")
    st.write("👥 Usuários")
    st.write("🔍 Auditoria")

# --- TÍTULO ---
st.header("Visão Geral de Ocorrências")

# --- DADOS FAKES ---
df = pd.DataFrame({
    'Idade': np.random.randint(18, 80, 200),
    'Tipo': np.random.choice(['APH', 'Incêndio', 'Salvamento', 'Vistoria'], 200),
    'Status': np.random.choice(['Aberto', 'Resolvido'], 200),
    'Mês': np.random.choice(['Jan', 'Fev', 'Mar', 'Abr', 'Mai'], 200)
})

# --- CARDS COLORIDOS DO TOPO (HTML INJETADO) ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
        <div class="card-laranja">
            <h3>Ocorrências Totais</h3>
            <h2>{len(df)}</h2>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="card-azul">
            <h3>Média Diária</h3>
            <h2>{np.random.randint(10, 30)}</h2>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="card-vermelho">
            <h3>Ocorrências Abertas</h3>
            <h2>{len(df[df['Status']=='Aberto'])}</h2>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
        <div class="card-verde">
            <h3>Resolvidas</h3>
            <h2>{len(df[df['Status']=='Resolvido'])}</h2>
        </div>
    """, unsafe_allow_html=True)

st.write("") # Espaço vazio
st.write("") 

# --- GRÁFICOS (PLOTLY) PARA FICAR COM AS CORES CERTAS ---
c1, c2 = st.columns([2, 1]) # Coluna da esquerda maior, direita menor

with c1:
    st.subheader("Distribuição de Idades")
    # Histograma Azul igual da imagem
    fig_hist = px.histogram(df, x="Idade", nbins=10, color_discrete_sequence=['#3F51B5'])
    fig_hist.update_layout(bargap=0.1)
    st.plotly_chart(fig_hist, use_container_width=True)

with c2:
    st.subheader("Tipos de Ocorrência")
    # Gráfico de Rosquinha Colorido
    contagem_tipos = df['Tipo'].value_counts().reset_index()
    contagem_tipos.columns = ['Tipo', 'Quantidade']
    
    # Cores personalizadas: Amarelo, Vermelho, Cinza, Azul, Laranja
    cores = ['#FFC107', '#D32F2F', '#757575', '#1976D2', '#F57C00']
    
    fig_pie = px.pie(contagem_tipos, values='Quantidade', names='Tipo', hole=0.5, 
                     color_discrete_sequence=cores)
    fig_pie.update_layout(showlegend=False) # Esconde legenda pra ficar igual a imagem
    st.plotly_chart(fig_pie, use_container_width=True)

# --- GRÁFICO DE LINHA (MACHINE LEARNING/PREVISÃO) ---
st.subheader("Tendência Temporal (Previsão)")
dados_linha = pd.DataFrame({
    'Mes': ['Ago', 'Set', 'Out', 'Nov', 'Dez'],
    'Ocorrencias': [18, 25, 20, 35, 42],
    'Previsao': [None, None, None, 38, 45] # Linha pontilhada simulada
})

# Gráfico de linha azul claro
fig_line = px.line(dados_linha, x='Mes', y=['Ocorrencias'], markers=True, 
                   color_discrete_sequence=['#00BCD4'])
st.plotly_chart(fig_line, use_container_width=True)
