import pandas as pd 
import numpy as np
import scipy 
import math 


df = pd.read_csv(r"C:\Users\DELL XPS\Desktop\SummerResearch\full-analysis\datasets\Reddit_Sub_Com_v4_genre.csv")


grouped = df.groupby(['artist','subreddit'])['label'].count()
grouped=grouped.reset_index()
grouped.columns=  ['artist','subreddit','count']

arts = df.groupby('artist')['label'].count()
arts = arts.reset_index()
arts.columns =['artist','count']
artists= arts['artist'].unique()

grouped['probability']=0
for a in artists: 
    print(a)
    val = arts.loc[arts['artist']==a,'count'].values[0]
    grouped.loc[grouped['artist']==a,'probability'] = grouped.loc[grouped['artist']==a]['count'].apply(lambda x: x/val)

grouped.to_csv('temp-entropy_v4.csv')

grouped['probability']=pd.to_numeric(grouped['probability'])
grouped.drop(grouped[grouped['probability']==0].index,inplace=True)
grouped['log'] = grouped['probability'].apply(lambda x: math.log(x, 2))

artists=grouped['artist'].unique()


entropy = []

for a in artists:
    print(a)
    temp = grouped[grouped['artist']==a]
    score = -sum((temp['probability'] * temp['log']))
    entropy.append({'name': a, 'entropy': score})

entr = pd.DataFrame(entropy).sort_values(by='entropy', ascending=False)
entr2= entr.dropna()

entr2.to_csv("full-analysis\\entropy_scores_v4.csv")


norm_entr =  entr.sort_values(by= 'entropy', ascending=False).head(20)

entr.to_csv("artist-normalized-entropy-scores.csv")



artist_counts=pd.read_csv(r"C:\Users\DELL XPS\Desktop\SummerResearch\data\datasets-important\Artist_Counts.csv")
top_artists = artist_counts.sort_values(by='genre',ascending=False).head(400)['artist'].values


top_entropy = entr[entr['name'].isin(top_artists)].sort_values(by='entropy')

top_entropy.to_csv("ccsv")





# entropy without looking at the music subreddits




artist_counts=pd.read_csv(r"C:\Users\DELL XPS\Desktop\SummerResearch\full-analysis\datasets\artist_counts_v4.csv")
df = pd.read_csv("full-analysis\\entropy_scores_v4.csv")
artist_song = pd.read_csv("artist-song.csv")
artist_song=artist_song[['artist','track_name','proporition']]
df = df[['name','entropy']]
df.columns = ['artist','entropy']
df=pd.merge(df,artist_song, on ='artist', how='left')

df= pd.merge(df,artist_counts, on ='artist')

df.columns = ['artist','entropy','track_name','proportion','artist_count']

# this plots the entropy using plotly

import plotly.express as px
df = df.drop(df[df['artist_count']==0].index)
df['log_artist_count'] = df['artist_count'].apply(lambda x: math.log(x, 10))
fig = px.scatter(df, x="log_artist_count", y="entropy", hover_data=['artist'])
fig.show()


df.to_csv("full-analysis\\artist_entropy_full.csv")


## plot entropy by count
import matplotlib.pyplot as plt 
import math 


fig, ax = plt.subplots(1, figsize= [7,5])
ax.scatter(df['artist_count'],df['entropy'])
plt.xlabel('artist count')
plt.ylabel('entropy score')
plt.suptitle('Log Count vs Entropy Score')
plt.savefig('count_entropy_score')
plt.show()

df.sort_values(by='log_artist_count')
df[df['artist'] == 'JOJI']


##### attempt at custom entropy score 
from sklearn.metrics import pairwise

artist_vectors = pd.read_csv('full-analysis\\datasets\\Artist_Vectors_v4.csv')
artist_vectors.index = artist_vectors['artist']
artist_vectors= artist_vectors[[str(k) for k in range(150)]]
artist_counts = pd.read_csv('full-analysis\\datasets\\Artist_Counts_v4.csv')

metadata=pd.read_table('C:\\Users\\DELL XPS\\Desktop\\SummerResearch\\data\\datasets-important\\reddit-master-metadata.tsv')
vectors=pd.read_table("C:\\Users\\DELL XPS\\Desktop\\SummerResearch\\data\\datasets-important\\reddit-master-vectors.tsv",names=list(range(150)))
metadata=metadata['community']
data=pd.merge(metadata,vectors,left_index=True,right_index=True)
data.index=data['community']
data.drop('community',axis=1,inplace=True)

cosine = pd.DataFrame(pairwise.cosine_similarity(artist_vectors,data.values),index = artist_vectors.index, columns = data.index)
cosine.reset_index(inplace=True)
cosine_melt = cosine.melt(id_vars='artist')
cosine_melt.columns = ['artist','subreddit','value']
cosine_melt['key'] = cosine_melt['artist'] + cosine_melt['subreddit']

artists = artist_counts['artist'].head(500).values
df2 = df[df['artist'].isin(artists)]
df['key'] = df['artist'] + df['subreddit']
artist = 'Dwayne Johnson'

# add another column that represents the weight. 

cosine_melt_temp = cosine_melt[cosine_melt['artist']==artist]

df = pd.merge(df, cosine_melt[['key','value']], on ='key')

df['weight'] = df['value'].apply(lambda x: 1 if x > 0.6 else 1.5 if x > 0.4 else 2)


grouped = df.groupby(['artist','subreddit']).agg({'label': 'count','weight':'mean'})
grouped=grouped.reset_index()
grouped.columns=  ['artist','subreddit','count', 'weight']



arts = df.groupby('artist')['label'].count()
arts = arts.reset_index()
arts.columns =['artist','count']
artists= arts['artist'].unique()

grouped['probability']=0
for a in artists: 
    print(a)
    val = arts.loc[arts['artist']==a,'count'].values[0]
    grouped.loc[grouped['artist']==a,'probability'] = grouped.loc[grouped['artist']==a]['count'].apply(lambda x: x/val)


grouped['probability_w'] = grouped['probability'] * grouped['weight']
grouped['log'] = grouped['probability'].apply(lambda x: math.log(x, 2))
entropy2 = []


for a in artists:
    print(a)
    temp = grouped[grouped['artist']==a]
    score = -sum((temp['probability_w'] * temp['log']))
    entropy2.append({'name': a, 'entropy': score})


entropy = pd.DataFrame(entropy2).sort_values(by='entropy',ascending=False)
df.head(30)