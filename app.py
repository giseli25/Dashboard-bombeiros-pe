import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Bombeiros PE", layout="wide")


# Lista completa dos Municípios de Pernambuco (185) para uso no DataFrame
municipios_pe = [
    'Recife', 'Jaboatão dos Guararapes', 'Olinda', 'Caruaru', 'Petrolina',
    'Paulista', 'Cabo de Santo Agostinho', 'Camaragibe', 'Garanhuns',
    'Vitória de Santo Antão', 'Igarassu', 'São Lourenço da Mata',
    'Ipojuca', 'Santa Cruz do Capibaribe', 'Abreu e Lima', 'Serra Talhada',
    'Gravatá', 'Araripina', 'Goiana', 'Belo Jardim', 'Carpina',
    'Arcoverde', 'Ouricuri', 'Surubim', 'Salgueiro', 'Pesqueira',
    'Bezerros', 'Escada', 'Paudalho', 'Limoeiro', 'Moreno', 'Palmares',
    'Buíque', 'São Bento do Una', 'Brejo da Madre de Deus', 'Timbaúba',
    'Bom Conselho', 'Águas Belas', 'Toritama', 'Santa Maria da Boa Vista',
    'Afogados da Ingazeira', 'Barreiros', 'Lajedo', 'Custódia',
    'Bom Jardim', 'Sirinhaém', 'Bonito', 'São Caitano', 'Aliança',
    'São José do Belmonte', 'Itambé', 'Bodocó', 'Petrolândia', 'Sertânia',
    'Ribeirão', 'Itaíba', 'Exu', 'Catende', 'São José do Egito',
    'Nazaré da Mata', 'Trindade', 'Cabrobó', 'Floresta', 'Ipubi',
    'Caetés', 'Glória do Goitá', 'Passira', 'Itapissuma', 'Tabira',
    'João Alfredo', 'Ibimirim', 'Inajá', 'Vicência', 'Água Preta',
    'Tupanatinga', 'Pombos', 'Manari', 'Ilha de Itamaracá', 'Condado',
    'Canhotinho', 'Lagoa Grande', 'Tacaratu', 'São João', 'Macaparana',
    'Agrestina', 'Tamandaré', 'Cupira', 'Pedra', 'Panelas', 'Vertentes',
    'Orobó', 'Feira Nova', 'Riacho das Almas', 'Chã Grande', 'Altinho',
    'Flores', 'Cachoeirinha', 'Rio Formoso', 'São Joaquim do Monte',
    'Araçoiaba', 'Lagoa de Itaenga', 'Carnaíba', 'São José da Coroa Grande',
    'Afrânio', 'Alagoinha', 'Amaraji', 'Angelim', 'Barra de Guabiraba',
    'Belém de Maria', 'Belém do São Francisco', 'Betânia', 'Brejão',
    'Brejinho', 'Buenos Aires', 'Calçado', 'Calumbi', 'Camocim de São Félix',
    'Camutanga', 'Capoeiras', 'Carnaubeira da Penha', 'Casinhas', 'Cedro',
    'Chã de Alegria', 'Correntes', 'Cortês', 'Cumaru', 'Dormentes',
    'Ferreiros', 'Frei Miguelinho', 'Gameleira', 'Granito', 'Iati',
    'Ibirajuba', 'Iguaraci', 'Ingazeira', 'Itacuruba', 'Itapetim',
    'Itaquitinga', 'Jaqueira', 'Jataúba', 'Jatobá', 'Joaquim Nabuco',
    'Jucati', 'Jupi', 'Jurema', 'Lagoa do Carro', 'Lagoa do Ouro',
    'Lagoa dos Gatos', 'Machados', 'Maraial', 'Mirandiba', 'Moreilândia',
    'Orocó', 'Parnamirim', 'Poção', 'Ponto Novo', 'Primavera', 'Quipapá',
    'Quixaba', 'Saloá', 'Sanharó', 'Santa Cruz da Baixa Verde',
    'Santa Filomena', 'Santa Terezinha', 'São Benedito do Sul',
    'São Vicente Ferrer', 'Serra Negra do Norte', 'Serrita', 'Tacaimbó',
    'Terra Nova', 'Venturosa', 'Verdejante', 'Vertente do Lério'
]


st.markdown("""
<style>
    /* Fundo */
    .stApp { background-color: #FDFDFD; }
    
    /* Cards - Com efeito de HOVER AMARELO */
    .card {
        border-radius: 8px;
        padding: 20px;
        color: white;
        height: 140px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        font-family: 'Segoe UI', sans-serif;
        transition: transform 0.2s, border 0.2s;
        border: 2px solid transparent;
        /* FLEXBOX para alinhar o conteúdo verticalmente */
        display: flex;
        flex-direction: column;
        justify-content: space-between; 
    }
    
    /* MOUSE: Cresce e fica Amarelo */
    .card:hover {
        transform: scale(1.02);
        border: 2px solid #FFD700; 
        box-shadow: 0 8px 16px rgba(255, 215, 0, 0.3);
        cursor: pointer;
    }

    .card-label {
        font-size: 14px;
        opacity: 0.9;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 5px;
        line-height: 1.2;
    }
    
    .card-value {
        font-size: 36px;
        font-weight: bold;
        margin-top: 5px;
        line-height: 1;
    }
    
    /* Cores dos Cards */
    .bg-laranja { background-color: #F57C00; }
    .bg-azul { background-color: #3949AB; }
    .bg-vermelho { background-color: #E65100; }
    .bg-verde { background-color: #388E3C; }
    
    /* Textos Gerais */
    h3 { font-size: 18px; margin: 0; color: white !important; font-weight: 500; }

    /* NOVO: Título específico do Menu Lateral - GARANTINDO QUE SEJA PRETO */
    .sidebar-title h3 {
        color: #000000 !important; /* Cor preta */
        font-size: 20px;
        font-weight: 600;
        margin-top: 5px; /* Ajuste para o espaçamento */
    }
    
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
    
    # APLICAÇÃO DA NOVA CLASSE PARA FORÇAR O PRETO
    st.markdown('<div class="sidebar-title">### **Bombeiros PE**</div>', unsafe_allow_html=True)
    
    menu_selecionado = st.radio(
        "Menu Principal",
        ["Dashboard", "Ocorrências", "Usuários", "Auditoria"],
        index=0,
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    df_filtrado = pd.DataFrame() 

    if menu_selecionado == "Dashboard":
        with st.expander("Filtros de Dados", expanded=True):
            np.random.seed(42)
            tipos_ocorrencia = [
                'Incêndio', 'Salvamento', 'Vistoria', 'Acidente', 
                'APH', 'Produtos Perigosos', 'Improcedentes / Trotes'
            ]
            faixas = ['18-25 anos', '26-35 anos', '36-50 anos', '51-65 anos', 'Mais de 65 anos']
            
            df = pd.DataFrame({
                'Bairro': np.random.choice(municipios_pe, 1000),
                'Tipo': np.random.choice(tipos_ocorrencia, 1000),
                'Status': np.random.choice(['Concluído', 'Em Andamento', 'Aberto'], 1000),
                'Faixa Etaria': np.random.choice(faixas, 1000, p=[0.2, 0.3, 0.25, 0.15, 0.1]),
                'Risco': np.random.randint(10, 100, 1000),
                'Latitude': np.random.uniform(-8.05, -8.15, 1000),
                'Longitude': np.random.uniform(-34.88, -34.95, 1000)
            })
            
            bairro_sel = st.multiselect("Cidade / Bairro", df['Bairro'].unique(), default=['Recife', 'Caruaru', 'Petrolina'])
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
    if not df_filtrado.empty:
        v_total = len(df_filtrado)
        v_media = int(v_total/30)
        v_abertas = len(df_filtrado[df_filtrado["Status"]=="Aberto"])
        v_resolvidas = len(df_filtrado[df_filtrado["Status"]=="Concluído"])
    else:
        v_total, v_media, v_abertas, v_resolvidas = 0, 0, 0, 0
    
    # Cards com a estrutura correta (Label, Título, Valor)
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
        fig_line = px.line(x=meses, y=[10, 25, 20, 45], markers=True, color_discrete_sequence=['#5C6BC0'], labels={"y": "Ocorrências"})
        fig_line.update_layout(height=300, margin=dict(l=0, r=0, t=0, b=0), showlegend=False, xaxis_title="", yaxis_title="",
                               hoverlabel=hover_config)
        st.plotly_chart(fig_line, use_container_width=True)

    with col_g3:
        st.markdown("##### Tipos de Ocorrência")
        cores = ['#FFCA28', '#D32F2F', '#1976D2', '#FFA726', '#546E7A', '#7B1FA2', '#424242']
        
        fig_pie = px.pie(df_filtrado, names='Tipo', hole=0.4, color_discrete_sequence=cores)
        
        fig_pie.update_layout(
            height=300, margin=dict(l=0, r=0, t=0, b=0), 
            showlegend=True, 
            legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.0),
            hoverlabel=hover_config
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")

    # --- IA E FATORES ---
    c_ia1, c_ia2 = st.columns([1, 1])

    with c_ia1:
        st.markdown("##### Fatores Determinantes nos Tipos de Caso")
        fatores = pd.DataFrame({
            'Fator': ['Localização (Cidade/Bairro)', 'Horário da Ocorrência', 'Clima / Chuva', 'Infraestrutura Urbana'],
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
        
        with col_in1: local = st.selectbox("Cidade / Bairro", municipios_pe, key="bairro_simulador")
        with col_in2: tipo = st.selectbox("Ocorrência", tipos_ocorrencia, key="tipo_simulador")
        
        if st.button("Prever Risco", type="primary"):
            risco = 87
            if tipo == "Improcedentes / Trotes":
                st.warning(f"Alerta: Alta probabilidade de TROTE ({risco}%) em {local}.")
            elif tipo == "Produtos Perigosos":
                st.error(f"RISCO CRÍTICO: 95% (Vazamento Químico/Gás) em {local}.")
            else:
                st.success(f"Risco Estimado para {tipo} em {local}: ALTO ({risco}%)")
        st.markdown('</div>', unsafe_allow_html=True)

else:
    st.title("Página em Construção")
    st.info("Funcionalidade em desenvolvimento.")
