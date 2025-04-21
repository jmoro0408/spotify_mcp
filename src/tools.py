from auth import client
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
