import streamlit as st
import os
import tweepy
import re

# -- Set page config
apptitle = 'Blue Bird Words'
st.set_page_config(page_title=apptitle, page_icon=":cloud:",
     menu_items={
         'Get Help': 'https://github.com/LincolnVS/blue-bird-words',
         'Report a bug': "https://github.com/LincolnVS/blue-bird-words/issues/new",
         'About': "Blue Birds Word by [Lincoln Schreiber](https://github.com/lincolnvs) and [Vitor Fraga](https://github.com/vitorfraga)"
     })

# -- Set API keys
api_key = st.secrets["api_key"]
api_key_secret = st.secrets["api_key_secret"]
access_token = st.secrets["access_token"]
access_token_secret = st.secrets["access_token_secret"]

# -- App

def get_stopwords(linguagem = 'pt'):
    if linguagem == 'en':
        return ['on', "mightn't", 'yours', 't', 'myself', 'did', 'as', 'more', 'haven', 'very', 'are', 'again', 'both', 'against', "wasn't", 'some', 'does', "didn't", 'above', 'for', 'having', 'by', 'during', 'same', 'further', 'under', 'when', 'wasn', 'they', 'be', 'm', "doesn't", 'each', 'd', 'of', "that'll", 'you', 'herself', 'ours', 'doesn', "isn't", 'all', "won't", 'himself', "couldn't", 'which', 'have', 'that', 'before', 'into', 'so', 'your', 'who', 'these', 'then', 'she', 'didn', 'do', 'we', 'my', 'to', 'after', 'most', 'should', 'me', "haven't", 'them', 'once', 'with', 'has', "don't", 'other', "mustn't", 'were', 'from', "shouldn't", 'aren', 'this', "weren't", 'doing', 'mightn', "you'd", "you'll", 'he', 'or', 'between', "you've", 'own', 'weren', 'am', 'if', 'ourselves', 'about', 'no', 'ma', 'but', "she's", 'our', 'any', 'was', 'been', 'their', 'will', 'needn', 've', 'is', 'll', 'wouldn', 'through', 'what', 'shan', "shan't", 'hadn', "it's", 'why', 'won', 'itself', 'in', 'those', 'off', 'her', "should've", 'mustn', 'here', 'at', 'until', 'ain', 'nor', 'yourselves', 's', 'don', 'its', 'i', 'a', 'it', 'out', 'such', 'just', 're', "hadn't", 'themselves', 'had', 'an', 'shouldn', "needn't", 'y', 'yourself', 'than', 'not', 'the', "hasn't", 'where', 'up', 'hers', "you're", 'because', 'down', 'can', 'and', "aren't", 'his', 'now', 'theirs', 'while', 'being', 'only', 'below', 'hasn', 'o', 'whom', "wouldn't", 'isn', 'how', 'few', 'there', 'couldn', 'too', 'him', 'over']
    elif linguagem == 'Não':
        return get_stopwords('pt') + get_stopwords('en')
    else: ## se n achar, devolve stopwords em portugues
        return ['houverei', 'seu', 'formos', 'há', 'pela', 'teu', 'seremos', 'estivesse', 'serei', 'numa', 'estejamos', 'tivemos', 'aquilo', 'houverá', 'teria', 'lhes', 'do', 'entre', 'aos', 'houverem', 'isso', 'for', 'muito', 'sou', 'seriam', 'fossem', 'tive', 'aquelas', 'os', 'foram', 'às', 'nossas', 'está', 'me', 'essas', 'seria', 'tinha', 'somos', 'tenha', 'sem', 'minha', 'estivéssemos', 'fôramos', 'tua', 'seja', 'meu', 'este', 'já', 'temos', 'houvermos', 'o', 'para', 'essa', 'isto', 'tém', 'com', 'como', 'será', 'que', 'estes', 'tem', 'pelos', 'houve', 'nossa', 'houver', 'vos', 'terei', 'fora', 'estiver', 'pelo', 'seríamos', 'tu', 'estávamos', 'um', 'dele', 'teve', 'pelas', 'tuas', 'aquele', 'pra', 'hei', 'hajam', 'ela', 'delas', 'forem', 'lhe', 'tivéramos', 'meus', 'fôssemos', 'qual', 'a', 'foi', 'dela', 'de', 'mas', 'também', 'fui', 'estivéramos', 'tenho', 'tivessem', 'terá', 'eles', 'teríamos', 'aqueles', 'estavam', 'no', 'estava', 'vocês', 'quem', 'tivesse', 'em', 'era', 'das', 'esta', 'estivera', 'houveremos', 'estão', 'esses', 'houvesse', 'você', 'estivermos', 'esteve', 'sua', 'teus', 'houvera', 'tiver', 'teriam', 'mesmo', 'estiverem', 'na', 'serão', 'Tweet', 'tenhamos', 'uma', 'Twitter', 'tiverem', 'ou', 'estiveram', 'estive', 'é', 'houvessem', 'teremos', 'tenham', 'deles', 'só', 'tiveram', 'sejam', 'esteja', 'as', 'eu', 'hão', 'seus', 'RT', 'não', 'nós', 'sejamos', 'nas', 'ele', 'minhas', 'mais', 'estivemos', 'havemos', 'tínhamos', 'houvéramos', 'suas', 'tinham', 'nos', 'depois', 'houveram', 'são', 'eram', 'houvemos', 'estas', 'houvéssemos', 'da', 'dos', 'num', 'estamos', 'nossos', 'nem', 'tivéssemos', 'hajamos', 'fomos', 'terão', 'por', 'ao', 'e', 'houveria', 'estou', 'houveríamos', 'se', 'até', 'fosse', 'houveriam', 'te', 'à', 'elas', 'nosso', 'éramos', 'houverão', 'tivermos', 'haja', 'aquela', 'tivera', 'esse', 'quando', 'estivessem', 'estejam', 'pra', 'para']

def slidebar():
    st.sidebar.write("## BLUE BIRD WORD")
    query = st.sidebar.text_input('Pesquisa', 'Brasil').lower()
    num_tweets = st.sidebar.slider('Selecione o numero de tweets', 10, 100, 50)
    #data = st.date_input("Desde quando deseja pegar", datetime.date(2019, 7, 6))
    linguagem = st.sidebar.selectbox(
    'Filtrar por idioma',
        ['Não','pt','en'])
    st.sidebar.markdown("Se escolher *Filtrar por idioma*, o programa irá utilizar apenas **10 tweets**.")
    if linguagem != 'Não':
        num_tweets = 10
    return query,num_tweets,linguagem
         
@st.cache(persist=True,suppress_st_warning=True)
def twitter_api(query,num_tweets,linguagem):
    #credenciais
    client = tweepy.Client(consumer_key= api_key,consumer_secret= api_key_secret,access_token= access_token,access_token_secret= access_token_secret, return_type = dict)

    max_trys = 3 #proteção para numero de requests
    trys = 0
    num_max = 100 #(Definimos uma variavel maxima para n estourar os limites que temos)
    num_tweets = num_max if num_max <= num_tweets else num_tweets 
    tweets = []

    while len(tweets) < num_tweets and trys < max_trys:
        search = client.search_recent_tweets(query=query,max_results=num_max, user_auth=True,tweet_fields ='lang')
        #print(search)

        for tweet in search['data']: #lang="pt", since="2017-04-03"
                #print(tweet)
                tweets.append(tweet['text']) if tweet['lang'] == linguagem or linguagem == 'Não' else None
        
        trys += 1
    
    string_total = ' '.join(tweets)
    string_total_n_patterns = re.sub(r'(#|@)(\w+|)|(https:|http:)[^\s]+', '', string_total) 

    # Set the entire file to lower case
    string_total_n_patternss = string_total_n_patterns.lower()

    # Replace the ' with nothing
    string_total_n_patternsss =  string_total_n_patternss.replace("`","")

    return string_total_n_patternsss

def texto_2_color_and_palette(text):
    if text == 'Gradiente - Estados Unidos':
        color = ['#ecf0f1', '#3498db', '#e74c3c']
        palette = None
    elif text == 'Amarelo':
        color = ['yellow']
        palette = None
    elif text == 'Azul':
        color = ['#1DA1F2']
        palette = None
    elif text == 'Vermelho':
        color = ['#c0392b']
        palette = None
    elif text == 'Branco':
        color = ['#ffffff']
        palette = None
    elif text == 'Gradiente - Escala de Cinza':
        color = ['#f0f0f0', '#a0a0a0', '#f0f0f0']
        palette = None
    elif text == 'Gradiente - Spectral':
        color = None
        palette = 'colorbrewer.diverging.Spectral_10'
    elif text == 'Gradiente - Bold':
        color = None
        palette = 'cartocolors.qualitative.Bold_5'
    elif text == 'Gradiente - Pastel':
        color = None
        palette = 'colorbrewer.sequential.YlOrBr_3'
    else:
        color = None
        palette = 'colorbrewer.diverging.Spectral_11'
    return color, palette

def texto_bg_2_color(text):
    if text == 'Preto':
        color = 'black'
    elif text == 'Branco':
        color = 'white'
    elif text == 'Vermelho':
        color = '#c0392b'
    elif text == 'Azul':
        color = '#1DA1F2'
    else:
        color = '#1DA1F2'
    return color

def texto_2_icon(text):
    if text == 'Padrão (Nuvem)':
        icone = 'fas fa-cloud'
    elif text == 'Twitter':
        icone = 'fab fa-twitter'
    elif text == 'Box':
        icone = 'fas fa-square'
    elif text == 'Cachorro':
        icone = 'fas fa-dog'
    elif text == 'Gato':
        icone = 'fas fa-cat'
    elif text == 'Aranha':
        icone = 'fas fa-spider'
    elif text == 'Fantasma':
        icone = 'fas fa-ghost'
    elif text == 'Circulo':
        icone = 'fas fa-circle'
    elif text == 'Biohazard':
        icone = 'fas fa-biohazard'
    elif text == 'Cerebro':
        icone = 'fas fa-brain'
    else:
        icone = 'fas fa-cloud'
    return icone

def cria_nuvem_de_palavras(texto,word_cloud_space,collocations,background_color,custom_max_words,custom_stopwords,custom_seed,font_color,invertido,icone_escolhido,gradiente):
    import matplotlib.pyplot as plt
    import stylecloud

    stopwords = get_stopwords(linguagem)

    # Create stopword list:
    stopwords = set(stopwords)
    stopwords.update(["tweet","twitter", "rt"])
    stopwords.update(custom_stopwords)

    color, palette = texto_2_color_and_palette(font_color)
    bg_color = texto_bg_2_color(background_color)
    icone = texto_2_icon(icone_escolhido)
    stylecloud.gen_stylecloud(
        text=texto,
        icon_name=icone,
        colors=color,
        palette=palette,
        background_color=bg_color,
        gradient=gradiente,
        custom_stopwords = stopwords,
        output_name='wordcloud.png',
        max_words=custom_max_words,
        collocations=collocations,
        invert_mask=invertido)

    word_cloud_space.image('wordcloud.png')

query,num_tweets,linguagem = slidebar()

st.write("## BLUE BIRD WORD (BBW)")

st.write('Nuvem de palavras com a pesquisa: ', query)
st.write("Total de ", num_tweets, ' tweets com essa pesquisa na linguagem ', linguagem)
texto = twitter_api(query,num_tweets,linguagem)

container = st.container()
word_cloud_space = container.empty()
#st.write('NUVEMM DE PALAVRAS VAI APARECER AQUIII')

st.markdown('---')
st.subheader('Parametros da nuvem de palavras:')

custom_max_words = st.slider('Selecione o numero de palavras na nuvem de palavra:', 1, 300, 150)

st.markdown(' ')
##Variaveis que o usuario vai poder editar wordcloud
custom_stopwords = st.text_input('Stopwords customizadas separadas por espaço ou virgula:', str(query)+',') #Palavras que quer tirar da nuvem de palavras

custom_stopwords = custom_stopwords.replace(' ',',').split(',')
custom_stopwords = [x for x in custom_stopwords if x != '']

st.write(custom_stopwords)

st.markdown(' ')
st.markdown(' ')

collocations = st.checkbox("Considerar palavras em conjunto.")#
st.write("> If true, same words can appear several times in the image, but if you disable that, you won't get words like 'black culture' or 'lets go'.")

st.markdown(' ')
st.markdown(' ')
icone_escolhido =  st.selectbox(
        'Icone:',
         ['Padrão (Nuvem)','Box','Circulo','Cerebro','Biohazard','Cachorro','Gato','Aranha','Fantasma','Twitter']) #cor de fundo so pode por enquanto 'black', 'white', 'red', 'blue'

invertido = st.checkbox("Inverter palavras pelo fundo")#

st.markdown(' ')
st.markdown(' ')

font_color =  st.selectbox(
        'Qual cor das palavras:', index=6,
        options = ['Azul','Vermelho','Amarelo','Branco','Gradiente - Cor Padrão','Gradiente - Escala de Cinza','Gradiente - Estados Unidos','Gradiente - Spectral','Gradiente - Bold','Gradiente - Pastel']) #cor de fundo

gradiente =  st.selectbox(
        'Se tem gradiente, vertical ou horizontal?',
         ['horizontal','vertical']) #cor de fundo


st.markdown(' ')
background_color =  st.selectbox(
        'Qual cor de fundo:',
         ['Preto','Azul','Branco','Vermelho']) #cor de fundo so pode por enquanto 'black', 'white', 'red', 'blue'


st.markdown(' ')
st.markdown(' ')
##Variaveis que o usuario vai poder editar wordcloud
custom_seed = st.number_input('Seed WordCloud',  min_value=1, max_value=10, value=1) #Palavras que quer tirar da nuvem de palavras


st.markdown(' ')

with container:
    with st.spinner('Wait for it...'):
        if len(texto) > 2:
            cria_nuvem_de_palavras(texto,word_cloud_space,collocations,background_color,custom_max_words,custom_stopwords,custom_seed,font_color,invertido,icone_escolhido,gradiente)
        else:
            word_cloud_space.markdown("**Não encontramos palavras para sua busca! :(**")
