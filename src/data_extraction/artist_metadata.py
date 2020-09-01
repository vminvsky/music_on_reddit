from sqlalchemy import create_engine
import pandas as pd
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import numpy as np

client_credentials_manager = SpotifyClientCredentials(client_id='cf6ba0faa2b642d29a2694676ffe7e7a',client_secret='477d209e17f348f0a3c02a36df2cee66')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

artist_info = {}
def artist_data(artistids):
    for i in artistids:
        try:
            print(list(artistids).index(i))
            k = sp.artist(i)
            artist = k['name']
            popularity = k['popularity']
            genres = k['genres']
            followers = k['followers']
            artist_info.update({i: {'artist': artist,'popularity': popularity, 'genres': genres,'followers':followers}})
        except:
            print('link is fake news')
    df2 = pd.DataFrame.from_dict(artist_info).T
    return df2
