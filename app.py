import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ----------------------------------------------------------------------
# FUNÇÃO DE SIMULAÇÃO DE MACHINE LEARNING
# Esta função simula a previsão de um modelo de classificação (0 a 100%)
# O risco é ajustado com base na cidade (simulando fatores geográficos)
# e no tipo de ocorrência (simulando a gravidade).
# ----------------------------------------------------------------------

def simular_previsao_risco(cidade, tipo_ocorrencia):
    """Simula a previsão de um modelo de Risco (0-100%)."""
    
    # Risco Base (simulando a previsão média do modelo)
    risco_base = 65 
    
    # 1. Ajuste por Tipo de Ocorrência (Gravidade)
    if tipo_ocorrencia == "Produtos Perigosos":
        risco_base += 30 # Risco muito alto
    elif tipo_ocorrencia == "Incêndio":
        risco_base += 15
    elif tipo_ocorrencia == "Improcedentes / Trotes":
        risco_base = 5 # Risco muito baixo (o que deve ser reportado é a probabilidade de ser Trote)
    elif tipo_ocorrencia == "APH":
        risco_base += 10

    # 2. Ajuste por Cidade (Fator Geográfico/Metropolitano)
    if cidade in ['Recife', 'Olinda', 'Jaboatão dos Guararapes']:
        risco_base += 10 # Risco ligeiramente maior em grandes centros
    elif cidade in ['Petrolina', 'Caruaru']:
        risco_base += 5
    
    # Garante que o risco esteja entre 0 e 100
    risco_final = max(0, min(100, risco_base))
    
    # Se for Trote, retorna o risco de TROTE, senão retorna o risco da OCORRÊNCIA
    if tipo_ocorrencia == "Improcedentes / Trotes":
        return 95, "Trote" # 95% de chance de ser trote
    else:
        # Adiciona uma pequena variação aleatória para simular a imprecisão do modelo
        variacao = np.random.randint(-5, 5)
        return max(10, min(100, risco_final + variacao)), "Ocorrência"

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Bombeiros PE", layout="wide")


# Mapeamento dos Municípios e Mesorregiões de PE (Amostra representativa para o filtro de região)
MAP_REGIOES = {
    'Recife': 'Metropolitana', 'Jaboatão dos Guararapes': 'Metropolitana', 'Olinda': 'Metropolitana',
    'Paulista': 'Metropolitana', 'Cabo de Santo Agostinho': 'Metropolitana', 'Camaragibe': 'Metropolitana',
    'Caruaru': 'Agreste', 'Garanhuns': 'Agreste', 'Santa Cruz do Capibaribe': 'Agreste',
    'Belo Jardim': 'Agreste', 'Vitória de Santo Antão': 'Zona da Mata', 'Goiana': 'Zona da Mata',
    'Palmares': 'Zona da Mata', 'Serra Talhada': 'Sertão', 'Arcoverde': 'Sertão', 'Salgueiro': 'Sertão',
    'Petrolina': 'São Francisco', 'Santa Maria da Boa Vista': 'São Francisco', 'Cabrobó': 'São Francisco',
}

# Lista completa dos Municípios de Pernambuco (185)
municipios_pe = list(MAP_REGIOES.keys()) + [
    'Abreu e Lima', 'Igarassu', 'São Lourenço da Mata', 'Ipojuca', 'Gravatá', 'Araripina', 'Carpina',
    'Ouricuri', 'Surubim', 'Pesqueira', 'Bezerros', 'Escada', 'Paudalho', 'Limoeiro', 'Moreno',
    'Buíque', 'São Bento do Una', 'Brejo da Madre de Deus', 'Timbaúba', 'Bom Conselho', 'Águas Belas', 
    'Toritama', 'Afogados da Ingazeira', 'Barreiros', 'Lajedo', 'Custódia', 'Bom Jardim', 
    'Sirinhaém', 'Bonito', 'São Caitano', 'Aliança', 'São José do Belmonte', 'Itambé', 'Bodocó', 
    'Petrolândia', 'Sertânia', 'Ribeirão', 'Itaíba', 'Exu', 'Catende', 'São José do Egito',
    'Nazaré da Mata', 'Trindade', 'Floresta', 'Ipubi', 'Caetés', 'Glória do Goitá', 'Passira', 
    'Itapissuma', 'Tabira', 'João Alfredo', 'Ibimirim', 'Inajá', 'Vicência', 'Água Preta',
    'Tupanatinga', 'Pombos', 'Manari', 'Ilha de Itamaracá', 'Condado', 'Canhotinho', 'Lagoa Grande', 
    'Tacaratu', 'São João', 'Macaparana', 'Agrestina', 'Tamandaré', 'Cupira', 'Pedra', 'Panelas', 
    'Vertentes', 'Orobó', 'Feira Nova', 'Riacho das Almas', 'Chã Grande', 'Altinho', 'Flores', 
    'Cachoeirinha', 'Rio Formoso', 'São Joaquim do Monte', 'Araçoiaba', 'Lagoa de Itaenga', 
    'Carnaíba', 'São José da Coroa Grande', 'Afrânio', 'Alagoinha', 'Amaraji', 'Angelim', 
    'Barra de Guabiraba', 'Belém de Maria', 'Belém do São Francisco', 'Betânia', 'Brejão',
    'Brejinho', 'Buenos Aires', 'Calçado', 'Calumbi', 'Camocim de São Félix', 'Camutanga', 
    'Capoeiras', 'Carnaubeira da Penha', 'Casinhas', 'Cedro', 'Chã de Alegria', 'Correntes', 
    'Cortês', 'Cumaru', 'Dormentes', 'Ferreiros', 'Frei Miguelinho', 'Gameleira', 'Granito', 
    'Iati', 'Ibirajuba', 'Iguaraci', 'Ingazeira', 'Itacuruba', 'Itapetim', 'Itaquitinga', 
    'Jaqueira', 'Jataúba', 'Jatobá', 'Joaquim Nabuco', 'Jucati', 'Jupi', 'Jurema', 'Lagoa do Carro', 
    'Lagoa do Ouro', 'Lagoa dos Gatos', 'Machados', 'Maraial', 'Mirandiba', 'Moreilândia', 
    'Orocó', 'Parnamirim', 'Poção', 'Ponto Novo', 'Primavera', 'Quipapá', 'Quixaba', 'Saloá', 
    'Sanharó', 'Santa Cruz da Baixa Verde', 'Santa Filomena', 'Santa Terezinha', 
    'São Benedito do Sul', 'São Vicente Ferrer', 'Serra Negra do Norte', 'Serrita', 'Tacaimbó', 
    'Terra Nova', 'Venturosa', 'Verdejante', 'Vertente do Lério'
]


# Definição dos Bairros Fictícios para simulação de filtro
BAIRROS_COMUNS = [
    'Centro', 'Boa Viagem', 'Madalena', 'Boa Vista', 'Porto', 'Caxangá', 
    'Ipsep', 'Santo Antônio', 'Casa Amarela', 'Jardim Paulista', 'Piedade',
    'Cohab', 'Sertãozinho', 'Nova Esperança', 'Agreste Novo', 'Rio Doce'
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
        height: 160px; /* AUMENTADO: Garante mais espaço e resolve o "espremido" */
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
        font-size: 48px; /* AUMENTADO: O número principal fica maior */
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

    /* Título específico do Menu Lateral - GARANTINDO QUE SEJA PRETO */
    .sidebar-title h3 {
        color: #000000 !important; 
        font-size: 20px;
        font-weight: 600;
        margin-top: 5px; 
    }
    
    /* Centraliza a imagem no sidebar (ajuste estético) */
    [data-testid="stSidebar"] img {
        display: block;
        margin-left: auto;
        margin-right: auto;
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
    # -----------------------------------------------
    # IMAGEM (BRASÃO) NO TOPO DO MENU LATERAL
    # -----------------------------------------------
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Bras%C3%A3o_CBMPE.png/120px-Bras%C3%A3o_CBMPE.png", width=60)
    
    # TÍTULO LOGO ABAIXO DA IMAGEM
    # Nota: Removi o markdown de cabeçalho '###' do HTML, pois já foi aplicado na classe .sidebar-title h3
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
            
            # --- CRIAÇÃO DO DATAFRAME COM A COLUNA DE BAIRRO ---
            df = pd.DataFrame({
                'Cidade': np.random.choice(municipios_pe, 1000),
                'Bairro': np.random.choice(BAIRROS_COMUNS, 1000), 
                'Tipo': np.random.choice(tipos_ocorrencia, 1000),
                'Status': np.random.choice(['Concluído', 'Em Andamento', 'Aberto'], 1000),
                'Faixa Etaria': np.random.choice(faixas, 1000, p=[0.2, 0.3, 0.25, 0.15, 0.1]),
                'Risco': np.random.randint(10, 100, 1000),
                'Latitude': np.random.uniform(-7.5, -9.5, 1000), 
                'Longitude': np.random.uniform(-34.8, -40.5, 1000)
            })
            
            # --- SIMULAÇÃO DE CLUSTERIZAÇÃO (4 GRUPOS) ---
            bins = [0, 40, 65, 85, 100]
            labels = ['Baixo Risco', 'Risco Moderado', 'Alto Risco', 'Risco Crítico']
            df['Cluster'] = pd.cut(df['Risco'], bins=bins, labels=labels, include_lowest=True).astype(str)
            
            # Adicionando a coluna de Região
            df['Regiao'] = df['Cidade'].apply(lambda x: MAP_REGIOES.get(x, 'Outras Regiões'))
            
            # --- FILTROS EM CASCATA ---
            
            # FILTRO 1: REGIÃO
            regiao_sel = st.multiselect("Região", df['Regiao'].unique(), 
                                        default=['Metropolitana', 'Agreste'])
            
            df_regiao = df[df['Regiao'].isin(regiao_sel)]

            # FILTRO 2: CIDADE (só exibe cidades dentro da região selecionada)
            cidade_opcoes = df_regiao['Cidade'].unique()
            cidade_sel = st.multiselect("Cidade", cidade_opcoes, 
                                        default=[c for c in ['Recife', 'Caruaru'] if c in cidade_opcoes])

            df_cidade = df_regiao[df_regiao['Cidade'].isin(cidade_sel)]
            
            # FILTRO 3: BAIRRO (só exibe bairros dentro das cidades selecionadas)
            bairro_opcoes = df_cidade['Bairro'].unique()
            bairro_sel = st.multiselect("Bairro", bairro_opcoes, 
                                        default=bairro_opcoes if len(bairro_opcoes) < 5 else bairro_opcoes[:5])

            # FILTRO FINAL
            df_filtrado = df_cidade[df_cidade['Bairro'].isin(bairro_sel)]

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
    
    # --- MAPA DE DISTRIBUIÇÃO ESPACIAL (AGORA COM PLOTLY) ---
    st.markdown("##### Distribuição Espacial das Ocorrências")
    
    if not df_filtrado.empty:
        
        # Cria o mapa de dispersão (scatter mapbox) com Plotly Express
        fig_map = px.scatter_mapbox(
            df_filtrado, 
            lat="Latitude", 
            lon="Longitude", 
            color="Tipo", 
            hover_name="Bairro", 
            zoom=7, 
            height=500,
            size_max=15, 
            size=np.ones(len(df_filtrado)), 
            mapbox_style="carto-positron" 
        )
        
        # Ajusta as cores, centro e marcadores (AUMENTA A VISIBILIDADE DOS PONTOS)
        fig_map.update_layout(
            margin={"r":0,"t":0,"l":0,"b":0},
            mapbox={
                'center': {'lat': -8.3, 'lon': -37.9}, 
                'zoom': 6.5 
            },
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig_map, use_container_width=True)
        
    else:
        st.info("Filtre pelo menos uma região, cidade ou bairro para visualizar a distribuição no mapa.")
        
    st.markdown("---") 

    # --- GRÁFICOS (3 COLUNAS) ---
    col_g1, col_g2, col_g3 = st.columns(3)

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
    
    # --- NOVO: GRÁFICO DE CLUSTERIZAÇÃO ---
    st.markdown("##### Clusterização (Agrupamento de Ocorrências)")
    
    if not df_filtrado.empty:
        # Usa o Risco (e Longitude como proxy para dispersão) e colore pelo Cluster
        fig_cluster = px.scatter(
            df_filtrado, 
            x="Risco", 
            y="Longitude", 
            color="Cluster",
            hover_name="Bairro",
            symbol="Cluster",
            size=np.ones(len(df_filtrado)) * 8, # Pontos maiores para visibilidade
            color_discrete_map={
                'Baixo Risco': '#388E3C', 
                'Risco Moderado': '#1E88E5', 
                'Alto Risco': '#F57C00', 
                'Risco Crítico': '#D32F2F'
            },
            labels={"Risco": "Risco de Ocorrência (0-100%)", "Longitude": "Localização (Eixo Y)"}
        )
        
        fig_cluster.update_traces(marker=dict(line=dict(width=0.5, color='DarkSlateGrey')))
        fig_cluster.update_layout(height=350, margin=dict(l=10, r=10, t=10, b=10), showlegend=True,
                                  hoverlabel=hover_config)
        st.plotly_chart(fig_cluster, use_container_width=True)

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
        
        with col_in1: 
            local_options = df['Cidade'].unique().tolist()
            local = st.selectbox("Cidade", local_options, key="cidade_simulador")
        
        with col_in2: tipo = st.selectbox("Ocorrência", tipos_ocorrencia, key="tipo_simulador")
        
        if st.button("Prever Risco", type="primary"):
            # CHAMA A FUNÇÃO DE SIMULAÇÃO DE MACHINE LEARNING
            risco, tipo_risco = simular_previsao_risco(local, tipo)
            
            if tipo_risco == "Trote":
                st.warning(f"Alerta: Alta probabilidade de TROTE ({risco}%) em {local}.")
            elif risco > 85:
                st.error(f"RISCO CRÍTICO: {risco}% (Ação Imediata Requerida) em {local}.")
            elif risco > 65:
                st.info(f"Risco Estimado para {tipo} em {local}: ALTO ({risco}%)")
            else:
                st.success(f"Risco Estimado para {tipo} em {local}: MODERADO ({risco}%)")
                
        st.markdown('</div>', unsafe_allow_html=True)

else:
    st.title("Página em Construção")
    st.info("Funcionalidade em desenvolvimento.")
