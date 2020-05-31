#%%
import pandas as pd
import numpy as np
from os import path
from PIL import Image
import matplotlib.pyplot as plt

from  wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import warnings
warnings.filterwarnings("ignore")

#df = pd.read_json('datasets/winemag-data-130k-v2.json')
df = pd.read_csv("datasets/winemag-data-130k-v2.csv")

#print("There are {} observation and {} features is this dataset. \n".format(df.shape[0], df.shape[1]))
#print("There are {} types of wine in this dataset such as {}...\n".format(len(df.variety.unique()), ", ".join(df.variety.unique()[0:5])))
#print("There are {} contries producing wine in this dataset such as {}... \n".format(len(df.country.unique()), ", ".join(df.country.unique()[0:5])))

text = " ".join(review for review in df.description)
print ("There are {} words in the combination of all review.".format(len(text)))

# Create stopword list:
stopwords = set(STOPWORDS)
stopwords.update(["drink", "now", "wine", "flavor", "flavors"])

# Generate a word cloud image
wordcloud = WordCloud(stopwords=stopwords, background_color="white").generate(text)

# Display the generated image:
# the matplotlib way:
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()






# %%
