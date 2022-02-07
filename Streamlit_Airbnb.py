import streamlit as st
import pandas as pd
import pydeck as pdk
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image
import plotly.express as px

# Adicionando uma imagem
image = Image.open('airbnb-logo-2-1.png')
st.sidebar.image(image,use_column_width=True)

DATA_URL = 'http://data.insideairbnb.com/spain/catalonia/barcelona/2022-01-09/visualisations/listings.csv'

@st.cache
def load_data():
    data = pd.read_csv(DATA_URL, index_col='id')
    data['last_review'] = pd.to_datetime(data.last_review)

    return data

# Carregar os dados
df = load_data()
labels = df.room_type.unique().tolist()

# SIDEBAR
# Parâmetros e números de ocorrências
st.sidebar.header('Parâmetros')
info_sidebar = st.sidebar.empty()
# st.sidebar.info('Análise dos dados de hospedagem e aluguel de imóveis disponibilizados pelo Airbnb relacionados a cidade de Barcelona, da Espanha. Projeto de Data Science voltado para a análise exploratória e explanatória.')

# Slider de seleção do ano
st.sidebar.subheader('Ano')
year_to_filter = st.sidebar.slider('Escolha a última visualização:', 2011, 2022, 2021)

# Checkbox da tabela
st.sidebar.markdown('# Classificação')
st.sidebar.subheader('Tabela')
tabela = st.sidebar.empty()


# Multiselect com os labels únicos dos tipos de quartos
label_to_filter = st.sidebar.multiselect(
    label='Escolha o tipo de quarto:',
    options=labels,
    default=labels
)



# Informações no rodapé da Sidebar
st.sidebar.markdown("""
Todos os dados usados aqui foram obtidos a partir do site [Inside Airbnn](http://insideairbnb.com/get-the-data.html)

Para esta análise exploratória inicial, será baixado apenas o seguinte:

`listings.csv` - Summary information and metrics for listings in Barcelona (good for visualisations).
""")

# Somente aqui os dados filtrados por ano são atualizados em novos dataframe
filtered_df = df[(df.last_review.dt.year == year_to_filter) & (df.room_type.isin(label_to_filter))]

# Aqui o placeholder vazio finalmente é atualizado com dados do filtered_df
info_sidebar.info('{} bairros selecionados.'.format(filtered_df.shape[0]))


# Main
st.title('Airbnb - Barcelona, Espanha 🏨')
st.markdown(f"""
    Estão sendo exibidas os alugueis disponíveis na cidade de Barcelona **{", ".join(label_to_filter)}**
    visualizado no ano de **{year_to_filter}**.
""")

# Raw data
if tabela.checkbox('Mostrar a tabela de dados'):
    st.write(filtered_df)

# Mapa
st.subheader("Mapa de quartos alugados em Barcelona")
st.map(filtered_df)

# Gráfico de barra
#st.sidebar.markdown('# Filtro para o gráfico')

# Categoria do gráfico
#categoria_grafico = st.sidebar.selectbox('Selecione o bairro para aprensetar no gráfico', options=df.room_type.unique())


# Bairros
bairros = df.groupby('neighbourhood_group')

# Novo dataframe com os bairros e seus preços médios
novo = pd.DataFrame(index=[0,1,2,3,4,5,6,7,8,9])
novo['Bairro'] = df.neighbourhood_group.unique()
novo['Preco'] = [data.price.mean() for bairro, data in bairros]
novo.sort_values(by=['Preco'], ascending=False, inplace=True)
novo.reset_index(inplace=True)
novo.drop(columns=['index'], inplace=True)
novo = novo.set_index('Bairro')


# Valores ausentes
valores_nan = pd.DataFrame(df.isnull().sum())
valores_nan.reset_index(inplace=True)
valores_nan.rename(columns={'index': 'Coluna', 0: 'Valores NaN'}, inplace=True)

# Gráfico dos valores ausentes
st.markdown('## Dados faltantes')
fig = px.bar(x=valores_nan['Valores NaN'], y=valores_nan.Coluna, orientation='h', labels={'x': 'Quantidade', 'y':'Colunas'})
st.plotly_chart(fig)

# Gráfico preço médio por bairro
st.markdown('## Preço médio por bairro')
st.bar_chart(novo.Preco)

# Referências, adicionando sidebar
st.sidebar.markdown('\n')
st.sidebar.markdown('\n')
st.sidebar.markdown('\n')
st.sidebar.markdown('\n')
st.sidebar.markdown('Feito por: Igor Leonel')

st.sidebar.markdown('\n')
st.sidebar.markdown("Redes Sociais :")
st.sidebar.markdown("- [Linkedin](https://www.linkedin.com/in/igorleonel/)")
st.sidebar.markdown("- [Notion](https://quickest-egg-336.notion.site/Igor-Leonel-56584b6cca804e35a9fc9b75bc5a8ec6)")
st.sidebar.markdown("- [Github](https://github.com/igorleonel)")
st.sidebar.markdown("- [Medium](https://medium.com/@igorleonelborba)")

st.sidebar.markdown('\n')
st.sidebar.markdown('\n')
st.sidebar.markdown('Acesso o código: [GitHub](https://github.com/igorleonel/DataScience/blob/main/Streamlit_Airbnb.py)')







