import pandas as pd 
import numpy as np 
from sklearn.metrics import pairwise

metadata=pd.read_table('data\\reddit-master-metadata.tsv')
vectors=pd.read_table("data\\reddit-master-vectors.tsv",names=list(range(150)))
metadata=metadata['community']
data=pd.merge(metadata,vectors,left_index=True,right_index=True)



df=pd.read_csv(r"data\Reddit_Sub_Com_genre.csv")
gens = pd.read_csv(r"data\genre_names.csv")
df = pd.merge(df, gens[['label','genre']], on='label')
df=df[['artist','genre','subreddit','label']]

def cosine_similarity(category):
    merged=pd.merge(df,data,left_on='subreddit',right_on='community')
    dimens = list(range(150))

    grouped=merged.groupby(category)[dimens].mean()
    grouped.to_csv(r"data\{}_vectors.csv".format(category))

    cosine_similarity=pd.DataFrame(pairwise.cosine_similarity(grouped.values), columns = grouped.index, index=grouped.index)
    cosine_similarity.to_csv(r"data\{}_cosine_similiarity.csv".format(category))

    return cosine_similarity


