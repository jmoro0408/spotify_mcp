import os
import spotipy
from dotenv import find_dotenv, load_dotenv
from spotipy.oauth2 import SpotifyOAuth


class SpotipyClient:
    def __init__(self):
        load_dotenv(find_dotenv())
        scope = "user-library-read,user-read-playback-state,user-modify-playback-state,user-read-currently-playing"
        cache_path = os.path.join(os.path.expanduser("~"), ".spotify_mcp_cache")
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(scope=scope, cache_path=cache_path)
        )


client = SpotipyClient()
