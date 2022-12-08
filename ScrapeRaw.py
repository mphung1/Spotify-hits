import numpy as np
import pandas as pd
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from time import sleep
from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
import time
import warnings
warnings.filterwarnings('ignore')

load_dotenv()
cid = os.getenv('client_id')
secret = os.getenv('client_secret')
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
username = 'Spotify'

# Create driver
# gecko=GeckoDriverManager().install()
driver = webdriver.Firefox(executable_path='C:\\Users\\pgmin\\.wdm\\drivers\\geckodriver\\win64\\0.32\\geckodriver.exe')

def fetch_songs_audio_features(year_start, year_end)
    for year in range(year_start, year_end):   
        driver.get('https://open.spotify.com/search/top hits of ' + str(year))
        time.sleep(4)

        playlist_els =  driver.find_element(By.XPATH, "//*[@class='ZWI7JsjzJaR_G8Hy4W6J']//span[normalize-space()='Playlists']")
        playlist_els.click() 
        time.sleep(3)

        playlist = driver.find_element(By.XPATH, "//*[@class='Nqa6Cw3RkDMV8QnYreTr']")
        playlist.click()
        playlist_link = driver.current_url
        playlist_id = playlist_link.split("/")[-1].split("?")[0]
        playlist_results = sp.user_playlist(username, playlist_id, 'tracks')
        time.sleep(3)

        playlist_tracks_data = playlist_results['tracks']
        playlist_tracks_id = []
        playlist_tracks_titles = []
        playlist_tracks_artists = []
        playlist_tracks_primary_artists = []

        for track in playlist_tracks_data['items']:
            playlist_tracks_id.append(track['track']['id'])
            playlist_tracks_titles.append(track['track']['name'])
            
            # Add a list of all artists involved in the song to the list of artists for the playlist
            artist_list = []
                for artist in track['track']['artists']:
                    artist_list.append(artist['name'])
                playlist_tracks_artists.append(artist_list)
                playlist_tracks_primary_artists.append(artist_list[0])

        # Get audio features for every song title
        features = sp.audio_features(playlist_tracks_id)
        songs_df = pd.DataFrame(data=features, columns=features[0].keys())

        songs_df['title'] = playlist_tracks_titles
        songs_df['primary_artist'] = playlist_tracks_primary_artists
        songs_df['all_artists'] = playlist_tracks_artists

        # Get the necessary columns
        songs_df = songs_df[['id', 'title', 'primary_artist', 'all_artists',
                                'danceability', 'energy', 'key', 'loudness',
                                'mode', 'speechiness', 'acousticness', 'instrumentalness',
                                'liveness', 'valence', 'tempo',
                                'duration_ms', 'time_signature']]
        
        # Convert song's duration to s
        songs_df["duration_s"] = songs_df.duration_ms.apply(lambda x : round(x/1000))
        songs_df.drop("duration_ms", axis=1, inplace=True)
        
        # Save the csv file for each year
        with open('./data/songs-'+str(year)+'.csv', 'w', encoding='utf-8') as f:
            songs_df.to_csv(f, header= True, index=True)

fetch_songs_audio_features(1970, 2020)