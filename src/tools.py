from auth import client
from resources import _get_uri_from_artist_song
from utils import logger, strip_uri


def _play_song_by_uri(uri: str) -> bool:
    try:
        sp = client.sp
        uri = strip_uri(uri)
        sp.start_playback(uris=[f"spotify:track:{uri}"])
        return True
    except Exception as e:
        logger.error(f"Failed to play song: {str(e)}")
        raise


def _play_song_by_artist(artist: str, song: str) -> bool:
    song_uri = _get_uri_from_artist_song(artist, song)
    if song_uri:
        return _play_song_by_uri(song_uri)
    else:
        return False


def _get_currently_playing() -> str:
    try:
        sp = client.sp
        current_track = sp.currently_playing()

        if current_track and current_track["is_playing"]:
            track_name = current_track["item"]["name"]
            artist_name = current_track["item"]["artists"][0]["name"]
            return f"Now playing: {track_name} by {artist_name}"
        else:
            return "No track is currently playing."
    except Exception as e:
        logger.error(f"Failed to get currently playing: {str(e)}")
        raise
