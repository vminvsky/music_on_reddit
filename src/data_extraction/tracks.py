from sqlalchemy import create_engine
import pandas as pd
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import numpy as np


client_credentials_manager = SpotifyClientCredentials(client_id='cf6ba0faa2b642d29a2694676ffe7e7a',client_secret='477d209e17f348f0a3c02a36df2cee66')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

### if you have a previous existing dataset of track ids
# old_data should be a list of track_ids we have already scraped. new_data should be a list of track_ids we have not yet scraped. 
def remove_duplicates(old_data, new_data):
    songids= list(set(new_data['0'].unique())-set(old_data.values))
    return songids


def extract_tracks(songids):
    j=0
    song_info = {}
    for i in songids:
        if j % 1000 == 40:
            pd.DataFrame.from_dict(song_info).T.to_csv("SongData2_temp.csv")
        j+=1
        try:
            print(j/len(songids))
            k = sp.track(i)
            artist = k['artists'][0]['name']
            album = k['album']['name'] 
            release_date = k['album']['release_date']
            popularity = k['popularity']
            explicit = k['explicit']
            track_name = k['name']
            song_info.update({i: {'artist': artist,'album': album,'release_date': release_date, 'popularity': popularity,'explicit': explicit,'track_name':track_name}})
        except:
            print('Id not found')
    df = pd.DataFrame.from_dict(song_info).T
    return df

# df2.to_csv('output\\TrackData.csv')
