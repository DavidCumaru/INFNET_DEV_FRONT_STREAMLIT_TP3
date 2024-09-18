import streamlit as st
import pandas as pd
import plotly.express as px

# Explicação do Objetivo e Motivação:
st.title("Dashboard de Análise de Dados de Turismo")
st.write("""
Foi desenvolvido com o objetivo de permitir a análise interativa de dados de turismo. https://www.data.rio/documents/04d5bb74aa254d0bae11206e3c7771aa/about
Diária média, gasto médio e permanência média por dia do visitante hospedado em hotéis do Município do Rio de Janeiro entre 1997-2002.
""")

# Função para carregar o arquivo CSV 
@st.cache_data
def carregar_dados(uploaded_file):
    if uploaded_file.name.endswith('.csv'):
        return pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith('.xls') or uploaded_file.name.endswith('.xlsx'):
        return pd.read_excel(uploaded_file)
    else:
        return None

# Realizar upload do arquivo
uploaded_file = st.file_uploader("Escolha um arquivo CSV ou Excel", type=["csv", "xls", "xlsx"])

# Barra de Progresso e Spinner
if uploaded_file is not None:
    with st.spinner('Carregando dados...'):
        dados = carregar_dados(uploaded_file)
        if dados is not None:
            st.success('Dados carregados com sucesso!')
        else:
            st.error('Formato de arquivo não suportado!')

# Dados e Seleção
if uploaded_file is not None and dados is not None:
    st.subheader('Filtrar Dados')
    colunas = st.multiselect("Selecione as colunas para exibir", options=dados.columns, default=dados.columns)

# Dados filtrados
if colunas:
    dados_filtrados = dados[colunas]
    st.subheader("Tabela de Dados")
    st.dataframe(dados_filtrados)

# Métricas Básicas
    st.subheader("Métricas Básicas")
    st.write("Total de registros:", len(dados_filtrados))

# Serviço de Download 
    csv = dados_filtrados.to_csv(index=False)
    st.download_button(label="Baixar dados filtrados em CSV", data=csv, file_name="dados_filtrados.csv", mime="text/csv")

# Visualizações de Dados
    st.subheader("Gráficos Simples")
    grafico_tipo = st.selectbox("Selecione o tipo de gráfico", options=["Barras", "Linhas", "Pizza"])
    coluna_grafico = st.selectbox("Selecione a coluna para o gráfico", options=colunas)

    if grafico_tipo == "Barras":
        st.bar_chart(dados_filtrados[coluna_grafico])
    elif grafico_tipo == "Linhas":
        st.line_chart(dados_filtrados[coluna_grafico])
    elif grafico_tipo == "Pizza":
        fig_pizza = px.pie(dados_filtrados, names=coluna_grafico, title=f"Gráfico de Pizza - {coluna_grafico}")
        st.plotly_chart(fig_pizza)

# Visualização de Dados - Gráficos Avançados 
    st.subheader("Gráficos Avançados")
    if st.checkbox("Exibir histograma"):
        coluna_hist = st.selectbox("Selecione a coluna para o histograma", options=colunas, key="hist")
        fig_hist = px.histogram(dados_filtrados, x=coluna_hist, title=f"Histograma - {coluna_hist}")
        st.plotly_chart(fig_hist)

    if st.checkbox("Exibir scatter plot"):
        coluna_x = st.selectbox("Selecione a coluna X", options=colunas, key="scatter_x")
        coluna_y = st.selectbox("Selecione a coluna Y", options=colunas, key="scatter_y")
        fig_scatter = px.scatter(dados_filtrados, x=coluna_x, y=coluna_y, title=f"Scatter Plot - {coluna_x} vs {coluna_y}")
        st.plotly_chart(fig_scatter)

# Color Picker
st.sidebar.subheader("Personalizar Visual")
cor_fundo = st.sidebar.color_picker("Escolha a cor de fundo", "#FFFFFF")
cor_texto = st.sidebar.color_picker("Escolha a cor do texto", "#000000")

# Aplicar cores
st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {cor_fundo};
        color: {cor_texto};
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Session State para filtros
if 'filtros' not in st.session_state:
    st.session_state['filtros'] = {}

# Session State
st.session_state['filtros']['colunas_selecionadas'] = colunas