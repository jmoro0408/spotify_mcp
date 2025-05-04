import logging
import random
import re

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


logger = logging.getLogger("spotify_mcp")


def strip_track_uri(uri: str) -> str:
    return re.sub(r"spotify:track:", "", uri)


def strip_playlist_uri(uri: str) -> str:
    return re.sub(r"spotify:playlist:", "", uri)


def true_shuffle(uris: list[str]) -> list[str]:
    return random.sample(uris, len(uris))
