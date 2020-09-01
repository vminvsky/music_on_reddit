import pandas as pd 
from sklearn.cluster import AgglomerativeClustering
from sklearn.decomposition import PCA
from scipy.cluster.hierarchy import dendrogram, linkage


metadata=pd.read_table('data\\reddit-master-metadata.tsv')
vectors=pd.read_table("data\\reddit-master-vectors.tsv",names=list(range(150)))
metadata=metadata['community']


data=pd.merge(metadata,vectors,left_index=True,right_index=True)

df = pd.read_csv("data\\Reddit_Sub_Com.csv")

artist_counts = df.groupby('artist')['artist'].count()
artist_counts = artist_counts.reset_index()
artist_counts.columns = ['artist','count']
artist_counts.to_csv("data\\artist_counts.csv")

def create_genres(df, n_clusters=50,with_ppmi=False):
    """df should be subreddit artist and ppmi. Columns should be ['subreddit','artist','ppmi'] """

    global data 
    if with_ppmi==False:
        df=df[['subreddit','artist']]

        merged=pd.merge(df,data,left_on='subreddit',right_on='community')


        count=merged.groupby('artist')['artist'].count()
        artist=merged.groupby('artist')[list(range(150))].mean()

        #only take artists with 20 or more shares 
        a_index=count[count>20].index
        artist=artist.loc[artist.index.isin(a_index)]

        # use hierarchical clustering
        ac=AgglomerativeClustering(n_clusters)

        ac.fit(artist)
        artist['label']=ac.labels_
        return artist, ac 
    elif with_ppmi==True:
        df=df[['subreddit','artist', 'ppmi']]
        merged=pd.merge(df,data,left_on='subreddit',right_on='community')
        for j in range(150):
            merged[j]=merged['ppmi']*merged[j]
        count=merged.groupby('artist')['artist'].count()
        artist=merged.groupby('artist')[list(range(150))].mean()

        #only take artists with 20 or more shares 
        a_index=count[count>20].index
        artist=artist.loc[artist.index.isin(a_index)]

        # use hierarchical clustering
        ac=AgglomerativeClustering(n_clusters)

        ac.fit(artist)
        artist['label']=ac.labels_
        return artist, ac


custom, ac = create_genres(df, 50, with_ppmi=False)
custom=custom.reset_index()


custom[['artist','label']].to_csv("datasets\\Artist_Genre.csv")

custom.groupby('label')[list(range(150))].mean().to_csv("Genre_Vectors.csv")


# save the model
from joblib import dump, load
dump(ac, 'datasets\\agglogomerative.joblib') 


# save the new finalized dataset
data4=pd.merge(df,custom[['artist','label']], on = 'artist')
data4 = data4[['score','link_id','author','subreddit','created_utc','id','parent_id','track_id','artist','track_name','link','youtube_id','class','url','album_id','label']]
data4.to_csv("datasets\\Reddit_Sub_Com_genre.csv")



