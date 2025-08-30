import pandas as pd
import streamlit as st
from PIL import Image
import plotly.express as px

st.set_page_config(
    page_title='Countries · Streamlit', 
    page_icon='📈', 
    layout='wide'
)

# Importando o dataset
df = pd.read_csv('dataset/zomato.csv', sep=',')

# Dropando valores nulos
df = df.dropna()

# Dropando valores duplicados
df = df.drop_duplicates()

# Resetando o índex
df = df.reset_index(drop=True)

# Adicionando colunas
COUNTRIES = {
    1: "India",
    14: "Australia",
    30: "Brazil",
    37: "Canada",
    94: "Indonesia",
    148: "New Zeland",
    162: "Philippines",
    166: "Qatar",
    184: "Singapure",
    189: "South Africa",
    191: "Sri Lanka",
    208: "Turkey",
    214: "United Arab Emirates",
    215: "England",
    216: "United States of America",
}
df['Country Name'] = df['Country Code'].map(COUNTRIES)
columns = df.columns.tolist()
country_name = columns.pop(columns.index('Country Name'))
columns.insert(3, country_name)
df = df[columns]

# Definir a função
def create_price_type(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"

# Aplicar a função e criar a nova coluna
df['Cuisines Category Type'] = df['Price range'].apply(create_price_type)

# Reordenar as colunas para colocar 'Cuisines Category Type' no índice 10
columns = df.columns.tolist()
columns.pop(columns.index('Cuisines Category Type'))  # Remove a coluna recém-criada
columns.insert(11, 'Cuisines Category Type')  # Insere na posição 10
df = df[columns]

#============================================================
# Funções
#============================================================
def download_csv(df, filename="data.csv"):
    csv = df.to_csv(index=False)
    return csv, filename
    
#============================================================
# Barra lateral
#============================================================
image_path = ('logo.png')
image = Image.open( image_path )
st.sidebar.image(image, width=80)
st.sidebar.markdown('## Gourmet Quest')
st.sidebar.markdown("""---""")
st.sidebar.markdown('## Filtros')


# Adicionar checkboxes para os países
selected_countries = st.sidebar.multiselect(
    'Escolha os Países que Deseja visualizar as Informações',
    options=sorted(COUNTRIES.values()),  # Lista de países ordenada
    default=sorted(COUNTRIES.values())# Padrão inicial baseado na imagem
)

# Filtrar o DataFrame com base nos países selecionados
if selected_countries:
    df_filtered = df[df['Country Name'].isin(selected_countries)]
else:
    df_filtered = df.copy()

# Exibir mensagem na barra lateral (opcional, para feedback)
st.sidebar.markdown('### Dados Tratados')
csv_data, file_name = download_csv(df_filtered, filename="data.csv")
st.sidebar.download_button(
    label="Download",
    data=csv_data,
    file_name=file_name,
    mime="text/csv"
)

#============================================================
#  Layout no Streamlit
#============================================================
st.title("🌎 Visão Países")

# GRÁFICO 1
with st.container():
    # Agrupar por 'Country Name' e contar o número de restaurantes
    df_aux = df_filtered.groupby('Country Name').size().reset_index(name='Counts')
    # Ordenar em ordem decrescente para efeito de cascata
    df_aux = df_aux.sort_values(by='Counts', ascending=False)
    # Criar gráfico de barras com Plotly
    fig = px.bar(df_aux, x='Country Name', y='Counts', 
                 title='Quantidade de Restaurantes Registrados por País', 
                 labels={'Country Name': 'Países', 'Counts': 'Quantidade de Restaurantes'},
                 color='Counts',  # Usa a contagem para gradiente de cor
                 color_continuous_scale='Blues')  # Escala de azul como no print
    # Personalizar o layout
    fig.update_layout(
        xaxis={'tickangle': 45},  # Rotacionar rótulos do eixo x
        yaxis=dict(range=[0, max(df_aux['Counts']) * 1.2]),  # Ajustar limite do eixo y
        showlegend=False  # Remover legenda, pois a cor é apenas ilustrativa
    )
    # Adicionar valores nas barras
    fig.update_traces(text=df_aux['Counts'], textposition='auto')
    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig, use_container_width=True, key="gráfico_restaurantes_pais")

st.markdown("""---""")

# GRÁFICO 2
with st.container():
    # Agrupar por 'Country Name' e contar o número único de cidades
    df_aux = df_filtered.groupby('Country Name')['City'].nunique().reset_index(name='City Count')
    # Ordenar em ordem decrescente para efeito de cascata
    df_aux = df_aux.sort_values(by='City Count', ascending=False)
    # Criar gráfico de barras com Plotly
    fig = px.bar(df_aux, x='Country Name', y='City Count', 
                 title='Quantidade de Cidades Registradas por País', 
                 labels={'Country Name': 'Países', 'City Count': 'Quantidade de Cidades'},
                 color='City Count',  # Usa a contagem para gradiente de cor
                 color_continuous_scale='plotly3') 
    # Personalizar o layout
    fig.update_layout(
        xaxis={'tickangle': 45},  # Rotacionar rótulos do eixo x
        yaxis=dict(range=[0, max(df_aux['City Count']) * 1.2]),  # Ajustar limite do eixo y
        showlegend=False  # Remover legenda, pois a cor é apenas ilustrativa
    )
    # Adicionar valores nas barras
    fig.update_traces(text=df_aux['City Count'], textposition='auto')
    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig, use_container_width=True, key="gráfico_cidades_pais")


st.markdown("""---""")

# GRÁFICO 3
with st.container():
    col1, col2 = st.columns(2)
    with col1: 
        df_aux = df_filtered[['Country Name', 'Aggregate rating']].groupby('Country Name').mean().reset_index()
        df_aux = df_aux.sort_values(by='Aggregate rating', ascending=False).round(2)
        fig = px.bar(df_aux, x='Country Name', y='Aggregate rating', 
                     title='Média de Avaliações por País', 
                     labels={'Country Name': 'Países', 'Aggregate rating': 'Média de Avaliações'},
                     color='Aggregate rating',  # Usa a contagem para gradiente de cor
                     color_continuous_scale='pubu') 
        # Personalizar o layout
        fig.update_layout(
            xaxis={'tickangle': 45},  # Rotacionar rótulos do eixo x
            yaxis=dict(range=[0, max(df_aux['Aggregate rating']) * 1.2]),  # Ajustar limite do eixo y
            showlegend=False  # Remover legenda, pois a cor é apenas ilustrativa
        )
        # Adicionar valores nas barras
        fig.update_traces(text=df_aux['Aggregate rating'], textposition='auto')
        # Exibir o gráfico no Streamlit
        st.plotly_chart(fig, use_container_width=True, key="gráfico_avaliacoes_media_pais")
        
    with col2: 
        df_aux = df[['Country Name', 'Average Cost for two']].groupby('Country Name').mean().reset_index()
        df_aux = df_aux.sort_values(by='Average Cost for two', ascending=False)
        fig = px.bar(df_aux, x='Country Name', y='Average Cost for two', 
                     title='Preço médio Prato pra 2 por País', 
                     labels={'Country Name': 'Países', 'Average Cost for two': 'Média de Preço'},
                     color='Average Cost for two',  # Usa a contagem para gradiente de cor
                     color_continuous_scale='hot') 
        # Personalizar o layout
        fig.update_layout(
            xaxis={'tickangle': 45},  # Rotacionar rótulos do eixo x
            yaxis=dict(range=[0, max(df_aux['Average Cost for two']) * 1.2]),  # Ajustar limite do eixo y
            showlegend=False  # Remover legenda, pois a cor é apenas ilustrativa
        )
        # Adicionar valores nas barras
        fig.update_traces(text=df_aux['Average Cost for two'], textposition='auto')
        # Exibir o gráfico no Streamlit
        st.plotly_chart(fig, use_container_width=True, key="gráfico_preco_2_pais")





    