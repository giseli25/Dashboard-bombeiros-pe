import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Bombeiros PE", layout="wide")


st.markdown("""
<style>
    /* Fundo */
    .stApp { background-color: #FDFDFD; }
    
    /* Cards - Com efeito de HOVER AMARELO */
    .card {
        border-radius: 8px;
        padding: 20px;
        color: white;
        height: 140px; /* Altura ajustada para o número caber folgado */
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        font-family: 'Segoe UI', sans-serif;
        transition: transform 0.2s, border 0.2s;
        border: 2px solid transparent;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    /* MOUSE: Cresce e fica Amarelo */
    .card:hover {
        transform: scale(1.02);
        border: 2px solid #FFD700; /* Borda AMARELA */
        box-shadow: 0 8px 16px rgba(255, 215, 0, 0.3);
        cursor: pointer;
    }

    .card-label {
        font-size: 14px;
        opacity: 0.9;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 5px;
    }
    
    .card-value {
        font-size: 36px;
        font-weight: bold;
        margin-top: 5px;
    }
    
    /* Cores dos Cards */
    .bg-laranja { background-color: #F57C00; }
    .bg-azul { background-color: #3949AB; }
    .bg-vermelho { background-color: #E65100; }
    .bg-verde { background-color: #388E3C; }
    
    /* Textos Gerais */
    h3 { font-size: 14px; margin: 0; color: white !important; font-weight: 500; }
    
    /* Box da Previsão */
    .prediction-box {
        background-color: #E8EAF6;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #3949AB;
    }
</style>
""", unsafe_allow_html=True)

# 3. MENU LATERAL
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Bras%C3%A3o_CBMPE.png/120px-Bras%C3%A3o_CBMPE.png", width=60)
    st.markdown("### **Bombeiros PE**")
    
    menu_selecionado = st.radio(
        "Menu Principal",
        ["Dashboard", "Ocorrências", "Usuários", "Auditoria"],
        index=0,
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    if menu_selecionado == "Dashboard":
        with st.expander("Filtros de Dados", expanded=True):
            # SEED 42 GARANTE QUE OS NÚMEROS SEJAM SEMPRE OS MESMOS (1000, 33...)
            np.random.seed(42)
            tipos_ocorrencia = [
                'Incêndio', 'Salvamento', 'Vistoria', 'Acidente', 
                'APH', 'Produtos Perigosos', 'Improcedentes / Trotes'
            ]
            faixas = ['18-25 anos', '26-35 anos', '36-50 anos', '51-65 anos', 'Mais de 65 anos']
            
            # Gerando EXATAMENTE 1000 linhas para bater com seu print
            df = pd.DataFrame({
                'Bairro': np.random.choice(['Boa Viagem', 'Santo Amaro', 'Várzea', 'Ibura', 'Derby'], 1000),
                'Tipo': np.random.choice(tipos_ocorrencia, 1000),
                'Status': np.random.choice(['Concluído', 'Em Andamento', 'Aberto'], 1000),
                'Faixa Etaria': np.random.choice(faixas, 1000, p=[0.2, 0.3, 0.25, 0.15, 0.1]),
                'Risco': np.random.randint(10, 100, 1000),
                'Latitude': np.random.uniform(-8.05, -8.15, 1000),
                'Longitude': np.random.uniform(-34.88, -34.95, 1000)
            })
            
            bairro_sel = st.multiselect("Bairro", df['Bairro'].unique(), default=df['Bairro'].unique())
            df_filtrado = df[df['Bairro'].isin(bairro_sel)]

    st.markdown("---")
    col_p1, col_p2 = st.columns([1, 4])
    with col_p1: st.write("👤")
    with col_p2: 
        st.caption("Logado como:")
        st.markdown("**Ana Silva - Admin**")

# 4. DASHBOARD
if menu_selecionado == "Dashboard":
    st.title("Visão Geral de Ocorrências")
    
    # --- CARDS COM NÚMEROS FICTÍCIOS MAS REAIS (DADOS DO DATAFRAME) ---
    c1, c2, c3, c4 = st.columns(4)
    
    # Cálculos
    v_total = len(df_filtrado)
    v_media = int(v_total/30)
    v_abertas = len(df_filtrado[df_filtrado["Status"]=="Aberto"])
    v_resolvidas = len(df_filtrado[df_filtrado["Status"]=="Concluído"])
    
    with c1: st.markdown(f'<div class="card bg-laranja"><span class="card-label">Total</span><h3>Ocorrências Totais</h3><div class="card-value">{v_total}</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="card bg-azul"><span class="card-label">Média</span><h3>Média Diária</h3><div class="card-value">{v_media}</div></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="card bg-vermelho"><span class="card-label">Atenção</span><h3>Ocorrências Abertas</h3><div class="card-value">{v_abertas}</div></div>', unsafe_allow_html=True)
    with c4: st.markdown(f'<div class="card bg-verde"><span class="card-label">Sucesso</span><h3>Resolvidas</h3><div class="card-value">{v_resolvidas}</div></div>', unsafe_allow_html=True)

    st.write("")
    
    # --- GRÁFICOS ---
    col_g1, col_g2, col_g3 = st.columns(3)

    # Config do Hover Amarelo
    hover_config = dict(bgcolor="#FFD700", font_size=14, font_family="Arial", font_color="black")

    with col_g1:
        st.markdown("##### Distribuição de Idades")
        contagem_faixa = df_filtrado['Faixa Etaria'].value_counts().reset_index()
        contagem_faixa.columns = ['Faixa', 'Qtd']
        ordem = ['18-25 anos', '26-35 anos', '36-50 anos', '51-65 anos', 'Mais de 65 anos']
        
        fig_hist = px.bar(contagem_faixa, x='Faixa', y='Qtd', category_orders={'Faixa': ordem},
                          color_discrete_sequence=['#5C6BC0'])
        fig_hist.update_layout(xaxis_title="", yaxis_title="Qtd", height=300, margin=dict(l=0, r=0, t=0, b=0),
                               hoverlabel=hover_config)
        st.plotly_chart(fig_hist, use_container_width=True)

    with col_g2:
        st.markdown("##### Evolução (Dezembro 2025)")
        meses = ['Semana 1', 'Semana 2', 'Semana 3', 'Semana 4']
        fig_line = px.line(x=meses, y=[10, 25, 20, 45], markers=True)
        fig_line.add_scatter(x=meses, y=[5, 15, 35, 30], mode='lines+markers', name='Série 2', line=dict(color='#26C6DA'))
        fig_line.add_scatter(x=meses, y=[15, 10, 25, 40], mode='lines+markers', name='Série 3', line=dict(color='#1E88E5'))
        fig_line.update_layout(height=300, margin=dict(l=0, r=0, t=0, b=0), showlegend=False, xaxis_title="", yaxis_title="",
                               hoverlabel=hover_config)
        st.plotly_chart(fig_line, use_container_width=True)

    with col_g3:
        st.markdown("##### Tipos de Ocorrência")
        cores = ['#FFCA28', '#D32F2F', '#1976D2', '#FFA726', '#546E7A', '#7B1FA2', '#424242']
        
        # ROSCA AJUSTADA: Buraco menor (0.4) e Legenda Clicável (showlegend=True)
        fig_pie = px.pie(df_filtrado, names='Tipo', hole=0.4, color_discrete_sequence=cores)
        
        fig_pie.update_layout(
            height=300, margin=dict(l=0, r=0, t=0, b=0), 
            showlegend=True, # Bolinhas clicáveis
            legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.0),
            hoverlabel=hover_config # Hover Amarelo
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")

    # --- IA E FATORES ---
    c_ia1, c_ia2 = st.columns([1, 1])

    with c_ia1:
        st.markdown("##### Fatores Determinantes nos Tipos de Caso")
        fatores = pd.DataFrame({
            'Fator': ['Localização (Bairro)', 'Horário da Ocorrência', 'Clima / Chuva', 'Infraestrutura Urbana'],
            'Peso': [0.85, 0.70, 0.40, 0.20]
        }).sort_values('Peso')
        
        fig_bar = px.bar(fatores, x='Peso', y='Fator', orientation='h', color_discrete_sequence=['#5C6BC0'])
        fig_bar.update_layout(height=250, margin=dict(l=0, r=0, t=0, b=0), yaxis_title="", xaxis_title="Influência",
                              hoverlabel=hover_config)
        st.plotly_chart(fig_bar, use_container_width=True)

    with c_ia2:
        st.markdown("##### Simulador de Risco (IA)")
        st.markdown('<div class="prediction-box">', unsafe_allow_html=True)
        col_in1, col_in2 = st.columns(2)
        with col_in1: local = st.selectbox("Bairro", df['Bairro'].unique())
        with col_in2: tipo = st.selectbox("Ocorrência", df['Tipo'].unique())
        
        if st.button("Prever Risco", type="primary"):
            risco = 87
            if tipo == "Improcedentes / Trotes":
                st.warning(f"Alerta: Alta probabilidade de TROTE ({risco}%) nesta região.")
            elif tipo == "Produtos Perigosos":
                st.error(f"RISCO CRÍTICO: 95% (Vazamento Químico/Gás)")
            else:
                st.success(f"Risco Estimado para {tipo} em {local}: ALTO ({risco}%)")
        st.markdown('</div>', unsafe_allow_html=True)

else:
    st.title("Página em Construção")
    st.info("Funcionalidade em desenvolvimento.")
