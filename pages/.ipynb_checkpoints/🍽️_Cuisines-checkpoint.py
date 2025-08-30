import pandas as pd
import streamlit as st
from PIL import Image
import plotly.express as px

st.set_page_config(
    page_title='Cuisines · Streamlit', 
    page_icon='📈', 
    layout='wide')

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
def top_tipos_culinarios(x):
    df_aux = df_filtered['Cuisines'].str.split(', ').explode().reset_index()
    df_aux = (
        df_aux.groupby('Cuisines')
        .size()
        .reset_index(name='Counts')
        .sort_values(by='Counts', ascending=False)
        .head(x)
    )
    return df_aux['Cuisines'].tolist()  # <-- retorna lista de strings

def top10_culinarias(x):
    df_exploded = df_filtered['Cuisines'].str.split(', ').explode()
    df_exploded_with_rating = df_exploded.to_frame().merge(df_filtered['Aggregate rating'], left_index=True, right_index=True)
    df_aux = df_exploded_with_rating.groupby('Cuisines')['Aggregate rating'].mean().reset_index()
    ascending_value = False if x.lower() == 'melhores' else True if x.lower() == 'piores' else False
    df_aux = df_aux.sort_values(by='Aggregate rating', ascending=ascending_value).head(10).round(2)

    fig = px.bar(df_aux, x='Cuisines', y='Aggregate rating',
                 title=f'Top 10 Tipos de Culinária por Média de Notas ({x})',
                 labels={'Cuisines': 'Tipos de Culinária', 'Aggregate rating': 'Média de Notas'},
                 text='Aggregate rating')
    fig.update_layout(
        xaxis=dict(tickangle=45),
        yaxis=dict(range=[0, df_aux['Aggregate rating'].max() * 1.1]),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=50, b=50)
    )
    fig.update_traces(textposition='auto')
    st.plotly_chart(fig, use_container_width=True, key=f"top_10_cuisines_chart_{x}")

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

# Exemplo de uso (descomente para testar)
# top10_culinarias('melhores')  # Para os melhores
# top10_culinarias('piores')    # Para os piores
#============================================================
#  Layout no Streamlit
#============================================================
st.title("🍽️ Visão Tipos de Cozinhas")
st.markdown("""---""")
#CONTAINER 1
with st.container():
    st.header("Melhores restaurantes dos principais tipos culinários")
    selected_cuisines = st.multiselect(
    'Escolha os tipos culinários que deseja visualizar',
    options=sorted(df_filtered['Cuisines'].str.split(', ').explode().unique()),
    default=sorted(top_tipos_culinarios(5))
)

    # Filtro por países
    if selected_countries:
        df_filtered = df[df['Country Name'].isin(selected_countries)]
    else:
        df_filtered = df.copy()
    
    # Filtro por tipos culinários
    if selected_cuisines:
        df_filtered = df_filtered[
            df_filtered['Cuisines'].apply(
                lambda x: any(cuisine in x for cuisine in selected_cuisines)
            )
        ]
    # Top 10 restaurantes combinando nota média e quantidade de avaliações
    # Agrupar por 'Restaurant Name' e agregar as métricas e colunas adicionais
    df_rest = (
        df_filtered.groupby("Restaurant Name")
        .agg(
            Nota_Media=("Aggregate rating", "mean"),
            Total_Avaliacoes=("Aggregate rating", "count"),
            Country_Name=("Country Name", "first"),    # Pega o primeiro 'Country Name'
            City=("City", "first"),                   # Pega o primeiro 'City'
            Cuisines=("Cuisines", "first")            # Pega o primeiro 'Cuisines'
        )
        .reset_index()
    )
    
    # Filtra só restaurantes com pelo menos 10 avaliações
    df_rest = df_rest[df_rest["Total_Avaliacoes"] >= 10]
    
    # Ordena pelos melhores
    df_rest = df_rest.sort_values(
        by=["Nota_Media", "Total_Avaliacoes"],
        ascending=[False, False]
    ).head(10)
    
    # Exibir o resultado no Streamlit
    st.subheader("Top 10 Restaurantes (10 avaliações mínimo)")
    st.dataframe(df_rest)

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        top10_culinarias('melhores')
    with col2: 
        top10_culinarias('piores')  