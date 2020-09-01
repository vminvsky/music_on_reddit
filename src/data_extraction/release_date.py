import pandas as pd 
import datetime as dt
import numpy as np


## data should be all the track id metadata. This should include the popularity and release date column. 
def artist_release_date(data):
    ids = data.groupby('artist')['popularity'].idxmax()

    artists=data['artist'].unique()
    artists = [x for x in artists if str(x) != 'nan']
    data=[]

    for a in artists:
        temp = data.iloc[ids[a]]
        release_date = temp['release_date']
        popularity = temp['popularity']
        data.append({'name': a,'release_date': release_date,'popularity':popularity})

    artist_period = pd.DataFrame(data)
    artist_period['release_date']=pd.to_datetime(artist_period['release_date'])
    artist_period['release_date_s'] = (artist_period['release_date'] - dt.datetime(1970,1,1)).dt.total_seconds()
    return artist_period

artist_period = artist_release_date(data)
artist_period.to_csv("data\\Artist_Release_Date.csv")



# create average age of genres
release_date = pd.read_csv(r"C:\Users\DELL XPS\Desktop\SummerResearch\Artist_Release_Date.csv")
release_date.columns=['Unnamed: 0','artist','release_date','popularity','release_date_s']
release_date=release_date[['artist','release_date','popularity']]

custom_genres = pd.read_csv(r"C:\Users\DELL XPS\Desktop\SummerResearch\full-analysis\datasets\genre_names_v4.csv")
df = pd.read_csv(r'C:\Users\DELL XPS\Desktop\SummerResearch\full-analysis\datasets\Reddit_Sub_Com_v4_genre.csv')

df = pd.merge(df, custom_genres, on='label', how='left')

df=df[['genre','artist']]

df2=pd.merge(df, release_date, on ='artist')

df2['release_date']=pd.to_datetime(df2['release_date'])

genres = df2['genre'].unique()

periods = []
for g in genres:
    print(g)
    temp = df2.loc[df2['genre'] == g,'release_date'].mean()
    periods.append({'genre':g,'mean_release_time': temp})

release_date_genres = pd.DataFrame(periods)

release_date_genres.to_csv("full-analysis\\genre_release_dates.csv")
