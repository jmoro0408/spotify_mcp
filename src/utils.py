import logging
import re

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


logger = logging.getLogger("spotify_mcp")


def strip_uri(uri: str) -> str:
    return re.sub(r"spotify:track:", "", uri)
