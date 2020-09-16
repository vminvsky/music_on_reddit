import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Groups should be in format [{name:..., weights:...}] or [{name:...., score_col: (hist, bin_edges) }]
def many_densities(groups, dimen_list, data, bins=30, density_scaling_factor=5, figsize=(10,10), all_label="users"):

    n_groups = len(groups)
    n_dimens = len(dimen_list)

    fig, axs = plt.subplots(1, n_dimens, figsize=figsize)
    
    min_maxs = []

    for i, dimen in enumerate(dimen_list):
        ax = axs[i]
        name = dimen
        ax.set_title(name)
        ax.set_frame_on(False)
        ax.tick_params(axis='x', labelrotation=90)
     
        if i == 0:
            ax.set_yticks(range(-1, n_groups + 1))
            group_labels = ["%s\nn=%d" % (group if type(group) is not dict else group["name"], sum(group['weights']) )for i, group in enumerate(groups)]
            ax.set_yticklabels([None] + group_labels +
                            ["$\\bf{All\\ %s}$\nn=%d" % (all_label, len(data))])
        else:
            ax.set_yticks([])
            
        ax.set_ylim(-1, n_groups + 2)
        min_max = (np.min(data[dimen]), np.max(data[dimen]))
        # min_max = (-2.5, 2.5)
        min_maxs.append(min_max)
        ax.set_xlim(min_max[0], min_max[1])
        
        median = np.median(data[name])
        ax.axvline(median, color='black', linestyle='--', linewidth=1)
            
    weights = np.empty(len(data))
    for i, group in enumerate(groups + [None]):
        
        if group is None:
            weights = np.ones(len(data))
        else:
            weights = group.get("weights", None)      
        
        for j, dimen in enumerate(dimen_list):
            name = dimen
            
            if group is not None and name in group:
                hist, bin_edges = group[name]
            else:
                hist, bin_edges = np.histogram(data[name], bins=bins, range=min_maxs[j], weights=weights, density=False)
                hist = hist / np.sum(hist)
                bin_edges = bin_edges[:-1]
            
            scaling_factor = (min_maxs[j][1] - min_maxs[j][0]) * density_scaling_factor
            
            score = 0.4
            x = bin_edges
            y = (scaling_factor * hist) + i
            axs[j].plot(x, y, color='black')
            axs[j].fill_between(x, y, i, alpha=score)

############### THIS IS DENSITY PLOTS FOR PPMI AND SPOTIFY GENRES
dimen_list=['affluence', 'age','edginess', 'gender', 'partisan', 'partisan_neutral', 'sociality']


df=pd.read_csv('C:\\Users\\DELL XPS\\Desktop\\SummerResearch\\full-analysis\\datasets\\Reddit_Sub_Com_v4_genre.csv')



custom_g=pd.read_csv('C:\\Users\\DELL XPS\\Desktop\\SummerResearch\\full-analysis\\datasets\\genre_names_v4.csv')

df = pd.merge(df,custom_g,on='label')

scores=pd.read_csv("C:\\Users\\DELL XPS\\Desktop\\SummerResearch\\data\\datasets-important\\venia_scores.csv")
df=pd.merge(df,scores, left_on='subreddit',right_on='community')


genres= df.groupby('genre')['genre'].count().sort_values(ascending=False).head(18).tail(10).index

df2=df[df['genre'].isin(genres)]




df2['ppmi'] = 1
lis=[]
# lis2=lis[len(lis)-48:]
# lis3=lis
# lis=lis2
for g in genres:
    print(g)
    lis.append({'name':g, 'weights':df2.apply(lambda x: x['ppmi'] if x['genre']==g else 0, axis=1).values})

vals=df[df['genre'] == 'rap']['affluence'].values



# define a subset of the genres we want to include

genres_ = ['death metal','pop punk','prog metal','rick astley & pop','alternative metal','indietronica','indie pop','electronica','pop edm','DnB','chill rap','modern rap']
lis_ = [k for k in lis if k['name'] in genres_]
df_ = df2[df2['genre'].isin(genres_)]

lis=[]
# lis2=lis[len(lis)-48:]
# lis3=lis
# lis=lis2
for g in genres:
    print(g)
    lis.append({'name':g, 'weights':df2.apply(lambda x: x['ppmi'] if x['genre']==g else 0, axis=1).values})

lis_.reverse()

many_densities(lis, dimen_list, df2, density_scaling_factor=2.5, bins=30, figsize=(15,19))
plt.show()
plt.savefig('full-analysis\\many-density-genres_top_15')





















import pickle


with open('many_densitiy_custom_genres_v2_weights.data', 'wb') as filehandle:
    # store the data as binary data stream
    pickle.dump(lis, filehandle)

'''
df4 = pd.read_csv("Reddit_Sub_Com_genres_SubredditScoring.csv")
for k in dimen_list:
    df4[k] = df4[k]*df4['ppmi']



dimen_list2=[k+'_' for k in dimen_list]


means=df4[dimen_list].mean()
stds=df4[dimen_list].std()

for k in dimen_list:
    df4[k+'_']=(df4[k]-means[k])/stds[k]




genres=df4.groupby('value')['subreddit'].count().sort_values(ascending=False).head(50).index
genres2=np.random.choice(genres,10, replace=False)

genres2=['rock','dance rock','new wave','metal','hip hop','rap', 'art rock','early us punk','comic', 'edm','classical']
df4['value'].unique()
genres2

df=df4[df4['value'].isin(genres2)]

lis = []

for g in genres2:
    print(g)
    lis.append({'name':g, 'weights':df.apply(lambda x: 1 if x['value']==g else 0, axis=1).values})



many_densities(lis, dimen_list2, df, bins = 40,density_scaling_factor= 0.5)
plt.savefig('zscore_densityplot')
##############



##############
df=pd.read_csv("comments_2mil.csv")
df2=pd.read_csv("Subreddit_Scores.csv")

data=df['subreddit']
data2=pd.merge(data,df2,left_on='subreddit',right_on='community')
data2=data2[['subreddit']+dimen_list]


data2['cat']='comment'
df4['cat']='music'

df=df4.append(data2)

df['w1']=df['cat'].apply(lambda x: 1 if x == 'music' else 0)
df['w2']=df['cat'].apply(lambda x: 1 if x == 'comment' else 0)

g=['music','comment']
w=['w1','w2']

groups=[]
for a,b in zip(g,w):
    groups.append({'name':a,'weights':df[b].values})


many_densities(groups, dimen_list, df, density_scaling_factor=2.5, figsize=[10,7])
plt.savefig('music_vs_comments')
plt.show()



####################################### this many densitites for no big subreddits 


df=pd.read_csv('Reddit_Sub_Com_customGenres_noBigSubreddits.csv')
dimen_list=['affluence', 'age','edgy', 'gender', 'partisan', 'politicalness', 'social']

custom_g=pd.read_excel('custom_genres_50_smallsubreddits.xlsx')

df=pd.merge(df,custom_g,left_on='label',right_on='genre_number')
scores=pd.read_csv("Subreddit_Scores.csv")
df=pd.merge(df,scores, left_on='subreddit',right_on='community')


genres= df.groupby('genre')['genre'].count().sort_values(ascending=False).head(10).index

df2=df[df['genre'].isin(genres)]



lis = []


for g in genres:
    print(g)
    lis.append({'name':g, 'weights':df2.apply(lambda x: x['ppmi'] if x['genre']==g else 0, axis=1).values})

df2.groupby('genre')['genre'].count()
df2[df2['genre']=='edm2']

df2.groupby(['genre','subreddit'])['genre'].count().sort_values()


many_densities(lis, dimen_list, df2, density_scaling_factor=4, bins=60)
plt.show()
plt.savefig('many_densities_customgenres_50_smallsubreddits')


'''