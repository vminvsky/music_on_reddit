from sqlalchemy import create_engine
import pandas as pd

#for tracks
engine = create_engine('postgresql://venia:asdf@ada.ais.sandbox:5432/reddit')
query = "select * from music_comments where body like '%%youtube.com/watch?v=%%'"

df = pd.read_sql(query, engine)
df = df[['score','link_id','author','subreddit','body','created_utc','id','parent_id']]
df['link'] = df['body'].apply(lambda x: x[x.find('youtube.com/watch?v='):x.find('youtube.com/watch?v=')+31])

df.to_csv("Reddit_Comments_YouTube_f.csv")