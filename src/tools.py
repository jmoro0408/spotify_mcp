from auth import client
from resources import (
    _get_uri_from_artist_song,
    _get_user_playlist_id,
    _get_user_playlists,
)
from utils import logger, strip_playlist_uri, strip_track_uri


def _play_song_by_uri(uri: str) -> bool:
    """
    Play a song by its URI.

    Args:
        uri (str): The URI of the song to play.

    Returns:
        bool: True if the song was successfully played, False otherwise.
    """
    try:
        sp = client.sp
        uri = strip_track_uri(uri)
        sp.start_playback(uris=[f"spotify:track:{uri}"])
        return True
    except Exception as e:
        logger.error(f"Failed to play song: {str(e)}")
        raise


def _play_song_by_artist(artist: str, song: str) -> bool:
    """
    Play a song by its artist and song name.

    Args:
        artist (str): The name of the artist of the song to play.
        song (str): The name of the song to play.

    Returns:
        bool: True if the song was successfully played, False otherwise.
    """
    song_uri = _get_uri_from_artist_song(artist, song)
    if song_uri:
        return _play_song_by_uri(song_uri)
    else:
        return False


def _get_currently_playing() -> str:
    """
    Get the currently playing track and artist.

    Returns:
        str: The name of the currently playing track and artist, or a message
            indicating that no track is currently playing.
    """
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
    """
    List the names of the user's playlists.

    Returns:
        str: A comma-separated string of the user's playlist names.
    """
    user_playlists = _get_user_playlists()
    return f"User playlists: {', '.join(user_playlists)}"


def _play_playlist_by_id(playlist_uri: str) -> bool:
    """
    Play a playlist on Spotify using its URI.

    Args:
        playlist_uri (str): The URI of the playlist to play.

    Returns:
        bool: True if the playlist was successfully played, False otherwise.
    """

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


def _play_user_playlist_by_name(playlist_name: str) -> bool:
    """
    Play a user's playlist by its name.

    Args:
        playlist_name (str): The name of the user's playlist to play.

    Returns:
        bool: True if the playlist was successfully played, False otherwise.
    """

    playlist_id = _get_user_playlist_id(playlist_name)
    if playlist_id:
        return _play_playlist_by_id(playlist_id)
    else:
        return False


def _get_playlist_id(query: str, limit: int = 50) -> str | None:
    # limit is high becauses sometimes intial results are None
    """
    Search for a playlist with the given query and return its uri.

    Args:
        query (str): The query to search for.
        limit (int, optional): The number of results to limit to. Defaults to 50.

    Returns:
        str | None: The uri of the first playlist found, or None if no results were returned.
    """
    sp = client.sp
    results = sp.search(q=query, type="playlist", limit=limit)
    if results is None:
        return None
    results = [x for x in results["playlists"]["items"] if x]
    logger.info(f"Found playlist: {results[0]['name']}")
    return results[0]["uri"]


def _pause_playback() -> bool:
    """
    Pause the user's active Spotify playback.

    Returns:
        bool: True if the playback was successfully paused, False otherwise.
    """
    try:
        sp = client.sp
        sp.pause_playback()
        logger.info("Playback paused")
        return True
    except Exception as e:
        logger.error(f"Failed to pause playback: {str(e)}")
        raise


def _start_playback() -> bool:
    """
    Start the user's active Spotify playback.

    Returns:
        bool: True if the playback was successfully started, False otherwise.
    """
    try:
        sp = client.sp
        sp.start_playback()
        logger.info("Playback started")
        return True
    except Exception as e:
        logger.error(f"Failed to start playback: {str(e)}")
        raise


def _next_track() -> bool:
    """
    Skip to the next track on the user's active Spotify playback.

    Returns:
        bool: True if the track was successfully skipped, False otherwise.
    """
    try:
        sp = client.sp
        sp.next_track()
        logger.info("Skipped to next track")
        return True
    except Exception as e:
        logger.error(f"Failed to skip to next track: {str(e)}")
        raise


def _previous_track() -> bool:
    """
    Skip to the previous track on the user's active Spotify playback.

    Returns:
        bool: True if the track was successfully skipped, False otherwise.
    """
    try:
        sp = client.sp
        sp.previous_track()
        logger.info("Skipped to previous track")
        return True
    except Exception as e:
        logger.error(f"Failed to skip to previous track: {str(e)}")
        raise


def _turn_shuffle_on() -> bool:
    """
    Enable shuffle on the user's active Spotify playback.

    Returns:
        bool: True if shuffle was successfully enabled, False otherwise.
    """
    try:
        sp = client.sp
        sp.shuffle(True)
        logger.info("Shuffle on")
        return True
    except Exception as e:
        logger.error(f"Failed to shuffle: {str(e)}")
        raise


def _turn_shuffle_off() -> bool:
    """
    Disable shuffle on the user's active Spotify playback.

    Returns:
        bool: True if shuffle was successfully disabled, False otherwise.
    """

    try:
        sp = client.sp
        sp.shuffle(False)
        logger.info("Shuffle off")
        return True
    except Exception as e:
        logger.error(f"Failed to shuffle: {str(e)}")
        raise


def _play_user_liked_songs() -> bool:
    """
    Play the user's liked songs.

    Returns:
        bool: True if the tracks were successfully played, False otherwise.
    """
    current_user_saved_tracks = client.sp.current_user_saved_tracks()
    if current_user_saved_tracks:
        tracks = current_user_saved_tracks["items"]
        uris = [track["track"]["uri"] for track in tracks]
        client.sp.start_playback(uris=uris)
        return True
    else:
        logger.error("Failed to get user saved tracks")
        raise


if __name__ == "__main__":
    print(_play_user_liked_songs())
