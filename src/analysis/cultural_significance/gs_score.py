import pandas as pd
import math 
from sklearn.metrics import pairwise 
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly
import plotly.figure_factory as ff
from scipy import stats

metadata=pd.read_table('C:\\Users\\DELL XPS\\Desktop\\SummerResearch\\data\\datasets-important\\reddit-master-metadata.tsv')
vectors=pd.read_table("C:\\Users\\DELL XPS\\Desktop\\SummerResearch\\data\\datasets-important\\reddit-master-vectors.tsv",names=list(range(150)))
metadata=metadata['comnmunity']
data=pd.merge(metadata,vectors,left_index=True,right_index=True)


df = pd.read_csv('full-analysis\\datasets\\Reddit_Sub_Com_v4_genre.csv')


grouped = df.groupby(['artist','subreddit'])['score'].count()
grouped = grouped.reset_index()
grouped.columns = ['artist','subreddit','count']
grouped = pd.merge(grouped, data, left_on = 'subreddit',right_on = 'community')

genres = pd.read_csv("full-analysis\\datasets\\genre_names_v4.csv")
artist_vector = pd.read_csv("full-analysis\\datasets\\Artist_Vectors_v4.csv")
artist_counts = pd.read_csv('full-analysis\\datasets\\Artist_Counts_v4.csv')


dimensions = [k for k in range(150)]
dimensions1 = [str(k) for k in range(150)]

artist_vector.index = artist_vector['artist']
artist_vector = artist_vector[dimensions1]
artists = artist_vector.index

artist_vector_n = (artist_vector.T  / [abs(k) for k in artist_vector.sum(axis = 1).values]).T
artist_vector_n.to_csv('full-analysis\\datasets\\Artist_Vector_n_v4.csv')

values = []
for i, a in enumerate(artists):
    print(str(i)+ ': ' + a)
    temp = grouped[grouped['artist']==a]
    subs = temp['subreddit'].unique()
    J = temp['count'].sum()
    artist_v = artist_vector_n.loc[artist_vector_n.index == a][dimensions1].values
    score = 0
    for sub in subs: 
        sub_df = temp[temp['subreddit']==sub]
        count = sub_df['count'].values[0]
        score += pairwise.cosine_similarity(sub_df[dimensions].values.reshape(1,-1), artist_v.reshape(1,-1)) * count
    score = score / J
    values.append({'artist': a,'GS_score':score[0][0]})


gs_score = pd.DataFrame(values).sort_values(by=  'GS_score')
gs_score.reset_index(inplace=True,drop=True)

artist_song = pd.read_csv('old_visuals_and_data\\artist-song.csv')
artist_song = artist_song[['artist','track_name','proporition']]
artist_song.columns = ['artist','track_name','proportion']

gs_score = pd.merge(artist_song, gs_score, on ='artist',how='right')
gs_score.sort_values(by='GS_score', inplace=True)
artist_counts = pd.read_csv("full-analysis\\datasets\\Artist_Counts_v4.csv")

gs_score = pd.merge(gs_score, artist_counts, on = 'artist',how='left')

gs_score.to_csv("full-analysis\\datasets\\gs_score.csv", index=  False)



gs_score = pd.read_csv("full-analysis\\datasets\\gs_score.csv")

gs_score['percentile'] = 0
dic = {'old_value': gs_score['count'].min()}
for i in np.arange(0.1, 1.1, .1):
    val = gs_score['count'].quantile(i)
    gs_score.loc[(gs_score['count'] <= val) & (gs_score['count'] >= dic['old_value']), 'percentile'] = int(i * 100)
    dic.update({'old_value': val})

lis = []
dic = {'old_value': gs_score['count'].min()}
for i in np.arange(0.1, 1.1, .1):
    val = gs_score['count'].quantile(i)
    lis.append({'percentile': int(i * 100), 'values': gs_score.loc[(gs_score['count'] <= val) & (gs_score['count'] >= dic['old_value']),'GS_score'].values})
    dic.update({'old_value': val})



values = [k['values'] for k in lis]
grouped_names = [k['percentile'] for k in lis]

fig = ff.create_distplot(values, grouped_names, show_hist=False, show_rug=False, )
fig.update_layout(
    xaxis_title = 'GS score',
    yaxis_title = 'Percentage of users',
    legend_title = 'Sharing percentile'
    )
fig.write_image('image.png', engine = 'kaleido', scale = 3)


gs_score_80 = gs_score[gs_score['percentile'] == 80]
gs_score_90 = gs_score[gs_score['percentile'] == 90]
gs_score_100 = gs_score[gs_score['percentile'] == 100]

gs_score_100['percentile2'] = gs_score_100['GS_score'].apply(lambda x: stats.percentileofscore(gs_score_100['GS_score'].values, x))
gs_score_90['percentile2'] = gs_score_90['GS_score'].apply(lambda x: stats.percentileofscore(gs_score_90['GS_score'].values, x))
gs_score_80['percentile2'] = gs_score_80['GS_score'].apply(lambda x: stats.percentileofscore(gs_score_80['GS_score'].values, x))

gs_score_f = gs_score_80.append(gs_score_90.append(gs_score_100))
gs_score_f = gs_score_f.sort_values(by='percentile2')
gs_score_f.to_csv("gs_score_percentile.csv")

gs_score_f[['artist','track_name','percentile2','count']].reset_index(drop=True).head(100)

# df = pd.read_csv("meme_artist_scores.csv")
# artist_counts = pd.read_csv("full-analysis\\datasets\\Artist_Counts_v4.csv")
# artist_counts = artist_counts[artist_counts['count'] > 600]
# artists = artist_counts['artist'].unique()
# df[df['artist'].isin(artists)]