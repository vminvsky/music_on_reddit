import pandas as pd
import requests

### for youtube links that are associated with at least three songs, 
#youtube_id should be a dataframe with track name, youtube_id and artist. 


def validate(youtube_id, min_tracks = 3):
    k = youtube_id.groupby('youtube_id')['youtube_id'].count().sort_values()
    links =list(k[k>  min_tracks].index)
    title = r'\"title\":\"'
    lis = []
    lis2 = []
    for link in links: 
        r = requests.get('https://' +link)
        ind = r.text.find(title)
        text = r.text[ind+len(title):].find('\\\"')
        name = r.text[ind+len(title):ind+text]
        print(links.index(link))
        data = youtube_id[youtube_id['youtube_id'] == link]['track_name']
        index = data.index 
        names = data.values
        for i, n in zip(index, names):
            if n.lower() in name.lower():
                print('works')
                pass
            else:
                print('didnt work')
                lis.append({'link': link,'index':i,'track_name':n,'youtube_title': name})
                youtube_id.drop(i,inplace=True)
    return youtube_id

