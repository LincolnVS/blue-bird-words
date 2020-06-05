import streamlit as st
import datetime
import numpy as np

def get_stopwords(linguagem = 'pt'):
  if linguagem == 'en':
    return ['on', "mightn't", 'yours', 't', 'myself', 'did', 'as', 'more', 'haven', 'very', 'are', 'again', 'both', 'against', "wasn't", 'some', 'does', "didn't", 'above', 'for', 'having', 'by', 'during', 'same', 'further', 'under', 'when', 'wasn', 'they', 'be', 'm', "doesn't", 'each', 'd', 'of', "that'll", 'you', 'herself', 'ours', 'doesn', "isn't", 'all', "won't", 'himself', "couldn't", 'which', 'have', 'that', 'before', 'into', 'so', 'your', 'who', 'these', 'then', 'she', 'didn', 'do', 'we', 'my', 'to', 'after', 'most', 'should', 'me', "haven't", 'them', 'once', 'with', 'has', "don't", 'other', "mustn't", 'were', 'from', "shouldn't", 'aren', 'this', "weren't", 'doing', 'mightn', "you'd", "you'll", 'he', 'or', 'between', "you've", 'own', 'weren', 'am', 'if', 'ourselves', 'about', 'no', 'ma', 'but', "she's", 'our', 'any', 'was', 'been', 'their', 'will', 'needn', 've', 'is', 'll', 'wouldn', 'through', 'what', 'shan', "shan't", 'hadn', "it's", 'why', 'won', 'itself', 'in', 'those', 'off', 'her', "should've", 'mustn', 'here', 'at', 'until', 'ain', 'nor', 'yourselves', 's', 'don', 'its', 'i', 'a', 'it', 'out', 'such', 'just', 're', "hadn't", 'themselves', 'had', 'an', 'shouldn', "needn't", 'y', 'yourself', 'than', 'not', 'the', "hasn't", 'where', 'up', 'hers', "you're", 'because', 'down', 'can', 'and', "aren't", 'his', 'now', 'theirs', 'while', 'being', 'only', 'below', 'hasn', 'o', 'whom', "wouldn't", 'isn', 'how', 'few', 'there', 'couldn', 'too', 'him', 'over']
  elif linguagem == 'outra_linguagem':
    return ['stopwords_da_outra_linguagem']
  else: ## se n achar, devolve stopwords em portugues
    return ['houverei', 'seu', 'formos', 'há', 'pela', 'teu', 'seremos', 'estivesse', 'serei', 'numa', 'estejamos', 'tivemos', 'aquilo', 'houverá', 'teria', 'lhes', 'do', 'entre', 'aos', 'houverem', 'isso', 'for', 'muito', 'sou', 'seriam', 'fossem', 'tive', 'aquelas', 'os', 'foram', 'às', 'nossas', 'está', 'me', 'essas', 'seria', 'tinha', 'somos', 'tenha', 'sem', 'minha', 'estivéssemos', 'fôramos', 'tua', 'seja', 'meu', 'este', 'já', 'temos', 'houvermos', 'o', 'para', 'essa', 'isto', 'tém', 'com', 'como', 'será', 'que', 'estes', 'tem', 'pelos', 'houve', 'nossa', 'houver', 'vos', 'terei', 'fora', 'estiver', 'pelo', 'seríamos', 'tu', 'estávamos', 'um', 'dele', 'teve', 'pelas', 'tuas', 'aquele', 'pra', 'hei', 'hajam', 'ela', 'delas', 'forem', 'lhe', 'tivéramos', 'meus', 'fôssemos', 'qual', 'a', 'foi', 'dela', 'de', 'mas', 'também', 'fui', 'estivéramos', 'tenho', 'tivessem', 'terá', 'eles', 'teríamos', 'aqueles', 'estavam', 'no', 'estava', 'vocês', 'quem', 'tivesse', 'em', 'era', 'das', 'esta', 'estivera', 'houveremos', 'estão', 'esses', 'houvesse', 'você', 'estivermos', 'esteve', 'sua', 'teus', 'houvera', 'tiver', 'teriam', 'mesmo', 'estiverem', 'na', 'serão', 'Tweet', 'tenhamos', 'uma', 'Twitter', 'tiverem', 'ou', 'estiveram', 'estive', 'é', 'houvessem', 'teremos', 'tenham', 'deles', 'só', 'tiveram', 'sejam', 'esteja', 'as', 'eu', 'hão', 'seus', 'RT', 'não', 'nós', 'sejamos', 'nas', 'ele', 'minhas', 'mais', 'estivemos', 'havemos', 'tínhamos', 'houvéramos', 'suas', 'tinham', 'nos', 'depois', 'houveram', 'são', 'eram', 'houvemos', 'estas', 'houvéssemos', 'da', 'dos', 'num', 'estamos', 'nossos', 'nem', 'tivéssemos', 'hajamos', 'fomos', 'terão', 'por', 'ao', 'e', 'houveria', 'estou', 'houveríamos', 'se', 'até', 'fosse', 'houveriam', 'te', 'à', 'elas', 'nosso', 'éramos', 'houverão', 'tivermos', 'haja', 'aquela', 'tivera', 'esse', 'quando', 'estivessem', 'estejam', 'pra', 'para']

def slidebar():
    hashtag = st.sidebar.text_input('Hashtag', '#Brasil')
    num_tweets = st.sidebar.slider('Selecione o numero de tweets', 10, 200, 90)
    #data = st.date_input("Desde quando deseja pegar", datetime.date(2019, 7, 6))
    linguagem = st.sidebar.selectbox(
    'Qual linguagem',
     ['pt','en'])
    return hashtag,num_tweets,linguagem
     
@st.cache(persist=True)
def twitter_api(hashtag,num_tweets,linguagem):
    # acessar https://apps.twitter.com para criar uma nova aplicação
    # cada aplicação tem suas próprias chaves

    import tweepy
    import re
    
    # acessar a aba "Keys and Access Tokens"
    # passa o Consumer Key e o Consumer Secret
    auth = tweepy.OAuthHandler('yE2PLUrZKOLWjzeQffoO2XS0y', 'nyDKJUmxBfltfq771hOCMz7gqZD7x6g7CFhguw6uurAAF2WunA')

    # define o token de acesso
    # para criar basta clicar em "Create my access token"
    # passa o "Access Token" e o "Access Token Secret"
    auth.set_access_token('1266783018351558668-euemNhqzmom8Fvg6XxHUJrKxxR5NAy',
            'nQuBusDWGWTuhxSf6MKmONehgziBau2ZZgRLZ77AeaRcs')

    # cria um objeto api
    api = tweepy.API(auth)

    num_max = 200 #(Defiinimos uma variavel maxima para n estourar os limites que temos)
    num_tweets = num_max if num_max <= num_tweets else num_tweets #proteção para numero de requests
    tweets = []
    for tweet in tweepy.Cursor(api.search,q=hashtag,count=num_tweets, tweet_mode="extended",lang=linguagem).items(num_tweets): #lang="pt", since="2017-04-03"
        tweets.append(tweet.full_text)

    string_total = ' '.join(tweets)
    string_total_n_patterns = re.sub(r'(#|@)(\w+|)|(https:|http:)[^\s]+', '', string_total) 

    # Set the entire file to lower case
    string_total_n_patterns = string_total_n_patterns.lower()

    # Replace the ' with nothing
    string_total_n_patterns =  string_total_n_patterns.replace("`","")
    return string_total_n_patterns

def cria_nuvem_de_palavras(texto,word_cloud_space,collocations,background_color,custom_max_words,custom_stopwords):
  import matplotlib.pyplot as plt
  from wordcloud import WordCloud

  stopwords = get_stopwords(linguagem)

  print ("There are {} words in the combination of all review.".format(len(texto)))

  # Create stopword list:
  stopwords = set(stopwords)
  stopwords.update(["tweet","twitter", "rt"])
  stopwords.update(custom_stopwords)

  # Generate a word cloud image
  wordcloud = WordCloud(stopwords=stopwords, background_color=background_color,collocations = collocations,max_words=custom_max_words).generate(texto)

  # Display the generated image:
  # the matplotlib way:
  plt.imshow(wordcloud, interpolation='bilinear')
  plt.axis("off")
  word_cloud_space.pyplot()


hashtag,num_tweets,linguagem = slidebar()

st.write("""
# BLUE BIRD WORD 
""")

st.write('Criando nuvem de palavras com a hashtag: ', hashtag)
st.write("Pegando ", num_tweets, ' tweets dessa hashtag na linguagem ', linguagem)
texto = twitter_api(hashtag,num_tweets,linguagem)

word_cloud_space = st.empty()
#st.write('NUVEMM DE PALAVRAS VAI APARECER AQUIII')

st.markdown('---')
st.subheader('Parametros da nuvem de palavras:')

custom_max_words = st.slider('Selecione o numero de palavras na nuvem de palavra', 20, 300, 100)

st.markdown(' ')
##Variaveis que o usuario vai poder editar wordcloud
custom_stopwords = st.text_input('Stopwords customizadas separadas por virgula', str(hashtag[1:])+',') #Palavras que quer tirar da nuvem de palavras
custom_stopwords = custom_stopwords.replace(' ','').split(',')

st.write(custom_stopwords)
st.markdown(' ')
st.markdown(' ')

collocations = st.checkbox("Considerar palavras em conjunto")#
st.write("> If true, same words can appear several times in the image, but if you disable that, you won't get 'black culture' or 'lets go'.")

st.markdown(' ')
st.markdown(' ')
background_color =  st.selectbox(
    'Qual cor de fundo',
     ['white','black','red','blue']) #cor de fundo so pode por enquanto 'black', 'white', 'red', 'blue'


cria_nuvem_de_palavras(texto,word_cloud_space,collocations,background_color,custom_max_words,custom_stopwords)
