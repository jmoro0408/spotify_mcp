import spotipy
from dotenv import find_dotenv, load_dotenv
from spotipy.oauth2 import SpotifyOAuth


class SpotipyClient:
    def __init__(self):
        load_dotenv(find_dotenv())
        scope = "user-library-read,user-read-playback-state,user-modify-playback-state,user-read-currently-playing, playlist-read-private, playlist-read-collaborative"
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(scope=scope, cache_path=".cache")
        )


client = SpotipyClient()
client = SpotipyClient()
