# Music Sharing on Reddit

## Data Extraction
### Get spotify shares
First run function extract_spotify_ids from extract_links.py for both 'album' and 'track'. 
After running twice you should have four dataframes. Two consist of posts on Reddit that share songs or albums (this will be needed later). 
Second you will have a set of ids for albums and tracks (name them album_ids.csv and track_ids.csv)

Take the album_ids csv file and run it in album_tracks.py. This will create a csv of all metadata for the tracks in those albums. 
Similarily run tracks.py on the tracks_ids file to get metadata for all shared tracks.

Merge these two dataframes into one trackdata.csv file. 


### Get YouTube shares
Use trackdata.csv to create a list of the form ```[{'artist': artist_1,'track':track_1}, {'artist': artist_2, 'track':track_2'}...]```. Input this into get_youtbe_link.py. 
This will extract youtube links for the tracks we have. 

Next we need to validate these links. 

Take the output and use it in validate_youtube_links.py. This will ensure the YouTube links are correct. 

Finally go back to extract_links.py and run extract_youtube_ids with the youtube links we have. This will give us all shares that contain these youtube links. 

Append the YouTube shares dataframe to the Spotify shares dataframe. 

Finally merge the Reddits posts dataframe with the Spotify metadata we have. This should be merged on youtube_id, track_id, and album_id. 

## Data cleaning
Now that we have a dataset we can start running the analysis.
### Vectorize artists and create custom genres. 
Run create_genre.py on the dataset. This will create a dataframe for artist vectors and cluster each artist. 

### Name the custom genres
Run genre_cluster_plots.py to create bar plots for naming the custom genres. 

Go through these plots and name each of the genres in a seperate excel file. 




