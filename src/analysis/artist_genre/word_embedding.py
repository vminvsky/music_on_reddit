import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
from sklearn.metrics import pairwise
import seaborn as sns

words = pd.read_table('data\\datasets-important\\wfc_vecs_1575657682.tsv', names=list(range(150)))
metadata= pd.read_table('data\\datasets-important\\wfc_meta_1575657682.tsv')

data=pd.merge(words,metadata, left_index=True,right_index=True)

data.index=data['word']

data.drop(['word','type'],axis=1,inplace=True)

genre_vectors= pd.read_csv("full-analysis\\datasets\\Genre_vectors_v4.csv")
genre_names = pd.read_csv("full-analysis\\datasets\\genre_names_v4.csv")

genre_vectors=pd.merge(genre_vectors, genre_names[['label','genre']])
genre_vectors.drop('label',axis=1,inplace=True)
genre_vectors.index = genre_vectors['genre']
genre_vectors.drop(['genre'],axis=1, inplace= True)


from sklearn.metrics import pairwise

df=pd.DataFrame(pairwise.cosine_similarity(data, genre_vectors))
df.columns=genre_vectors.index

df.index=data.index


ind = df.index 
genres=df.columns

genres=genres.dropna()

## create the wordcloud 

from wordcloud import WordCloud 
wc = WordCloud(width=500, height = 300)


for g in genres: 
    weights = df[g].values 
    vals = {}
    for a,b in zip(ind,weights):
        vals.update({a:b})
    wordcloudd = wc.generate_from_frequencies(vals)
    plt.figure(figsize=[6,4])
    plt.imshow(wordcloudd)
    plt.axis('off')
    plt.savefig('visuals\\word_cloud_{}'.format(g.replace('/','').replace('.', '').replace(' ','')))

plt.show()  
