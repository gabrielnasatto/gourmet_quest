import pandas as pd
import streamlit as st
from PIL import Image
import plotly.express as px

st.set_page_config(
    page_title='Cities · Streamlit', 
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
st.title("🏙️ Visão Cidades")

# GRÁFICO 1
with st.container():
    # Agrupar por 'City' e contar o número de restaurantes, limitando a top 10
    df_aux = df_filtered[['City', 'Restaurant ID']].groupby('City').count().reset_index()
    df_aux = df_aux.sort_values(by='Restaurant ID', ascending=False).head(10)  # Ordenar e pegar os 10 primeiros
    # Criar gráfico de barras com Plotly
    fig = px.bar(df_aux, x='City', y='Restaurant ID', 
                 title='Top 10 cidades com mais Restaurantes', 
                 labels={'City': 'Cidades', 'Restaurant ID': 'Qtd Restaurantes'},
                 color='Restaurant ID',  # Usa a contagem para gradiente de cor
                 color_continuous_scale='pubu') 
    # Personalizar o layout
    fig.update_layout(
        xaxis={'tickangle': 45},  # Rotacionar rótulos do eixo x
        yaxis=dict(range=[0, max(df_aux['Restaurant ID']) * 1.2]),  # Ajustar limite do eixo y
        showlegend=False  # Remover legenda, pois a cor é apenas ilustrativa
    )
    # Adicionar valores nas barras
    fig.update_traces(text=df_aux['Restaurant ID'], textposition='auto')
    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig, use_container_width=True, key="gráfico_restaurantes_cidades")

st.markdown("""---""")

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        # Agrupar por 'City' e contar o número de restaurantes, limitando a top 10
        df_aux = df_filtered[['City', 'Aggregate rating']].groupby('City').mean().reset_index()
        df_aux = df_aux.sort_values(by='Aggregate rating', ascending=False).head(5).round(2)  # Ordenar e pegar os 10 primeiros
        # Criar gráfico de barras com Plotly
        fig = px.bar(df_aux, x='City', y='Aggregate rating', 
                     title='Top 5 Cidades com maior média', 
                     labels={'City': 'Cidades', 'Aggregate rating': 'Média'},
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
        st.plotly_chart(fig, use_container_width=True, key="gráfico_cidades_media_restaurantes")
    with col2:
        # Agrupar por 'City' e contar o número de restaurantes, limitando a top 10
        df_aux = df_filtered[['City', 'Aggregate rating']].groupby('City').mean().reset_index()
        df_aux = df_aux.sort_values(by='Aggregate rating', ascending=True).head(5).round(2) # Ordenar e pegar os 10 primeiros
        # Criar gráfico de barras com Plotly
        fig = px.bar(df_aux, x='City', y='Aggregate rating', 
                     title='Top 5 Cidades com menor média', 
                     labels={'City': 'Cidades', 'Aggregate rating': 'Média'},
                     color='Aggregate rating',  # Usa a contagem para gradiente de cor
                     color_continuous_scale='blackbody') 
        # Personalizar o layout
        fig.update_layout(
            xaxis={'tickangle': 45},  # Rotacionar rótulos do eixo x
            yaxis=dict(range=[0, max(df_aux['Aggregate rating']) * 1.2]),  # Ajustar limite do eixo y
            showlegend=False  # Remover legenda, pois a cor é apenas ilustrativa
        )
        # Adicionar valores nas barras
        fig.update_traces(text=df_aux['Aggregate rating'], textposition='auto')
        # Exibir o gráfico no Streamlit
        st.plotly_chart(fig, use_container_width=True, key="gráfico_cidades_media_restaurantes_baixo")

st.markdown("""---""")

with st.container():
    df_exploded = df_filtered['Cuisines'].str.split(', ').explode()
    country_cuisine_count = df_exploded.groupby(df['City']).nunique().reset_index(name='Unique Cuisine Count')
    # Juntar com o DataFrame original para obter o nome do restaurante e outras informações
    country_cuisine_count = country_cuisine_count.sort_values(by='Unique Cuisine Count', ascending=False).head(10)
    fig = px.bar(country_cuisine_count, x='City', y='Unique Cuisine Count', 
                 title='Cidades com mais tipos de culinária distintos', 
                 labels={'City': 'Cidade', 'Unique Cuisine Count': 'Tipos Culinários'},
                 color='Unique Cuisine Count',  # Usa a contagem para gradiente de co
                 color_continuous_scale='greens') 
    # Personalizar o layout
    fig.update_layout(
    xaxis={'tickangle': 45},  # Rotacionar rótulos do eixo x
    yaxis=dict(range=[0, max(country_cuisine_count['Unique Cuisine Count'])]),  # Ajustar limite do eixo y
    showlegend=False  # Remover legenda, pois a cor é apenas ilustrativa
    )
    # Adicionar valores nas barras
    fig.update_traces(text=country_cuisine_count['Unique Cuisine Count'], textposition='auto')
    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig, use_container_width=True, key="gráfico_cidades_tipos_culinários")