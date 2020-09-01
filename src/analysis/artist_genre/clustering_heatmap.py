import matplotlib.pyplot as plt 
import pandas as pd 
import numpy as np 
import seaborn as sns 
from sklearn.metrics import pairwise

# option: artists we want to use
################################################ ARTISTS ###############################################

def artists_heatmap():
    NUMBER_ARTISTS = 30
    figsize = (10,10)
    method = 'average'
    category= 'artist'


    # getting the data to make plot for the artists 

    cosine = pd.read_csv("data\\artist_cosine_similarity.csv")
    cosine.index = cosine['artist']
    cosine.drop('artist',axis=1,inplace=True)
    art_cosine = [k.replace('$','S') for k in cosine.index]
    cosine.columns = art_cosine
    cosine.index = art_cosine


    # this defines the artists we will be including in our heatmap 
    counts= pd.read_csv("data\\artist_counts.csv")
    artists = counts.sort_values(by='count', ascending=False)['artist'].head(NUMBER_ARTISTS).values
    artists=[k.replace('$','S') for k in artists]


    # if we want to use the custom dataset with artist names
    # artists = artist_set['artist'].values

    cosine = cosine[cosine.index.isin(artists)]
    cosine = cosine[artists]
    cosine = cosine.T[artists]


    ### get the release_date info
    release_date = pd.read_csv(r"data\Artist_Release_Date.csv")
    release_date['name'] = release_date['name'].apply(lambda x: x.replace('$','S'))


    date = release_date[release_date['name'].isin(artists)]
    date.reset_index(inplace=True,drop=True)
    date.index=date['name']
    date = date.T[artists]
    date = date.T
    date['release_date']=pd.to_datetime(date['release_date'])
    date['release_date_y'] = date['release_date'].dt.year
    date=date.sort_values(by='release_date_y')


    # defines the colormap to show the age of the artist. 


    ran = date['release_date_y'].max() - date['release_date_y'].min() + 1

    years_list = list(np.arange(date['release_date_y'].min(),date['release_date_y'].max() + 1))

    palette = sns.color_palette("Blues", ran)

    date['palette'] = date['release_date_y'].apply(lambda x: palette[years_list.index(x)])

    temp = date[['release_date_y','palette']]
    temp.index = temp['release_date_y']
    temp = temp.drop('release_date_y',axis=1)
    lut = temp.to_dict()['palette']


    row_colors = pd.DataFrame(date['release_date_y'])['release_date_y'].map(lut)
    row_colors.name = 'release date'

    def create_heatmap(df, method, figsize, row_colors=None):
        '''df should be in the form of a cosine similarity matrix'''
        fig, (ax1,ax2) = plt.subplots(2)
        labels = df.index
        im = sns.clustermap(df,method=method,yticklabels=True, xticklabels=True, figsize=figsize, row_colors=row_colors, col_colors=row_colors)
        # sns.set(font_scale=0.65)    
        plt.tight_layout()
        return im 
    im =create_heatmap(cosine, method, figsize, row_colors)

    plt.subplots_adjust(bottom=0.28, right = 0.86)


    plt.savefig('images\\heatmap-{}-similarity-{}'.format(category, NUMBER_ARTISTS))

    plt.show()






################################################ GENRES ###############################################

def genre_heatmap():
    figsize = (15,15)
    method = 'average'
    category= 'genre'




    # getting the data to make plot for the genres 

    cosine = pd.read_csv(r"C:\Users\DELL XPS\Desktop\SummerResearch\full-analysis\datasets\genre_cosine_similiarity_v4.csv")
    cosine.index = cosine['genre']
    cosine.drop('genre',axis=1,inplace=True)


    sns.clustermap(cosine,yticklabels=True, xticklabels=True, figsize=figsize)
    plt.savefig(r"C:\Users\DELL XPS\Desktop\SummerResearch\full-analysis\genre_similarity")
    plt.show()


    ### get the release_date info
    release_date = pd.read_csv(r"full-analysis\genre_release_dates.csv")
    release_date.dropna(inplace=True)

    release_date.index=release_date['genre']
    release_date['mean_release_time']=pd.to_datetime(release_date['mean_release_time'])
    release_date['release_date_y'] = release_date['mean_release_time'].dt.year

    release_date = release_date.sort_values(by='release_date_y')
    # defines the colormap. 

    ran = release_date['release_date_y'].max() - release_date['release_date_y'].min() + 1

    years_list = list(np.arange(release_date['release_date_y'].min(),release_date['release_date_y'].max() + 1))

    palette = sns.color_palette("Blues", ran)

    release_date['palette'] = release_date['release_date_y'].apply(lambda x: palette[years_list.index(x)])

    temp = release_date[['release_date_y','palette']]
    temp.index = temp['release_date_y']
    temp = temp.drop('release_date_y',axis=1)
    lut = temp.to_dict()['palette']
    # lut = dict(zip(set(release_date['release_date_y']), sns.color_palette("Blues", len(set(release_date['release_date_y'])))))
    # lut = dict(zip(set(release_date['release_date_y']), sns.color_palette("Blues", ran)))

    row_colors = pd.DataFrame(release_date['release_date_y'])['release_date_y'].map(lut)




    def create_heatmap(df, method, figsize, row_colors=None):
        '''df should be in the form of a cosine similarity matrix'''
        labels = df.index
        im = sns.clustermap(df,method=method,yticklabels=True, xticklabels=True, figsize=figsize, row_colors=row_colors, col_colors=row_colors)
        sns.set(font_scale=0.65)    
        plt.tight_layout()
        return im 

    im =create_heatmap(cosine, method, figsize, row_colors)


    plt.subplots_adjust(bottom=0.28, right = 0.86)
    plt.savefig('version_1\\heatmap-{}-similarity'.format(category))
    plt.show()

