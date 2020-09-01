import pandas as pd 
from sqlalchemy import create_engine
import pandas as pd
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import numpy as np


client_credentials_manager = SpotifyClientCredentials(client_id='cf6ba0faa2b642d29a2694676ffe7e7a',client_secret='477d209e17f348f0a3c02a36df2cee66')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# albums should be a list of all the album ids. this should be from pd.read_csv("output\\album_ids.csv")
def extract_album_tracks(albums):
    data={}
    i=0
    for album in albums:
        if i % 1000== 1:
            df2 = pd.DataFrame.from_dict(data,orient='index')
            df2.to_csv('album_tracks_temp.csv')
        i+=1
        try:
            print(album)
            a = sp.album_tracks(album)['items']
            b = sp.album(album)
            release_date = b['release_date']
            popularity = b['popularity']
            track_names = [k['name'] for k in a]
            track_ids = [k['id'] for k in a]
            artists = [k['artists'][0]['name'] for k in a]
            artist_ids = [k['artists'][0]['id'] for k in a]
            data.update({album:
            {'track_names': track_names, 
            'release_date':release_date,
            'popularity':popularity,
            'track_ids': track_ids,
            'artists':artists,
            'artist_ids':artist_ids}})
        except:
            print("didn't work")
    df = pd.DataFrame.from_dict(data,orient='index')
    return df

