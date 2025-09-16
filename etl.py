def load_top_tracks(sp, time_range="medium_term", limit=50):
    """Load user's top tracks and their audio features into the DB.

    Args:
        sp: Authenticated Spotipy client.
        time_range: One of "short_term" (4 weeks), "medium_term" (6 months), or "long_term" (several years).
        limit: Number of top tracks to fetch (max 50 per Spotify API).

    Returns:
        Number of tracks loaded.
    """
    from db import get_conn

    results = sp.current_user_top_tracks(time_range=time_range, limit=limit)
    items = results.get("items", [])
    if not items:
        return 0

    tracks_data = []
    artists_data = {}
    audio_features_data = []

    for item in items:
        track_id = item["id"]
        track_name = item["name"]
        artist = item["artists"][0]  # Primary artist
        artist_id = artist["id"]
        artist_name = artist["name"]
        genres = ", ".join(sp.artist(artist_id).get("genres", []))  # Fetch genres
        album_name = item["album"]["name"]
        release_date = item["album"]["release_date"]
        duration_ms = item["duration_ms"]
        popularity = item["popularity"]

        tracks_data.append((track_id, track_name, artist_id, album_name, release_date, duration_ms, popularity))
        if artist_id not in artists_data:
            artists_data[artist_id] = (artist_id, artist_name, genres)

    # Fetch audio features in bulk
    track_ids = [item["id"] for item in items]
    audio_features_list = sp.audio_features(tracks=track_ids)
    for af in audio_features_list:
        if af:  # Ensure audio features were returned
            audio_features_data.append((
                af["id"], af["danceability"], af["energy"], af["key"], af["loudness"],
                af["mode"], af["speechiness"], af["acousticness"], af["instrumentalness"],
                af["liveness"], af["valence"], af["tempo"]
            ))

    with get_conn() as conn:
        cursor = conn.cursor()

        # Insert artists
        cursor.executemany("""
            INSERT OR IGNORE INTO artists (artist_id, name, genres) VALUES (?, ?, ?)
        """, artists_data.values())


def load_recently_played(sp, limit=50):
    """Load user's recently played tracks into the DB.

    Args:
        sp: Authenticated Spotipy client.
        limit: Number of recent plays to fetch (max 50 per Spotify API).

    Returns:
        Number of plays loaded.
    """
    from db import get_conn

    results = sp.current_user_recently_played(limit=limit)
    items = results.get("items", [])
    if not items:
        return 0

    plays_data = []
    tracks_data = []
    artists_data = {}

    for item in items:
        track = item["track"]
        track_id = track["id"]
        track_name = track["name"]
        artist = track["artists"][0]  # Primary artist
        artist_id = artist["id"]
        artist_name = artist["name"]
        album_name = track["album"]["name"]
        release_date = track["album"]["release_date"]
        duration_ms = track["duration_ms"]
        popularity = track["popularity"]
        played_at = item["played_at"]
        context = item.get("context", {}).get("type", None)  # e.g., "playlist", "album"

        play_id = f"{track_id}::{played_at}"
        plays_data.append((play_id, track_id, played_at, context))
        tracks_data.append((track_id, track_name, artist_id, album_name, release_date, duration_ms, popularity))
        if artist_id not in artists_data:
            genres = ", ".join(sp.artist(artist_id).get("genres", []))  # Fetch genres
            artists_data[artist_id] = (artist_id, artist_name, genres)

    with get_conn() as conn:
        cursor = conn.cursor()

        # Insert artists
        cursor.executemany("""
            INSERT OR IGNORE INTO artists (artist_id, name, genres) VALUES (?, ?, ?)
        """, artists_data.values())

        # Insert tracks
        cursor.executemany("""
            INSERT OR IGNORE INTO tracks (track_id, name, artist_id, album_name, release_date, duration_ms, popularity)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, tracks_data)

        # Insert plays
        cursor.executemany("""
            INSERT OR IGNORE INTO plays (play_id, track_id, played_at, context) VALUES (?, ?, ?, ?)
        """, plays_data)


def df_top_tracks():
    """Fetch top tracks with audio features as a DataFrame."""
    import pandas as pd
    from db import get_conn

    query = """
        SELECT t.track_id, t.name AS track_name, a.name AS artist_name, t.album_name,
               t.release_date, t.duration_ms, t.popularity,
               af.danceability, af.energy, af.valence
        FROM tracks t
        JOIN artists a ON t.artist_id = a.artist_id
        LEFT JOIN audio_features af ON t.track_id = af.track_id
        ORDER BY t.popularity DESC
    """
    with get_conn() as conn:
        df = pd.read_sql_query(query, conn)
    return df

def df_recent_activity():
    """Fetch recent plays as a DataFrame."""
    import pandas as pd
    from db import get_conn

    query = """
        SELECT p.play_id, t.name AS track_name, a.name AS artist_name, p.played_at, p.context
        FROM plays p
        JOIN tracks t ON p.track_id = t.track_id
        JOIN artists a ON t.artist_id = a.artist_id
        ORDER BY p.played_at DESC
    """
    with get_conn() as conn:
        df = pd.read_sql_query(query, conn)
    return df