import streamlit as st
from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from db import init_db
from etl import load_top_tracks, load_recently_played
from dashboards import top_tracks_viz, mood_profile_viz, recent_activity_viz, listening_heatmap_viz

load_dotenv()  # Load .env file

st.set_page_config(page_title="Spotify Music Insights", page_icon="🎵", layout="wide")

# ---------- Minimal CSS to match the wireframe ----------
st.markdown("""
<style>
.block-container {padding-top: 1.5rem; padding-bottom: 2rem;}
.card {background: #ffffff; border: 1px solid #e9e9e9; border-radius: 12px; padding: 16px;}
.card-soft {background: #f8f8f8; border: 1px solid #ececec; border-radius: 12px; padding: 14px;}
.hdr {font-weight: 700; font-size: 1.05rem; margin-bottom: 0.35rem;}
.subtle {color: #777;}
.step {display:flex; align-items:center; gap:.5rem; margin: .25rem 0;}
.step-dot {width: 14px; height: 14px; border-radius: 50%; background: #e0e0e0; display:inline-block;}
.step-dot.done {background: #1DB954;}
</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.title("🎵 Spotify Music Insights Dashboard")
st.caption("Personal analytics from your listening history.")
st.markdown('</div>', unsafe_allow_html=True)

# ---------- Layout: sidebar + main ----------
left, right = st.columns([0.23, 0.77], gap="medium")

with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("#### Steps")
    step1 = '<div class="step"><span class="step-dot"></span> 1. Connect Spotify</div>'
    step2 = '<div class="step"><span class="step-dot"></span> 2. Load Data</div>'
    step3 = '<div class="step"><span class="step-dot"></span> 3. View Insights</div>'
    step_container = st.empty()
    st.markdown('<div class="card-soft" style="margin-top:16px;">', unsafe_allow_html=True)
    st.write("**Privacy**")
    st.caption("Read-only access. No sharing. Revoke anytime.")
    st.markdown('</div>', unsafe_allow_html=True)
    st.caption("GitHub • Docs")
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    init_db()

    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")
    scope = "user-top-read user-read-recently-played"

    auth_manager = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scope,
        show_dialog=True
    )
    st.write("All query params:", st.query_params)
    # `st.query_params.get('code')` can be either a list (Streamlit sometimes
    # provides values as lists) or a plain string depending on how the URL was
    # constructed. Guard against both cases so we don't accidentally take only
    # the first character of the code when it's a string.
    raw_code = st.query_params.get("code", None)
    if isinstance(raw_code, list):
        code = raw_code[0] if raw_code else None
    else:
        code = raw_code

    # Normalize empty string to None for downstream checks
    if code == "":
        code = None

    st.write("Parsed code:", code)


    try:
        token_info = auth_manager.get_cached_token()
        st.write("Code from URL:", code)
        st.write("Token info from cache:", token_info)
        if not token_info:
            if code:
                # Exchange the code for a token and cache it
                token = auth_manager.get_access_token(code, as_dict=False)
                sp = spotipy.Spotify(auth=token)
                st.success("Connected to Spotify")
                step1 = '<div class="step"><span class="step-dot done"></span> 1. Connect Spotify</div>'
                step_container.markdown(step1 + step2 + step3, unsafe_allow_html=True)
            else:
                auth_url = auth_manager.get_authorize_url()
                st.warning("Please connect your Spotify account to continue.")
                st.markdown(f"[Login with Spotify]({auth_url})")
                st.stop()
        else:
            token = token_info['access_token']
            sp = spotipy.Spotify(auth=token)
            st.success("Connected to Spotify")
            step1 = '<div class="step"><span class="step-dot done"></span> 1. Connect Spotify</div>'
            step_container.markdown(step1 + step2 + step3, unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.write("#### Data Loader")

        top_tracks = sp.current_user_top_tracks(limit=10)
        recently_played = sp.current_user_recently_played(limit=10)

        st.write("#### Top Tracks")
        for item in top_tracks['items']:
            track = item['name']
            artist = item['artists'][0]['name']
            st.write(f"- {track} by {artist}")

        st.write("#### Recently Played")
        for item in recently_played['items']:
            track = item['track']['name']
            artist = item['track']['artists'][0]['name']
            st.write(f"- {track} by {artist}")

    except Exception as e:
        st.error(f"Spotify authentication or API call failed: {e}")