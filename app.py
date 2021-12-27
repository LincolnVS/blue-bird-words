from typing_extensions import final
import streamlit as st
import os
import re
import utils as u

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

def slidebar():
    st.sidebar.write("## BLUE BIRD WORD")
    query = st.sidebar.text_input('Search', 'Brasil').lower()
    max_tweets = st.sidebar.slider('Select the number of tweets', 10, 100, 50)
    #data = st.date_input("Desde quando deseja pegar", datetime.date(2019, 7, 6))
    lang = st.sidebar.selectbox(
    'Filter by language',
        ['no','pt','en'])
    st.sidebar.markdown("If you choose *Filter by language*, the program will use only **10 tweets**.")
    
    if lang != 'no':
        max_tweets = 10

    return query,max_tweets,lang
         
@st.cache(persist=True)
def request_twitter(query,max_tweets,lang):
    import tweepy
    #credenciais
    client = tweepy.Client(consumer_key= api_key,consumer_secret= api_key_secret,access_token= access_token,access_token_secret= access_token_secret, return_type = dict)

    max_trys = 3 #proteção para numero de requests
    trys = 0

    tweets = []

    while len(tweets) < max_tweets and trys < max_trys:
        n_requests = max(max_tweets - len(tweets),10)
        search = client.search_recent_tweets(query=query, max_results=n_requests, user_auth=True, tweet_fields='lang')

        for tweet in search['data']:
            tweets += [tweet['text']] if lang == 'no' or tweet['lang'] == lang else []
        
        trys += 1
    
    final_string = ' '.join(tweets)
    final_string_n_patterns = re.sub(r'(#|@)(\w+|)|(https:|http:)[^\s]+', '', final_string) 

    # Set the entire file to lower case, Replace the ' with nothing, Replace the \n with space
    final_string_n_patterns = final_string_n_patterns.lower().replace("`","").replace("\n"," ")

    print(final_string_n_patterns)
    return final_string_n_patterns

def create_wordcloud(tweets,word_cloud_space,collocations,background_color,custom_max_words,custom_stopwords,custom_seed,font_color,invertido,icone_escolhido,gradiente):
    import matplotlib.pyplot as plt
    import stylecloud

    # Create stopword list:
    stopwords = u.get_stopwords(lang)
    stopwords = set(stopwords)
    stopwords.update(custom_stopwords)

    color, palette = u.text_2_color_and_palette(font_color)
    bg_color = u.text_bg_2_color(background_color)
    icone = u.text_2_icon(icone_escolhido)

    stylecloud.gen_stylecloud(
        text=tweets,
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

query,max_tweets,lang = slidebar()

st.write("## BLUE BIRD WORD (BBW)")

if lang == 'no':
    text = f"Wordcloud using {max_tweets} tweets with '{query}' without filtering by language."
else:
    text = f"Wordcloud using {max_tweets} tweets with '{query}' and with '{lang}' language filter"
st.write(text)

tweets = request_twitter(query,max_tweets,lang)

container = st.container()
word_cloud_space = container.empty()
#st.write('NUVEMM DE PALAVRAS VAI APARECER AQUIII')

st.markdown('---')
st.subheader('Word cloud parameters:')

custom_max_words = st.slider('Select the number of words in the word cloud:', 1, 300, 150)

st.markdown(' ')
##Variaveis que o usuario vai poder editar wordcloud
custom_stopwords = st.text_input('Customized stopwords (*separated by space or comma*):', str(query)+',') #Palavras que quer tirar da nuvem de palavras

custom_stopwords = custom_stopwords.replace(' ',',').split(',')
custom_stopwords = [x for x in custom_stopwords if x != '']

st.write(custom_stopwords)

st.markdown(' ')
st.markdown(' ')
icone_escolhido =  u.selectbox(
        'Icon:',
        options = u.icon_list() ) #cor de fundo so pode por enquanto 'black', 'white', 'red', 'blue'

invertido = u.checkbox(label="Invert background and icon")#

font_color =  u.selectbox(
        'Word color:',
        options = u.font_colors_list() ) #cor de fundo

background_color =  u.selectbox(
        'Background color:',
        options = u.bg_color_list() ) #cor de fundo so pode por enquanto 'black', 'white', 'red', 'blue'

with st.expander("Advanced options"):
    
    gradient = ''
    if 'Grad' in font_color or font_color == 'Default':
        gradient =  u.selectbox(
                'The gradient color is ...?',
                options = ['horizontal','vertical']) #cor de fundo
        st.markdown('---')


    collocations = st.checkbox("Consider words together.")#
    st.write("> If true, same words can appear several times in the image, but if you disable that, you won't get words like 'black culture' or 'lets go'.")

    st.markdown('---')
    
    ##Variaveis que o usuario vai poder editar wordcloud
    custom_seed = u.number_input('Seed WordCloud', value=1) #Palavras que quer tirar da nuvem de palavras


st.markdown(' ')

with container:
    with st.spinner('Wait for it...'):
        if len(tweets) > 2:
            create_wordcloud(tweets,word_cloud_space,collocations,background_color,custom_max_words,custom_stopwords,custom_seed,font_color,invertido,icone_escolhido,gradient)
        else:
            word_cloud_space.markdown("**We can't find words for your search! :(**")
