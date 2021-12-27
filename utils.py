import streamlit as st

# -- Stopwords 
def load_stopwords(path):
    with open(path, 'r') as file:
        stopwords = file.read().split('\n')
    return stopwords

stopwords = {
    'pt': load_stopwords('stopwords/pt.txt'),
    'en': load_stopwords('stopwords/en.txt'),
    'es': load_stopwords('stopwords/es.txt'),
    'default': load_stopwords('stopwords/default.txt')
}

def get_stopwords(lang = 'no'):
    words = stopwords['default']

    if lang == 'en' or lang == 'no':
        words += stopwords['en']
    
    if lang == 'pt' or lang == 'no':
        words += stopwords['pt']

    if lang == 'es' or lang == 'no':
        words += stopwords['es']

    return words

# -- Plot 
font_colors = {
    'Default': [['#ecf0f1', '#3498db', '#e74c3c'],None],
    'Black': ['black',None],
    'Yellow': ['yellow',None],
    'Red': ['#c0392b',None],
    'Blue': ['#1DA1F2',None],
    'White': ['#ffffff',None],
    'Gradient - Grayscale': [['#00f0f0', '#a0a0a0', '#f0f0f0'],None],
    'Gradient - Spectral':[None, 'colorbrewer.diverging.Spectral_10'],
    'Gradient - Bold':[None, 'colorbrewer.diverging.Bold_5'],
    'Gradient - Pastel':[None, 'colorbrewer.diverging.YlOrBr_3']
}
def text_2_color_and_palette(text):  
    return font_colors.get(text, font_colors['Default'])

def font_colors_list():
    return list(font_colors.keys())
def bg_color_list():
    return list(bg_color.keys())
def icon_list():
    return list(icons.keys())

bg_color = {
    'Default': 'black',
    'Black': 'black',
    'Yellow': 'yellow',
    'Red': '#c0392b',
    'Blue': '#1DA1F2',
    'White': 'white',
}
def text_bg_2_color(text):
    return bg_color.get(text, bg_color['Default'])

icons = {
    'Default': 'fas fa-cloud',
    'Twitter': 'fab fa-twitter',
    'Box': 'fas fa-square',
    'Dog': 'fas fa-dog',
    'Cat': 'fas fa-cat',
    'Spider': 'fas fa-spider',
    'Ghost': 'fas fa-ghost',
    'Circle': 'fas fa-circle',
    'Biohazard': 'fas fa-biohazard',
    'Brain': 'fas fa-brain'
}
def text_2_icon(text):
    return icons.get(text, icons['Default'])

# -- STREAMLIT WIDGETS

def text_field(label, columns=None, **input_params):
    c1, c2 = st.columns(columns or [1, 4])

    # Display field name with some alignment
    c1.markdown("##")
    c1.markdown(label)

    # Sets a default key parameter to avoid duplicate key errors
    input_params.setdefault("key", label)

    # Forward text input parameters
    return c2.text_input("", **input_params)

def selectbox(label, columns=None, **input_params):
    c1, c2 = st.columns(columns or [1, 4])

    # Display field name with some alignment
    c1.markdown("##")
    c1.markdown(label)

    # Sets a default key parameter to avoid duplicate key errors
    input_params.setdefault("key", label)

    # Forward text input parameters
    return c2.selectbox("", **input_params)

def checkbox(label, columns=None, **input_params):
    c1, c2 = st.columns(columns or [1, 4])

    # Display field name with some alignment
    c1.markdown("##")
    c1.markdown('')

    # Sets a default key parameter to avoid duplicate key errors
    input_params.setdefault("key", label)

    # Forward text input parameters
    return c2.checkbox(label, **input_params)

def number_input(label, columns=None, **input_params):
    c1, c2 = st.columns(columns or [1, 4])

    # Display field name with some alignment
    c1.markdown("##")
    c1.markdown(label)

    # Sets a default key parameter to avoid duplicate key errors
    input_params.setdefault("key", label)

    # Forward text input parameters
    return c2.number_input("", **input_params)