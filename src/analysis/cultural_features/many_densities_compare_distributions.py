import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm
plt.rcParams['font.family'] = 'arial'


# Groups should be in format [{name:..., weights:...}] or [{name:...., score_col: (hist, bin_edges) }]
def many_densities(groups, dimen_list, data, bins=30, density_scaling_factor=5, figsize=(10,10), all_label="difference"):

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
                            ["$\\bf{%s}$" % (all_label)])
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
            weights1 = groups[i-1].get('weights',None)
            weights2 = groups[i-2].get('weights', None)
        else:
            weights = group.get("weights", None)      
        for j, dimen in enumerate(dimen_list):    

            name = dimen
            if group is not None and name in group:
                hist, bin_edges = data[name]
            elif group is None:
                hist1, bin_edges1 = np.histogram(data[name], bins=bins, range=min_maxs[j], weights=weights1, density=False)
                hist2, bin_edges2 = np.histogram(data[name], bins=bins, range=min_maxs[j], weights=weights2, density=False)
                hist1 = hist1 / np.sum(hist1)
                hist2 = hist2 / np.sum(hist2)
                bin_edges = bin_edges1[:-1]     
                bin_edges2 = bin_edges2[:-1]     
                hist=hist2-hist1          
            else:
                hist, bin_edges = np.histogram(data[name], bins=bins, range=min_maxs[j], weights=weights, density=False)
                hist = hist / np.sum(hist)
                bin_edges = bin_edges[:-1]
            
            scaling_factor = (min_maxs[j][1] - min_maxs[j][0]) * density_scaling_factor
            x = bin_edges
            y = (scaling_factor * hist) + i
            score = 0.4
            axs[j].plot(x, y, color='black')
            axs[j].fill_between(x, y, i, alpha=score)
dimen_list=['affluence', 'age', 'gender', 'partisan', 'partisan-ness']

df4 = pd.read_csv(r"C:\Users\DELL XPS\Desktop\SummerResearch\full-analysis\datasets\Reddit_Sub_Com_v4_genre.csv")
genre = pd.read_csv("full-analysis\\datasets\\genre_names_v4.csv")

df4=pd.merge(df4,genre[['label','genre']],on='label')
genres = df4['genre'].unique()


df=pd.read_csv("C:\\Users\\DELL XPS\\Desktop\\SummerResearch\\data\\datasets-important\\comments_2mil.csv")
df2=pd.read_csv("C:\\Users\\DELL XPS\\Desktop\\SummerResearch\\full-analysis\\datasets\\cultural_scores.csv")
df2['partisan-ness'] = df2['partisan_neutral']

data=pd.DataFrame(df['subreddit'], columns = ['subreddit'])

data2=pd.merge(data,df2,left_on='subreddit',right_on='community')
data2=data2[['subreddit']+dimen_list]



df4= pd.merge(df4,df2,left_on='subreddit',right_on='community')

music=df4[['subreddit','genre']+dimen_list]
music['ppmi'] = 1
data2['genre'] = 'comment'
data2['ppmi'] = 1


all_df = music.append(data2)

all_df['w1'] = all_df.apply(lambda x: x['ppmi'] if x['genre'] != 'comment' else 0, axis =1)
all_df['w2'] = all_df['genre'].apply(lambda x: 1 if x =='comment' else 0)
all_df=all_df.dropna(subset=['genre'])
for g in genres:
    print(g)
    temp = all_df[(all_df['genre']==g) | (all_df['genre']=='comment')]
    n = len(temp)
    g_ = [g,'comment']
    w = ['w1','w2']

    groups = []
    for a,b in zip(g_,w):
        groups.append({'name': a,'weights':temp[b].values})

    many_densities(groups, dimen_list, temp, density_scaling_factor=2, figsize=[10,7])
    plt.savefig('C:\\Users\\DELL XPS\\Desktop\\SummerResearch\\full-analysis\\many-densities-difference-{}2'.format(g.replace('/','_')))
    plt.cla()
    plt.clf()
plt.show()










# to compare all music versus all comments 
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



many_densities(groups, dimen_list, df, density_scaling_factor=2.5, figsize=[8,5], bins = 20)
plt.savefig('full-analysis\\music_vs_comments_difference5.pdf', dpi = 300)
plt.show()
