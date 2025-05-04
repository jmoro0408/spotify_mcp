# spotify_mcp

## Project Description

This project is a Spotify integration built using the Model Context Protocol (MCP). It provides a set of tools and resources that allow interaction with the Spotify API, enabling control over playback, access to user data, and more, all through the MCP framework.

## Setup

To get this project up and running, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/spotify_mcp.git
    cd spotify_mcp
    ```
    (Replace `your-username` with the actual repository owner and name if this is hosted on GitHub)

2.  **Set up a virtual environment (recommended):**
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    uv sync
    ```

4.  **Set up Spotify API Credentials:**
    - Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).
    - Log in and create a new application.
    - Note down your `Client ID` and `Client Secret`.
    - Add a Redirect URI. For local development, `http://localhost:8888/callback` is commonly used.
    - Create a `.env` file in the project root directory with the following content:
      ```env
      SPOTIPY_CLIENT_ID='YOUR_CLIENT_ID'
      SPOTIPY_CLIENT_SECRET='YOUR_CLIENT_SECRET'
      SPOTIPY_REDIRECT_URI='YOUR_REDIRECT_URI'
      ```
      Replace the placeholder values with your actual credentials and redirect URI.

5.  **Run the server:**
    ```bash
    python src/server.py
    ```
    This will start the MCP server, making the Spotify tools and resources available.

## Usage

Once the server is running and configured, you can interact with the Spotify API through the defined MCP tools. The specific methods for interacting with MCP tools will depend on the client application or framework you are using that supports MCP.

If using Claude as your MCP client, you need to edit your `claude_desktop_config.json` to include:

```
{
  "mcpServers": {
    "Spotify_MCP": {
      "command": "<FULL_UV_PATH>",
      "args": [
        "run",
        "--with",
        "mcp[cli]",
        "--with",
        "spotipy",
        "mcp",
        "run",
        <FULL_PATH_TO_MAIN.py>
      ],
      "env": {
        "SPOTIFY_CLIENT_ID": "<CLIENT_ID>",
        "SPOTIFY_CLIENT_SECRET": "<CLIENT_SECRET>",
        "SPOTIFY_REDIRECT_URI": "<REDIRECT_URI>"
      }
    }
  }
}
```

## Currently supported actions

1. Play a song
2. Get users playlists
3. Play from user playlist
4. Play from SP playlists like charts
5. Pause Playback
6. Skip to next
7. Skip to previous
8. Turn shuffle on
9. Turn shuffle off
10. Play a user's liked songs
11. Get recently played song
12. Add to queue
13. Get most played songs this week/month/year

## To Implement
1. Add a song to a playlist
2. Add tracks to playlist
3. Create a playlist
4. Get recently popular songs. i.e. songs that I discovered recently that I have been playing a lot of.
5. Generate LLM powered playlists. i.e. "Create a dance workout playlist based on my recent favorite artists"

## Project Structure

- `src/auth.py`: Handles Spotify API authentication.
- `src/main.py`: Likely the main entry point or core logic of the application.
- `src/resources.py`: Defines MCP resources for accessing Spotify data.
- `src/server.py`: The MCP server implementation.
- `src/tools.py`: Defines MCP tools for interacting with the Spotify API (the supported actions listed above).
- `src/utils.py`: Utility functions used across the project.
