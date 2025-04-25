import difflib

from auth import client
from server import mcp
from utils import logger


@mcp.resource(
    "play://{artist}_{song}",
    name="get_uri_from_artist_song",
    description="get unique spotify uri from artist and song",
)
def _get_uri_from_artist_song(artist: str, song: str) -> str | None:
    """
    Get a unique Spotify URI for a song given its artist and song name.

    Args:
        artist (str): The name of the artist of the song to search for.
        song (str): The name of the song to search for.

    Returns:
        str | None: The URI of the first matching track, or None if no results were returned.
    """
    try:
        sp = client.sp
        query = f"artist:{artist} track:{song}"
        results = sp.search(q=query, type="track", limit=1)
        if results is None:
            return None
        tracks = results["tracks"]["items"]
        if tracks:
            return tracks[0]["uri"]
        else:
            return None
    except Exception as e:
        logger.error(f"Failed to get uri from artist and song: {str(e)}")
        raise


def get_all_user_playlists():
    """
    Get a list of all user playlists.

    Returns:
        list[dict]: A list of playlist dictionaries.
    """
    all_playlists = []
    sp = client.sp
    results = sp.current_user_playlists(limit=50)
    while results:
        all_playlists.extend(results["items"])
        if results["next"]:
            results = sp.next(results)
        else:
            break
    return all_playlists


def _get_user_playlists() -> list[str]:
    """
    Retrieve the names of all playlists for the current user.

    Returns:
        list[str]: A list of playlist names as strings. Returns an empty
        list if no playlists are found or an error occurs.
    """

    try:
        playlists = get_all_user_playlists()
        if playlists is None:
            return []
        return [x["name"] for x in playlists]

    except Exception as e:
        logger.error(f"Failed to get user playlists: {str(e)}")
        raise


def _get_user_playlist_id(
    playlist_name: str, similarity_threshold: float = 0.6
) -> str | None:
    """
    Get the ID of a user's playlist given its name.

    Args:
        playlist_name (str): The name of the user's playlist to search for.
        similarity_threshold (float, optional): The minimum similarity score
            required to consider a playlist name a match. Defaults to 0.6.

    Returns:
        str | None: The ID of the user's playlist, or None if no matching playlist
            was found.
    """

    sp = client.sp

    all_playlists = []
    results = sp.current_user_playlists()
    while results:
        all_playlists.extend(results["items"])
        if results["next"]:
            results = sp.next(results)
        else:
            break

    playlist_names = [p["name"] for p in all_playlists]

    matches = difflib.get_close_matches(
        playlist_name, playlist_names, n=1, cutoff=similarity_threshold
    )

    if matches:
        best_match = matches[0]
        playlist = next(p for p in all_playlists if p["name"] == best_match)
        return playlist["id"]
    else:
        logger.error("Playlist ID not found.")
        return None


@mcp.resource(
    "read://recent_tracks",
    name="get_recent_tracks",
    description="get user's recently played tracks",
)
def _get_recent_tracks() -> dict[str, str]:
    """
    Retrieve the user's recently played tracks.

    Returns:
        list[str]: A list of URIs for the user's recently played tracks.

    Raises:
        Exception: If an error occurs while fetching the recent tracks.
    """

    recently_played = client.sp.current_user_recently_played(limit=10)
    if recently_played:
        track_names = []
        artists = []
        for track in recently_played["items"]:
            track_names.append(track["track"]["name"])
            artists.append(track["track"]["artists"][0]["name"])
        return dict(zip(artists, track_names, strict=True))
    else:
        logger.error("Failed to get recent tracks")
        raise


if __name__ == "__main__":
    print(_get_recent_tracks())
