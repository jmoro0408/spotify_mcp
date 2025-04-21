from loguru import logger

from auth import SpotipyClient
from utils import strip_uri


def _play_song_by_uri(uri: str) -> bool:
    try:
        auth = SpotipyClient()
        sp = auth.sp
        uri = strip_uri(uri)
        sp.start_playback(uris=[f"spotify:track:{uri}"])
        return True
    except Exception as e:
        logger.error(f"Failed to play song: {str(e)}")
        raise
