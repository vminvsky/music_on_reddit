import pandas as pd 
import numpy as np 

df = pd.read_csv("full-analysis\\datasets\\Reddit_Sub_Com_v4_genre.csv")
track_data=pd.read_csv("data\\datasets-important\\TrackData.csv")
track_data=track_data.drop_duplicates(subset=['track_id'])

data = pd.merge(df,track_data, on = 'track_id')
data['artist']=data['artist_y']

art_son = data.groupby('artist')['track_name'].agg(pd.Series.mode)
art_son=art_son.reset_index()

art_son['key'] = art_son['artist']+art_son['track_name']

unique = data.groupby('artist')['track_name'].count()
unique = unique.reset_index()

artist_song = data.groupby(['artist','track_name'])['Unnamed: 0_x'].count()
artist_song=artist_song.reset_index()

artist_song = pd.merge(artist_song, unique, on = 'artist')
artist_song.columns = ['artist','track_name','song_count','artist_count']

artist_song['proporition'] = artist_song['song_count']/artist_song['artist_count']
artist_song['key'] = artist_song['artist'] + artist_song['track_name']


art_son['key'] = art_son['key'].apply(lambda x: str(x))
artist_song['key'] = artist_song['key'].apply(lambda x: str(x))
data =  pd.merge(art_son, artist_song[['key','proporition']], on = 'key')
data.drop('key',axis=1,inplace=True)

data.to_csv("artist-song.csv")