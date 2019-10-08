import spotipy
import time
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 250)

client_id = 'client_id'
client_secret = 'client_secret'

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

chart_df = pd.read_csv('chart_data.csv', index_col=0)

chart_df['Token'] = [chart_df['Song Links'][item].split('/')[-1] for item in range(0, len(chart_df['Song Links']))]

chart_df.insert(6, 'Loudness', 0, allow_duplicates=True)
counter = 0

test_set_df = chart_df[0:1000]

for i in range(0, len(test_set_df)):
    test_set_df.loc[i, 'Loudness'] = sp.audio_features(test_set_df.Token[i])[0]['loudness']
    counter += 1

    if counter > 25:
        time.sleep(2)
        print('Cooling down...{} done and {} left.'.format(i, len(test_set_df)-i))
        counter = 0

test_set_df.to_csv(path_or_buf='./MVP_data.csv', index=True)