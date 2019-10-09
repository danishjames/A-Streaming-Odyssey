import spotipy
import time
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 250)

client_id = ''
client_secret = ''

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

chart_df = pd.read_csv('chart_data.csv', index_col=0)

chart_df.dropna(axis=0, how='any', subset=['Artist'], inplace=True)

chart_df.drop(labels=['Song Links'], axis=1, inplace=True)

artist_df = chart_df.drop_duplicates(subset=['Artist'], keep='last')

artist_df.reset_index(drop=True, inplace=True)

artist_df.insert(4, 'Followers', 0, allow_duplicates=True)

counter = 0

for i in range(0, len(artist_df)):
    artist_df.loc[i, 'Followers'] = sp.search(q=artist_df.Artist[0], type='artist')['artists']['items'][0]['followers']['total']

    counter += 1

    if counter > 25:
        time.sleep(2)
        print('Cooling down...{} done and {} left.'.format(i, len(artist_df) - i))
        counter = 0

artist_df.to_csv(path_or_buf='./artist_data.csv', index=True)