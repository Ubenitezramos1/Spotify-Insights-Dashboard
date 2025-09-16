import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def get_spotify():
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI", "http://localhost:8888/callback")
    scope = "user-top-read user-read-recently-played"
    if not client_id or not client_secret:
        raise RuntimeError("Missing Spotify credentials in environment variables.")
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scope
    ))
    return sp