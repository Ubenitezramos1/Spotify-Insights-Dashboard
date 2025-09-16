import streamlit as st
import sqlite3
from contextlib import contextmanager

DB_PATH = "spotify_insights.db"

@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

DDL = """
    PRAGMA foreign_keys = ON;

    CREATE TABLE IF NOT EXISTS artists (
        artist_id       TEXT PRIMARY KEY, 
        name            TEXT NOT NULL, 
        genres          TEXT
    );


    CREATE TABLE IF NOT EXISTS tracks (
        track_id        TEXT PRIMARY KEY, 
        name            TEXT NOT NULL, 
        artist_id       INTEGER, 
        album_name      TEXT, 
        release_date    TEXT, 
        duration_ms     INTEGER, 
        popularity      INTEGER,
        FOREIGN KEY (artist_id) REFERENCES artists(artist_id)
    );

    CREATE TABLE IF NOT EXISTS audio_features (
        track_id        TEXT PRIMARY KEY,
        danceability    REAL,
        energy          REAL,
        key             INTEGER,
        loudness        REAL,
        mode            INTEGER,
        speechiness     REAL,
        acousticness    REAL,
        instrumentalness REAL,
        liveness        REAL,
        valence         REAL,
        tempo           REAL,
        FOREIGN KEY (track_id) REFERENCES tracks(track_id)
    );

    CREATE TABLE IF NOT EXISTS plays (
        play_id    TEXT PRIMARY KEY, -- e.g., "{track_id}::{played_at}"
        track_id   TEXT NOT NULL,
        played_at  TEXT NOT NULL,    -- ISO8601 timestamp
        context    TEXT,             -- e.g., "playlist", "album"
        FOREIGN KEY (track_id) REFERENCES tracks(track_id)
    );
    
    CREATE INDEX IF NOT EXISTS idx_plays_played_at ON plays(played_at);
"""

def init_db():
    with get_conn() as conn:
        conn.executescript(DDL)