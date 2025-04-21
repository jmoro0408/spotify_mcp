from auth import SpotipyClient
from utils import strip_uri


def _play_song_by_uri(uri: str) -> None:
    auth = SpotipyClient()
    sp = auth.sp
    uri = strip_uri(uri)
    sp.start_playback(uris=[f"spotify:track:{uri}"])
    return None
