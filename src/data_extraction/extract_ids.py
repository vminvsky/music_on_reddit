from sqlalchemy import create_engine
import pandas as pd

columns = ['author','score','link_id','subreddit','created_utc','id','parent_id']

#for tracks
def extract_spotify_ids(category):
    engine = create_engine('postgresql://venia:asdf@ada.ais.sandbox:5432/reddit')
    query = "select * from music_comments where body like '%%open.spotify.com/{}%%'".format(category)
    query2 = "select * from music_submissions where url like '%%open.spotify.com/%%'".format(category)
    df = pd.read_sql(query, engine)
    df2 = pd.read_sql(query2, engine)
    df[category] = df['body'].apply(lambda x: x[x.find('open.spotify.com/{}/'.format(category)) + 23: x.find('open.spotify.com/{}/'.format(category)) + 45])
    df2[category] = df2['url'].apply(lambda x: x[x.find('open.spotify.com/{}/'.format(category)) + 23: x.find('open.spotify.com/{}/'.format(category)) + 45])

    comments = pd.Series(pd.Series(df[category].unique()).append(pd.Series(df2[category].unique())).unique())
    submissions = pd.Series(pd.Series(df[category].unique()).append(pd.Series(df2[category].unique())).unique())
    ids = comments.append(submissions)
    dataframe = df.append(df2)
    return dataframe, ids

# save these files into the output folder: track_ids.to_csv("output\\track_ids.csv"), album_ids.to_csv("output\\album_ids.csv")



### this will extract youtube

# youtube links should be a list of youtube_links that we know are associated with youtube accounts 
def extract_youtube_ids(youtube_links):
    engine = create_engine('postgresql://venia:asdf@ada.ais.sandbox:5432/reddit')
    query_comment = "select * from music_comments where body like '%%youtube.com/watch?v=%%'"
    query_submission = "select * from music_submissions where url like '%%youtube.com/watch?v=%%'"
    comments = pd.read_sql(query_comment, engine)
    submissions = pd.read_sql(query_submission, engine)
    comments['youtube_id'] = comments['body'].apply(lambda x: x[x.find('youtube.com/watch?v='): x.find('youtube.com/watch?v=') + 31])
    submissions['youtube_id'] = submissions['url'].apply(lambda x: x[x.find('youtube.com/watch?v='): x.find('youtube.com/watch?v=') + 31])
    df = comments.append(submissions)
    df_clean = df[df['youtube_id'].isin(youtube_links)]
    return df_clean


