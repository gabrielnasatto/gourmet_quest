import pandas as pd
import streamlit as st
from PIL import Image
import folium
from streamlit_folium import folium_static

st.set_page_config(
    page_title="Home · Streamlit",
    page_icon="📊",
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

def country_maps(df_filtered):
    # Agrupar por cidade e calcular a mediana de latitude e longitude
    df_aux = df_filtered.loc[:, ['City', 'Country Name', 'Latitude', 'Longitude']].groupby(['City', 'Country Name']).median().reset_index()
    
    # Criar o mapa base centrado na média das coordenadas
    map = folium.Map(location=[df_aux['Latitude'].mean(), df_aux['Longitude'].mean()], zoom_start=2)
    
    # Adicionar marcadores para cada cidade
    for index, location_info in df_aux.iterrows():
        folium.Marker(
            [location_info['Latitude'], location_info['Longitude']],
            popup=f"City: {location_info['City']}<br>Country: {location_info['Country Name']}"
        ).add_to(map)
    
    # Exibir o mapa no Streamlit
    folium_static(map, width=1024, height=600)
    
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
st.title("Gouermet Quest!")
st.header("O Melhor lugar para encontrar seu mais novo restaurante favorito!")
st.subheader("Temos as seguintes marcas dentro da nossa plataforma:")

with st.container():
        st.markdown("""---""")
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.markdown('###### Restaurantes Cadastrados')
            restaurantes_cadastrados = df_filtered['Restaurant ID'].nunique()
            col1.metric('', restaurantes_cadastrados,label_visibility='collapsed')
        with col2:
            st.markdown('###### Países Cadastrados')
            paises_cadastrados = df_filtered['Country Code'].nunique()
            col2.metric('', paises_cadastrados,label_visibility='collapsed')
        with col3:
            st.markdown('###### Cidades Cadastradas')
            cidades_cadastrados = df_filtered['City'].nunique()
            col3.metric('', cidades_cadastrados,label_visibility='collapsed')
        with col4:
            st.markdown('###### Avaliações Feitas na Plataforma')
            avaliacoes_feitas = df_filtered['Votes'].sum()
            col4.metric('', avaliacoes_feitas,label_visibility='collapsed')
        with col5:
            st.markdown('###### Tipos de Culinária Oferecidas')
            tipos_culinaria = df_filtered['Cuisines'].str.split(', ').explode().nunique()
            col5.metric('', tipos_culinaria,label_visibility='collapsed')
st.markdown("""---""")

with st.container():
    country_maps(df_filtered)