import pandas as pd
import matplotlib.pyplot as plt  
import seaborn as sns 
from sklearn.metrics import pairwise
# plt.style.use(['science', 'no-latex'])
plt.rcParams['font.family'] = 'arial'


df = pd.read_csv("data\\Reddit_Sub_Com_f.csv")

df['datetime']= pd.to_datetime(df['created_utc'],unit='s')
df['month_year'] = df['datetime'].dt.to_period('M')
df['quarter'] = df['datetime'].dt.to_period('Q')
df['week_year'] = df['datetime'].dt.to_period('W')
df['date'] = df['datetime'].dt.date
df['year'] = df['datetime'].dt.year

# we'll analyze years 2012 or after. 
df = df[df['year'].isin([2014,2015,2016,2017,2018,2019])]


metadata=pd.read_table('data\\reddit-master-metadata.tsv')
vectors=pd.read_table("data\\reddit-master-vectors.tsv",names=list(range(150)))
metadata=pd.DataFrame(metadata['community'])
data=pd.merge(metadata,vectors,left_index=True,right_index=True)

cultural_vectors = pd.read_csv("data\\cultural_scores.csv")
cultural_dimens = ['age','affluence','gender','partisan','partisan_neutral']
dimens = list(range(150))

## there are two levels to this analysis: similarity and cultural level 
# similarity between artists (context) and how an artist changes to him/herself. 

def artist_context(artist, metric, top_x = 5):
    vals = df[metric].unique()
    artist_scores = []
    for q in vals:
        temp = df[df[metric] == q]
        temp.groupby('artist')['score'].count().sort_values(ascending=False)
        merged=pd.merge(temp,data,left_on='subreddit',right_on='community')
        dimens = list(range(150))
        genre_grouped=merged.groupby('artist')[dimens].mean()
        cosine_similarity=pd.DataFrame(pairwise.cosine_similarity(genre_grouped.values), columns = genre_grouped.index, index=genre_grouped.index)
        scores = cosine_similarity[artist].sort_values(ascending=False).head(top_x + 1).tail(top_x)
        scores = scores.reset_index()
        period_dict = {}
        l = 0
        for i, k in scores.values:
            artist_scores.append({'artist': artist, 'datetime': q, 'artist_rank': l, 'closest_artist': i,'similarity': k})
            l+=1
    response = artist_scores
    response = pd.DataFrame(response)

    t = response.groupby('datetime')['closest_artist'].apply(list)
    t=t.apply(lambda x: pd.Series(x)).T

    import plotly.graph_objects as go

    fig = go.Figure(data=[go.Table(
        header=dict(values=list(t.columns),
                    align='center'),
        cells=dict(values=[t[2014], t[2015], t[2016], t[2017], t[2018], t[2019]],
                align='left'))
    ])
    fig.update_layout(
        title={
            'text': artist,
            'y':0.85,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    fig.write_image('visuals\\{}_context2.png'.format(artist), engine="kaleido")
    return t
response = artist_context("Bruce Springsteen", 'year')

## now do how an artist similarity to him/herself changes. 
artist_list = df.groupby('artist')['score'].count().sort_values(ascending=False).head(100).sample(5).index
def similarity_evolution(artist_list, start_year):  
    fig, ax = plt.subplots(1,1)
    for artist in artist_list:
        temp = df[(df['artist'] == artist) & (df['year'] >= start_year)]

        merged=pd.merge(temp,data,left_on='subreddit',right_on='community')
        grouped = merged.groupby('year')[dimens].mean().sort_index()
        grouped = (grouped.T / abs(grouped.sum(axis = 1)).values).T
        initial_values = grouped.loc[grouped.index == start_year][dimens]

        score = pairwise.cosine_similarity(initial_values, grouped.values)
        ax.plot(grouped.index, score[0], label = artist)
        ax.set_xticks(grouped.index)

similarity_evolution(artist_list, 2015)
plt.legend()
plt.xlabel("Year")
plt.ylabel("Similarity to base year")
plt.savefig("visuals\\Artist_Evolution4")
plt.show()



### evolution of the cultural 
df_temp = pd.merge(df,cultural_vectors, left_on='subreddit',right_on='community')
vals = df_temp.groupby("year")[cultural_dimens].mean()
cultural_dimens= ['age','affluence','gender','partisan','partisan-ness']
vals.columns = cultural_dimens
### if we want to normalize the results between [0,1] using max min scaler. 

# for k in cultural_dimens:
#     max_v = vals[k].max()
#     min_v = vals[k].min()
#     dif = max_v - min_v 
#     vals[k] = vals[k].apply(lambda x: (x- min_v) / dif)

# vals = vals.T 
# vals.index = vals['index']
# vals.drop('index', axis = 1,inplace=True)
# vals = vals.T


fig, axs = plt.subplots(len(cultural_dimens), 1, figsize =[4,3.5], sharex=True)
max_i = len(cultural_dimens) - 1
for i, feat in enumerate(cultural_dimens):
    axs[i].plot(vals.index, vals[feat], label = feat)
    axs[i].title.set_text(feat.replace('_',' '))
    # axs[i].plot(1,1,label = feat,marker = '',ls ='')
    # axs[i].legend(loc= 'upper right')
    # if i < max_i:
    #     axs[i].axes.set_xticks([])
# plt.legend()
plt.tight_layout()
plt.savefig('culture_timeseries2.pdf', dpi = 300)

plt.show()
