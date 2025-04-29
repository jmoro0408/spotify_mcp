from auth import client
from resources import (
    _get_recent_tracks,
    _get_uri_from_artist_song,
    _get_user_playlist_id,
    _get_user_playlists,
)
from server import mcp
from utils import logger, strip_playlist_uri, strip_track_uri


def get_device_id():
    devices = client.sp.devices()
    if not devices:
        raise Exception("No active devices found. Please open Spotify on a device.")

    return devices["devices"][0]["id"]


@mcp.tool(
    name="play_song_by_uri", description="play a song on spotify given its unique uri"
)
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


@mcp.tool(
    name="play_public_playlist_by_name",
    description="play a public playlist given it's name",
)
def play_public_playlist_by_name(playlist_name: str) -> bool:
    """
    Play a public playlist on Spotify using its name.

    Args:
        playlist_name (str): The name of the public playlist to play.

    Returns:
        bool: True if the playlist was successfully played, False otherwise.
    """
    playlist_id = _get_playlist_id(playlist_name)
    if playlist_id:
        return _play_playlist_by_id(playlist_id)
    else:
        return False


@mcp.tool(
    name="play_song_by_artist_song",
    description="play a song on spotify given its artist and song",
)
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


@mcp.tool(
    name="get_currently_playing",
    description="get the currently playing artist and song",
)
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


@mcp.tool(
    name="get_user_playlists",
    description="list the users playlists",
)
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

    device_id = get_device_id()

    playlist_uri = f"spotify:playlist:{playlist_uri}"

    sp.start_playback(device_id=device_id, context_uri=playlist_uri)
    logger.info(f"Playing playlist: {playlist_uri}")
    return True


@mcp.tool(
    name="play_user_playlist_by_name",
    description="play a user's playlist given its name",
)
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


@mcp.tool(
    name="pause_playback",
    description="pause playback on active device",
)
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


@mcp.tool(
    name="start_playback",
    description="start playback on active device",
)
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


@mcp.tool(
    name="next_track",
    description="skip to next track on active device",
)
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


@mcp.tool(
    name="previous_track",
    description="skip to previous track on active device",
)
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


@mcp.tool(
    name="turn_shuffle_on",
    description="Toggle shuffle on active device",
)
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


@mcp.tool(
    name="turn_shuffle_off",
    description="Toggle shuffle off active device",
)
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


@mcp.tool(
    name="play_user_liked_songs",
    description="Play the user's liked songs",
)
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


@mcp.tool(
    name="get_recent_tracks",
    description="Return the user's recently played tracks",
)
def get_recent_tracks() -> bool:
    """
    Return the user's recently played tracks.

    Returns:
        dict[str, str]: A dictionary of recently played tracks with artist as the key and song as the value.
    """
    tracks = _get_recent_tracks()
    if not tracks:
        logger.error("Failed to get recent tracks")
        raise
    return tracks


@mcp.tool(
    name="add_track_to_queue_by_artist_and_song",
    description="Add a track to the active device's queue",
)
def add_to_queue_by_artist_and_song(artist: str, song: str) -> bool:
    """
    Add a track to the active device's queue given its artist and song name.

    Args:
        artist (str): The name of the artist of the track to add to the queue.
        song (str): The name of the track to add to the queue.

    Returns:
        bool: True if the track was successfully added to the queue, False otherwise.
    """

    try:
        uri = _get_uri_from_artist_song(artist=artist, song=song)
        client.sp.add_to_queue(uri)
        return True
    except Exception as e:
        logger.error(f"Failed to add track to queue: {str(e)}")
        raise


@mcp.tool(
    name="play_top_tracks_short_term",
    description="Play the user's top 20 tracks from the last month.",
)
def play_top_tracks_short_term():
    """
    Play the user's top 20 tracks from the last month.

    Returns:
        bool: True if the tracks were successfully played, False otherwise.
    """
    top_tracks = client.sp.current_user_top_tracks(limit=20, time_range="short_term")
    if top_tracks:
        track_uris = [track["uri"] for track in top_tracks["items"]]
    else:
        logger.error("Failed to get top tracks")
        raise

    device_id = get_device_id()
    client.sp.start_playback(device_id=device_id, uris=track_uris)

    logger.info("Now playing your top 20 tracks from the last month.")


@mcp.tool(
    name="play_top_tracks_medium_term",
    description="Play the user's top 20 tracks from the last 6 months.",
)
def play_top_tracks_medium_term():
    """
    Play the user's top 20 tracks from the 6 months.

    Returns:
        bool: True if the tracks were successfully played, False otherwise.
    """
    top_tracks = client.sp.current_user_top_tracks(limit=20, time_range="medium_term")
    if top_tracks:
        track_uris = [track["uri"] for track in top_tracks["items"]]
    else:
        logger.error("Failed to get top tracks")
        raise

    device_id = get_device_id()
    client.sp.start_playback(device_id=device_id, uris=track_uris)

    logger.info("Now playing your top 20 tracks from the last 6 months.")


@mcp.tool(
    name="play_top_tracks_long_term",
    description="Play the user's top 20 tracks from the last 6 months.",
)
def play_top_tracks_long_term():
    """
    Play the user's top 20 tracks from the year.

    Returns:
        bool: True if the tracks were successfully played, False otherwise.
    """
    top_tracks = client.sp.current_user_top_tracks(limit=20, time_range="long_term")
    if top_tracks:
        track_uris = [track["uri"] for track in top_tracks["items"]]
    else:
        logger.error("Failed to get top tracks")
        raise

    device_id = get_device_id()
    client.sp.start_playback(device_id=device_id, uris=track_uris)

    logger.info("Now playing your top 20 tracks from the last year.")


if __name__ == "__main__":
    print(play_top_tracks_short_term())
