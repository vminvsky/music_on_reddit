import pandas as pd 
import numpy as np 
from sklearn.metrics import pairwise
import matplotlib.pyplot as plt 
import seaborn as sns 

df = pd.read_csv("full-analysis\\datasets\\z-scores.csv")



metadata=pd.read_table('C:\\Users\\DELL XPS\\Desktop\\SummerResearch\\data\\datasets-important\\reddit-master-metadata.tsv')
vectors=pd.read_table("C:\\Users\\DELL XPS\\Desktop\\SummerResearch\\data\\datasets-important\\reddit-master-vectors.tsv",names=list(range(150)))
metadata=metadata['community']

data = pd.merge(metadata, vectors,left_index=True,right_index=True)


def create_scores(artists: list, limit = 2, high_limit = True):
    rick = df[df['artist'].isin(artists)]
    rick_v = pd.merge(rick,data, left_on='subreddit',right_on='community') 

    # rick_v2 = rick_v[(rick_v['z-score'] >= high_limit) | (rick_v['z-score'] <= lower_limit)]
    if high_limit==True:
        rick_v2 = rick_v[(rick_v['z-score'] >= limit)]
    elif high_limit == False:
        rick_v2=rick_v[(rick_v['z-score'] <= limit)]

    cols = [k for k in range(150)]

    for c in cols:
        rick_v2[c] = rick_v2[c]*abs(rick_v2['z-score'])

    meme_vector = rick_v2[cols].mean().values

    vals = pairwise.cosine_similarity(vectors,meme_vector.reshape(1,-1))

    df2 = pd.DataFrame(vals, index= metadata.values)

    df2= df2.sort_values(by=0, ascending = False)
    df2.columns = ['cosine-similarity']

    return df2, meme_vector 

df2, vector = create_scores(['Rick Astley'], limit = 1.7)


pd.Series(vector).to_csv("full-analysis\\datasets\\rick_astley-vector.csv", index=False)
df2.head(20)



df[df['artist']=='Bob Dylan'].sort_values(by='z-score')

df2.to_csv("rick-astley-score-subreddits.csv")



## projecting (instead of cosine similarity)

def create_scores_project(artists: list, high_limit = 2,low_limit = -0.5):
    rick = df[df['artist'].isin(artists)]
    rick_v = pd.merge(rick,data, left_on='subreddit',right_on='community') 

    # rick_v2 = rick_v[(rick_v['z-score'] >= high_limit) | (rick_v['z-score'] <= lower_limit)]
    pos_v = rick_v[(rick_v['z-score'] >= high_limit)]
    neg_v = rick_v[(rick_v['z-score'] <= low_limit)]
    cols = [k for k in range(150)]
    print(pos_v)
    print(neg_v)
    # for c in cols:
    #     pos_v[c] = pos_v[c]*abs(pos_v['z-score'])
    #     neg_v[c] = neg_v[c]*abs(neg_v['z-score'])
    # print(pos_v)

    pos_v = pos_v[cols].mean().values
    neg_v = neg_v[cols].mean().values
    vector = pos_v - neg_v
    vals = np.dot(vectors, vector) / np.linalg.norm(vector)

    df2 = pd.DataFrame(vals, index= metadata.values)

    df2= df2.sort_values(by=0, ascending = False)
    df2.columns = ['projection']

    return df2, vector

artist = 'Kanye West'
df2, vector = create_scores([artist], low_limit=-.3, high_limit=1.7)

df2.to_csv('data\\subreddit-on-{}-projection.csv'.format(artist))
vector= pd.DataFrame(vector)

vector.to_csv('{]-vector_v2.csv'.format(artist),index=False)