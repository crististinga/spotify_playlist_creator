from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth




URL = "https://www.billboard.com/charts/hot-100/"
CLIENT_ID = "6303592b0403481e87e1e84d1a3809ad"
CLIENT_SECRET = "35e20c6aa3944f679de476315fa4ab17"
REDIRECT_URL = "http://example.com"


date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
year = date[0:4]

response = requests.get(f"{URL}{date}")
billboard = response.text


soup = BeautifulSoup(billboard, "html.parser")

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URL,
                                               scope="playlist-modify-private",
                                               show_dialog=True,
                                               cache_path="token.txt"))
user_id = sp.current_user()["id"]

song_names_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_spans]
songs_uri = []

for name in song_names:
    item = sp.search(q=f"track {name} year {year}", type="track")
    try:
        uri = item["tracks"]["items"][0]["uri"]
        songs_uri.append(uri)
    except IndexError:
        print(f"{name} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)

sp.playlist_add_items(playlist_id=playlist["id"], items=songs_uri)
