from auth import client
from resources import _get_playlist_id, _get_uri_from_artist_song, _get_user_playlists
from utils import logger, strip_playlist_uri, strip_track_uri


def _play_song_by_uri(uri: str) -> bool:
    try:
        sp = client.sp
        uri = strip_track_uri(uri)
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


def _list_user_playlists() -> str:
    user_playlists = _get_user_playlists()
    return f"User playlists: {', '.join(user_playlists)}"


def _play_playlist_by_id(playlist_uri: str) -> bool:
    playlist_uri = strip_playlist_uri(playlist_uri)
    sp = client.sp
    devices = sp.devices()
    device_id = None
    if devices is None or "devices" not in devices:
        logger.error("Failed to get active devices")
        return False

    for d in devices["devices"]:
        if d["is_active"]:
            device_id = d["id"]
            break

    playlist_uri = f"spotify:playlist:{playlist_uri}"

    sp.start_playback(device_id=device_id, context_uri=playlist_uri)
    logger.info(f"Playing playlist: {playlist_uri}")
    return True


def _play_playlist_by_name(playlist_name: str) -> bool:
    playlist_id = _get_playlist_id(playlist_name)
    if playlist_id:
        return _play_playlist_by_id(playlist_id)
    else:
        return False


if __name__ == "__main__":
    print(_play_playlist_by_name("Aug 22"))
