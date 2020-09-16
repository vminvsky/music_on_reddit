import pandas as pd 
from sklearn.metrics import pairwise, r2_score
from scipy.stats import pearsonr
import seaborn as sns 
import matplotlib.pyplot as plt  
from matplotlib.lines import Line2D
import numpy as np
# plt.style.use(['science', 'no-latex'])
plt.rcParams['font.family'] = 'arial'


##### this is all preparing the data for the plot
df = pd.read_csv('full-analysis\\datasets\\Reddit_Sub_Com_v4_genre.csv')
genres = pd.read_csv('full-analysis\\datasets\\genre_names_v4.csv')[['label','genre','short']]
genres['short'] = genres['short'].fillna(genres['genre'])
gens = genres['short'].values
scores = pd.read_csv('full-analysis\\datasets\\cultural_scores.csv')


dimen_list = [k for k in scores.columns if k != 'community']

df=pd.merge(df,genres,on='label')

data=df[['artist','subreddit','short']]
data.columns = ['artist','community','genre']
data= pd.merge(data,scores, on='community')
artist_vals = data.groupby('artist')[dimen_list].mean()

# this will normalize the results by a max min scaler 

genre_vals = data.groupby('genre')[dimen_list].mean()

for k in dimen_list:
    max_v = genre_vals[k].max()
    min_v = genre_vals[k].min()
    dif = max_v - min_v 
    genre_vals[k] = genre_vals[k].apply(lambda x: (x- min_v) / dif)


genre_vals.reset_index(inplace=True)
genre_vals = pd.melt(genre_vals, id_vars=['genre'])

genre_vals.columns = ['genre','dimension','score']

vals = genre_vals

vals = vals.sort_values(by='score', ascending=True)
vals['score'] = vals['score']

dimen_list = ['age', 'partisan', 'gender', 'affluence', 'sociality', 'partisan_neutral']



vals = vals[vals['dimension'].isin(dimen_list)]




# vals['genre'] = vals['genre'].apply(lambda x: x if len(x)<12 else x[0:12] + '.')

vals.to_csv("full-analysis\\genre_cultural_feats.csv")


### this is the actual plot 
# plt.rcParams["font.family"] = "serif"




vals['dimension'] = vals['dimension'].apply(lambda x: x if x != 'partisan_neutral' else 'partisan-ness')

fig, ax = plt.subplots(1, figsize = (11,5))
sns.stripplot(x=vals['dimension'],y=vals['score'], jitter = False, ax=ax, orient='v', alpha = 0.6)
dimen_list = list(vals['dimension'].unique())

y_old = {key:value for (key,value) in zip(dimen_list, np.zeros(len(dimen_list))-1)}




for i in range(len(vals)):
    x = vals['dimension'].values[i]
    y = vals['score'].values[i]
    s = vals['genre'].values[i]
    if (abs(y - y_old[x]) >= 0.03) & ((s!='k-pop2') | (x != 'partisan')):
        ax.annotate(s= s, xy= (dimen_list.index(x),y), xytext= (dimen_list.index(x)- 0.1, y), horizontalalignment='right', arrowprops=dict(arrowstyle='-'), fontsize=8, color='black', verticalalignment='center')
        y_old[x] = y
    else:
        pass

# for i in range(len(vals)):
#     x = vals['dimension'].values[i]
#     y = vals['score'].values[i]
#     s = vals['genre'].values[i]
#     if abs(y - y_old[x]) >= 0.03:
#         im.annotate(x=dimen_list.index(x)- 0.03, y=y, s=s, horizontalalignment='right', fontsize=8, color='black', verticalalignment='center')
#         y_old[x] = y
#     else:
#         pass

for tick in ax.xaxis.get_major_ticks():
    tick.label.set_fontsize(12) 

for tick in ax.yaxis.get_major_ticks():
    tick.label.set_fontsize(12) 


plt.ylabel('score', fontsize = 12)
    
plt.xlabel(None)
plt.tight_layout()
plt.savefig('full-analysis\\cultural-dimensions-plot10_s.pdf', dpi = 300)
plt.show()


# left_side = ax.spines["left"]
# left_side.set_visible(False)

# right_side = ax.spines["right"]
# right_side.set_visible(False)
# top = ax.spines["top"]
# top.set_visible(False)

# bottom = ax.spines["bottom"]
# bottom.set_visible(False)

plt.show()
