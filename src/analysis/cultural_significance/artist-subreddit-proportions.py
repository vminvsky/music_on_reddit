import pandas as pd 
import numpy as np 


posts = pd.read_csv("full-analysis\\datasets\\Reddit_Sub_Com_v4_genre.csv")
artists = posts['artist'].unique()
subs= posts['subreddit'].unique()

num_posts_sub = posts.groupby('subreddit')['Unnamed: 0'].count()
num_posts_subs_large = num_posts_sub[num_posts_sub>100]
ind = num_posts_subs_large.index

track_sub = posts.groupby(['subreddit','artist'])['Unnamed: 0'].count()
track_sub = track_sub.reset_index()


track_sub['count'] =0
for i, sub in enumerate(subs):
    print(i/len(subs))
    track_sub.loc[track_sub['subreddit'] == sub, 'count'] = num_posts_sub[num_posts_sub.index == sub].values[0]

track_sub2 = track_sub[track_sub['subreddit'].isin(ind)]
track_sub2['proportion'] = track_sub2['Unnamed: 0']/track_sub2['count']

average_proprotion = track_sub2.groupby('artist')['proportion'].agg(['mean','var'])

average_proprotion.to_csv("full-analysis\\datasets\\average-artist-proportion-subreddit_v4.csv")

average_proprotion = pd.read_csv("full-analysis\\datasets\\average-artist-proportion-subreddit_v4.csv")
average_proprotion.columns = ['mean','var']
average_proprotion = average_proprotion.reset_index()

track_sub2['mean'] = track_sub2.apply(lambda x: average_proprotion.loc[average_proprotion['artist']==x['artist'], 'mean'].values[0],axis=1)
track_sub2['var'] = track_sub2.apply(lambda x: average_proprotion.loc[average_proprotion['artist']==x['artist'], 'var'].values[0],axis=1)

track_sub2['z-score'] = (track_sub2['proportion'] - track_sub2['mean']) / track_sub2['var']**(1/2)

track_sub2.to_csv("full-analysis\\datasets\\z-scores.csv")

k = track_sub2[track_sub2['artist'] =='Rick Astley'].sort_values(by='z-score', ascending = False)

k.to_csv("rick-astley.csv")


