import spotipy
from dotenv import find_dotenv, load_dotenv
from spotipy.oauth2 import SpotifyOAuth


class Authorizer:
    def __init__(self):
        load_dotenv(find_dotenv())

        scope = "user-library-read, user-read-playback-state,user-modify-playback-state"

        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
