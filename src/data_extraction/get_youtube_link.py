import pandas as pd 
import requests

# input should be a list of dictionaries of the following form [{'artist': artist_1,'track':track_1}, {'artist': artist_2, 'track':track_2'}...]
# if you wish to run this program paralelly start and end mark the values to start and end at
def get_youtube_links(values,start,end):
    for i in range(start, end):
        try:
            print("We're on track {}".format(i))
            if i % 300==50:
                pd.DataFrame(values).to_csv('TracksWithYouTubeLink2{}_{}.csv'.format(start,end))
            artist = values[i]['artist'].replace(' ','+')
            title = values[i]['track'].replace(' ', '+')
            r = requests.get('http://www.last.fm/music/{}/_/{}'.format(artist, title)).text
            ind = r.find('data-track-name=\"{}\"'.format(title))
            youtube_id = r[ind-18:ind-7]
            values[i].update({'youtube_id':youtube_id})
        except:
            print('cound not find this youtube link')
    return values

