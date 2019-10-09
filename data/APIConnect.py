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

chart_df['Token'] = [chart_df['Song Links'][item].split('/')[-1] for item in range(0, len(chart_df['Song Links']))]

chart_df.dropna(axis=0, how='any', subset=['Artist'], inplace=True)

chart_df.drop(labels=['Song Links'], axis=1, inplace=True)

song_df = chart_df.drop_duplicates(subset=['Token'], keep='last')

song_df.insert(5, 'Duration', 0, allow_duplicates=True)
song_df.insert(6, 'Loudness', 0, allow_duplicates=True)
song_df.insert(7, 'Speechiness', 0, allow_duplicates=True)
song_df.insert(8, 'Energy', 0, allow_duplicates=True)
song_df.insert(9, 'Tempo', 0, allow_duplicates=True)
song_df.insert(10, 'Valence', 0, allow_duplicates=True)
song_df.insert(11, 'Instrumentalness', 0, allow_duplicates=True)
song_df.insert(12, 'Modality', 0, allow_duplicates=True)

counter = 0

song_df.reset_index(drop=True, inplace=True)

for i in range(0, len(song_df)):
    song_df.loc[i, 'Loudness'] = sp.audio_features(song_df.Token[i])[0]['loudness']
    song_df.loc[i, 'Speechiness'] = sp.audio_features(song_df.Token[i])[0]['speechiness']
    song_df.loc[i, 'Energy'] = sp.audio_features(song_df.Token[i])[0]['energy']
    song_df.loc[i, 'Tempo'] = sp.audio_features(song_df.Token[i])[0]['tempo']
    song_df.loc[i, 'Valence'] = sp.audio_features(song_df.Token[i])[0]['valence']
    song_df.loc[i, 'Instrumentalness'] = sp.audio_features(song_df.Token[i])[0]['instrumentalness']
    song_df.loc[i, 'Modality'] = sp.audio_features(song_df.Token[i])[0]['mode']
    song_df.loc[i, 'Duration'] = sp.audio_features(song_df.Token[i])[0]['duration_ms']
    counter += 1

    if counter > 25:
        time.sleep(2)
        print('Cooling down...{} done and {} left.'.format(i, len(song_df) - i))
        counter = 0

song_df.to_csv(path_or_buf='./song_data.csv', index=True)