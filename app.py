import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Bombeiros PE", layout="wide")

# 2. CSS PARA O VISUAL (CORES E ESTILO)
st.markdown("""
<style>
    /* Fundo da aplicação */
    .stApp { background-color: #FDFDFD; }
    
    /* Estilo dos Cards (KPIs) */
    .card {
        border-radius: 8px;
        padding: 15px;
        color: white;
        height: 140px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        font-family: 'Segoe UI', sans-serif;
        position: relative;
    }
    .card-number {
        font-size: 12px;
        opacity: 0.8;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 5px;
        display: block;
    }
    
    /* Cores dos Cards (Idênticas ao print) */
    .bg-laranja { background-color: #F57C00; }
    .bg-azul { background-color: #3949AB; }
    .bg-vermelho { background-color: #E65100; }
    .bg-verde { background-color: #388E3C; }
    
    /* Tipografia dos Cards */
    h3 { font-size: 15px; margin: 0; color: white !important; font-weight: 500; }
    h2 { font-size: 34px; margin: 5px 0 0 0; color: white !important; font-weight: bold; }
    
    /* Box da Previsão */
    .prediction-box {
        background-color: #E8EAF6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #3949AB;
    }
</style>
""", unsafe_allow_html=True)

# 3. MENU LATERAL (SIDEBAR) IDÊNTICO AO PEDIDO
with st.sidebar:
    # Logo e Título
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Bras%C3%A3o_CBMPE.png/120px-Bras%C3%A3o_CBMPE.png", width=60)
    st.markdown("### **Bombeiros PE**")
    st.write("") # Espaço

    # O Menu de Navegação
    menu_selecionado = st.radio(
        "Navegação",
        ["🔥 Ocorrências", "📊 Dashboard", "👥 Usuários", "🔍 Auditoria"],
        index=1, # Já começa no Dashboard
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Filtros (Ficam escondidos ou visíveis aqui para não poluir)
    if menu_selecionado == "📊 Dashboard":
        with st.expander("🎛️ Filtros de Dados", expanded=True):
            np.random.seed(42)
            bairros_recife = ['Boa Viagem', 'Santo Amaro', 'Várzea', 'Ibura', 'Derby', 'Casa Forte', 'Pina']
            tipos_caso = ['Incêndio', 'Salvamento', 'Vistoria', 'Acidente', 'APH']
            
            # Gerando dados
            df = pd.DataFrame({
                'Bairro': np.random.choice(bairros_recife, 1000),
                'Tipo': np.random.choice(tipos_caso, 1000),
                'Status': np.random.choice(['Concluído', 'Em Andamento', 'Aberto'], 1000),
                'Risco': np.random.randint(10, 100, 1000),
                'Latitude': np.random.uniform(-8.05, -8.15, 1000),
                'Longitude': np.random.uniform(-34.88, -34.95, 1000)
            })
            
            bairro_sel = st.multiselect("Bairro", df['Bairro'].unique(), default=df['Bairro'].unique())
            df_filtrado = df[df['Bairro'].isin(bairro_sel)]

    st.markdown("---")
    # Perfil do Usuário no Rodapé (Igual ao print)
    col_perfil1, col_perfil2 = st.columns([1, 4])
    with col_perfil1:
        st.write("👤")
    with col_perfil2:
        st.caption("Logado como:")
        st.markdown("**Ana Silva - Admin**")


# 4. LÓGICA DAS PÁGINAS
if menu_selecionado == "📊 Dashboard":
    # === AQUI COMEÇA O DASHBOARD QUE JÁ FIZEMOS ===
    
    st.title("Visão Geral de Ocorrências")
    st.write("")

    # --- CARDS DE MÉTRICAS ---
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(f'<div class="card bg-laranja"><span class="card-number">Total</span><h3>Ocorrências Totais</h3><h2>{len(df_filtrado)}</h2></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="card bg-azul"><span class="card-number">Média</span><h3>Média Diária</h3><h2>{int(len(df_filtrado)/30)}</h2></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="card bg-vermelho"><span class="card-number">Atenção</span><h3>Ocorrências Abertas</h3><h2>{len(df_filtrado[df_filtrado["Status"]=="Aberto"])}</h2></div>', unsafe_allow_html=True)
    with c4: st.markdown(f'<div class="card bg-verde"><span class="card-number">Sucesso</span><h3>Resolvidas</h3><h2>{len(df_filtrado[df_filtrado["Status"]=="Concluído"])}</h2></div>', unsafe_allow_html=True)

    st.write("")
    st.write("")

    # --- GRÁFICOS PRINCIPAIS ---
    col_graf1, col_graf2, col_graf3 = st.columns([1, 1, 1])

    with col_graf1:
        st.subheader("Distribuição de Idades")
        # Histograma Azul/Roxo
        fig_hist = px.histogram(df_filtrado, x="Risco", nbins=10, color_discrete_sequence=['#5C6BC0'])
        fig_hist.update_layout(height=250, margin=dict(l=0, r=0, t=0, b=0), showlegend=False)
        st.plotly_chart(fig_hist, use_container_width=True)

    with col_graf2:
        st.subheader("Tendência (Previsão)")
        # Gráfico de Linha (Simulado)
        meses = ['Set', 'Out', 'Nov', 'Dez', 'Jan (Prev)']
        valores = [30, 45, 35, 60, 75]
        fig_line = px.line(x=meses, y=valores, markers=True)
        fig_line.update_traces(line_color='#26C6DA', line_width=3)
        fig_line.update_layout(height=250, margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig_line, use_container_width=True)

    with col_graf3:
        st.subheader("Tipos de Caso")
        # Gráfico de Rosquinha
        cores = ['#FFCA28', '#D32F2F', '#1976D2', '#FFA726', '#546E7A']
        fig_pie = px.pie(df_filtrado, names='Tipo', hole=0.6, color_discrete_sequence=cores)
        fig_pie.update_layout(height=250, margin=dict(l=0, r=0, t=0, b=0), showlegend=False)
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")

    # --- IA E DETERMINANTES ---
    c_ia1, c_ia2 = st.columns([1, 1])

    with c_ia1:
        st.subheader("🤖 Fatores Determinantes (IA)")
        st.caption("O que a Inteligência Artificial identificou como causa principal.")
        fatores = pd.DataFrame({
            'Fator': ['Localização', 'Horário', 'Clima', 'Infraestrutura'],
            'Peso': [0.85, 0.70, 0.40, 0.20]
        }).sort_values('Peso')
        
        fig_bar = px.bar(fatores, x='Peso', y='Fator', orientation='h', color_discrete_sequence=['#5C6BC0'])
        fig_bar.update_layout(height=200, margin=dict(l=0, r=0, t=0, b=0), yaxis_title="")
        st.plotly_chart(fig_bar, use_container_width=True)

    with c_ia2:
        st.subheader("🔮 Simulador de Risco Individual")
        st.markdown('<div class="prediction-box">', unsafe_allow_html=True)
        col_in1, col_in2 = st.columns(2)
        with col_in1:
            local = st.selectbox("Bairro", bairros_recife)
        with col_in2:
            tipo = st.selectbox("Ocorrência", tipos_caso)
        
        if st.button("Prever Risco Agora", type="primary"):
            risco = np.random.randint(30, 95)
            if tipo == "Incêndio": risco = max(risco, 80)
            
            if risco > 70:
                st.error(f"⚠️ ALTO RISCO DETECTADO: {risco}%")
            else:
                st.success(f"✅ Risco Moderado: {risco}%")
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # --- PÁGINAS EM CONSTRUÇÃO (Só para o menu funcionar visualmente) ---
    st.title(f"{menu_selecionado}")
    st.info("Esta página está disponível apenas para usuários administradores ou será implementada na próxima versão.")
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Bras%C3%A3o_CBMPE.png/200px-Bras%C3%A3o_CBMPE.png", width=150)
